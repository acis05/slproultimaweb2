import threading
import json, logging, sqlite3, uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from .config import HOST,PORT,DB_PATH,LOG_DIR,BASE_DIR, BACKUP_DIR, WEB_MODE, DATABASE_BACKEND, IS_POSTGRES
from .product import PRODUCT_NAME, IS_ULTIMA, VERSION
from .database import init_database, backup_database, DB_OPERATIONAL_ERRORS, DB_INTEGRITY_ERRORS
from . import repository as repo
from . import order_dp
from . import reporting
from . import excel_import
from . import coa_templates
from . import owner_cloud, licensing, saas
from .webui import HTML
from .owner_admin_ui import OWNER_HTML
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s",
handlers=[logging.FileHandler(LOG_DIR/"server.log",encoding="utf-8"),logging.StreamHandler()])
log=logging.getLogger("stokledger")
DATABASE_SWITCH_REQUESTED = False
ACTIVE_SERVER = None
class E(Exception):
    def __init__(self,s,m):self.s=s;self.m=m
class H(BaseHTTPRequestHandler):
    def log_message(self,f,*a):log.info("%s - %s",self.client_address[0],f%a)
    def out(self,s,b,t):
        self.send_response(s)
        self.send_header("Content-Type",t);self.send_header("Content-Length",str(len(b)))
        self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","SAMEORIGIN")
        self.send_header("Referrer-Policy","same-origin")
        self.send_header("Permissions-Policy","camera=(), microphone=(), geolocation=()")
        if str(self.headers.get("X-Forwarded-Proto","")).lower()=="https":
            self.send_header("Strict-Transport-Security","max-age=31536000; includeSubDomains")
        self.end_headers();self.wfile.write(b)
    def js(self,s,d):self.out(s,json.dumps(d,ensure_ascii=False).encode(),"application/json; charset=utf-8")
    def fileout(self,content,filename):
        self.send_response(200);self.send_header("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition",'attachment; filename="'+str(filename).replace('"','')+'"')
        self.send_header("Content-Length",str(len(content)));self.send_header("Cache-Control","no-store")
        self.end_headers();self.wfile.write(content)
    def body(self):
        length=int(self.headers.get("Content-Length","0") or 0)
        if length>40*1024*1024: raise E(413,"Ukuran data terlalu besar.")
        try:return json.loads(self.rfile.read(length).decode() or "{}")
        except:raise E(400,"JSON tidak valid.")
    def token(self):
        v=self.headers.get("Authorization","");return v[7:].strip() if v.lower().startswith("bearer ") else ""
    def me(self,perm=None):
        u=repo.authenticate(self.token())
        if not u:raise E(401,"Sesi tidak valid.")
        if perm and not repo.allowed(u,perm):raise E(403,"Tidak punya hak akses.")
        return u
    def cost_allowed(self,user):
        return repo.allowed(user,"cost.view")
    def mask_cost_item(self,item):
        if not isinstance(item,dict): return item
        hidden={"purchase_price","average_cost","stock_value","average_cost_before","average_cost_after","unit_cost","purchase_price_snapshot","cost_of_goods","inventory_value","cogs_value"}
        return {k:(None if k in hidden else v) for k,v in item.items()}
    def mask_cost_items(self,items):
        return [self.mask_cost_item(x) for x in items]

    def safe(self,func,*args):
        try:return func(*args)
        except ValueError as x:raise E(400,str(x))
        except DB_OPERATIONAL_ERRORS as x:
            log.exception('Database operational error')
            raise E(500,'Struktur database belum lengkap atau database sedang sibuk: '+str(x))
        except DB_INTEGRITY_ERRORS as x:
            text=str(x)
            if "products.sku" in text:raise E(409,"Kode Barang / SKU sudah digunakan.")
            if "products.barcode" in text:raise E(409,"Barcode sudah digunakan oleh barang lain.")
            if "brands.code" in text:raise E(409,"Kode merk sudah digunakan.")
            if "salespersons.code" in text:raise E(409,"Kode salesman sudah digunakan.")
            if "business_partners.code" in text:raise E(409,"Kode pelanggan/pemasok sudah digunakan.")
            low=text.lower()
            if "unique constraint failed" in low or "duplicate key value" in low or "unique constraint" in low:
                raise E(409,"Kode atau nomor tersebut sudah digunakan.")
            if "foreign key constraint failed" in low or "foreign key constraint" in low:
                raise E(400,"Data referensi tidak valid atau sudah tidak tersedia.")
            raise
    def edition_guard(self, path, method="GET"):
        if IS_ULTIMA:
            return
        blocked_prefixes=("/api/project-","/api/projects/","/api/departments/")
        if path.startswith(blocked_prefixes):
            raise E(403,"Fitur Proyek dan Departemen hanya tersedia pada StokLedger Pro Ultima.")
        if path in ("/api/project-budgets","/api/projects") and method != "GET":
            raise E(403,"Fitur Proyek hanya tersedia pada StokLedger Pro Ultima.")
        if path == "/api/departments" and method != "GET":
            raise E(403,"Fitur Departemen hanya tersedia pada StokLedger Pro Ultima.")

    def do_GET(self):
        try:
            p=urlparse(self.path);path=p.path;q=parse_qs(p.query)
            self.edition_guard(path,"GET")
            if path=="/":self.out(200,HTML.encode(),"text/html; charset=utf-8")
            elif path=="/owner-admin":self.out(200,OWNER_HTML.encode(),"text/html; charset=utf-8")
            elif path=="/api/owner/accounts":
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                self.js(200,{"items":saas.list_accounts(q.get("q",[""])[0],q.get("status",[""])[0])})
            elif path=="/api/owner/discounts":
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                self.js(200,{"items":saas.list_discounts()})
            elif path=="/assets/stokledger-logo.png":
                asset=BASE_DIR/"assets"/"stokledger-logo.png"
                self.out(200,asset.read_bytes(),"image/png")
            elif path=="/favicon.ico":
                asset=BASE_DIR/"assets"/"favicon.ico"
                self.out(200,asset.read_bytes(),"image/x-icon")
            elif path=="/assets/stokledger-icon.png":
                asset=BASE_DIR/"assets"/"stokledger-icon.png"
                self.out(200,asset.read_bytes(),"image/png")
            elif path=="/api/master-import/types":self.me("inventory.manage");self.js(200,{"items":excel_import.available_types()})
            elif path=="/api/master-import/template":
                user=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not user or not repo.allowed(user,"inventory.manage"):raise E(401,"Sesi download template tidak valid.")
                content,filename=self.safe(excel_import.template,q.get("type",[""])[0]);self.fileout(content,filename)
            elif path=="/api/health":
                self.js(200,{"status":"ok","app":PRODUCT_NAME+" Server","version":VERSION,"edition":PRODUCT_NAME,"is_ultima":IS_ULTIMA,"web_mode":WEB_MODE,"database_backend":DATABASE_BACKEND,"platform_mode":"MULTI_TENANT_SAAS" if IS_POSTGRES else "SINGLE_DATABASE","trial_days":7,"trial_users":2,"registration_enabled":bool(IS_POSTGRES)})
            elif path=="/api/system/storage-info":
                self.me("settings.manage");self.js(200,{"database":"PostgreSQL" if IS_POSTGRES else str(DB_PATH),"backend":DATABASE_BACKEND,"backup_directory":"Railway PostgreSQL Backups" if IS_POSTGRES else str(BACKUP_DIR),"data_directory":"PostgreSQL managed" if IS_POSTGRES else str(DB_PATH.parent)})
            elif path=="/api/me":self.js(200,{"user":self.me()})
            elif path=="/api/license-status":self.me();self.js(200,repo.license_status())
            elif path=="/api/subscription-admin":
                u=self.me();
                if u.get("role",{}).get("code")!="ADMIN": raise E(403,"Khusus Administrator.")
                self.js(200,repo.subscription_admin_status(u))
            elif path=="/api/company-logo":
                user=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not user:raise E(401,"Sesi tidak valid.")
                content,mime=repo.company_logo_bytes()
                if not content:raise E(404,"Logo belum tersedia.")
                self.out(200,content,mime or "image/png")
            elif path=="/api/company-profile":self.me();self.js(200,repo.company_profile())
            elif path=="/api/price-levels":self.me("partners.view");self.js(200,{"items":repo.list_price_levels(q.get("active",[None])[0]=="1" if q.get("active",[None])[0] is not None else None)})
            elif path=="/api/brands":self.me("inventory.view");self.js(200,{"items":repo.list_brands(q.get("active",["0"])[0]=="1")})
            elif path=="/api/salespersons":self.me("partners.view");self.js(200,{"items":repo.list_salespersons(q.get("active",["0"])[0]=="1")})
            elif path=="/api/permissions":self.me("users.manage");self.js(200,{"items":repo.permissions_catalog()})
            elif path=="/api/roles":self.me("users.manage");self.js(200,{"items":repo.list_roles()})
            elif path=="/api/users":self.me("users.manage");self.js(200,{"items":repo.list_users()})
            elif path=="/api/audit":self.me("audit.view");self.js(200,{"items":repo.list_audit(q.get("limit",["100"])[0])})
            elif path=="/api/partners/summary":self.me("partners.view");self.js(200,repo.partner_summary())
            elif path=="/api/partners":
                self.me("partners.view");active=q.get("active",[None])[0];av=None if active is None else active=="1"
                self.js(200,{"items":repo.list_partners(q.get("q",[""])[0],q.get("type",[None])[0],av)})
            elif path=="/api/company-profile":self.safe(repo.update_company_profile,self.me("settings.manage"),self.body(),self.client_address[0]);self.js(200,{"status":"updated"})
            elif path.startswith("/api/document-templates/"):
                item=self.safe(repo.update_document_template,self.me("settings.manage"),
                  path.rsplit("/",1)[1],self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/flexible-invoice-templates/"):
                item=self.safe(repo.save_flexible_invoice_template,self.me("settings.manage"),self.body(),self.client_address[0],int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/coa/"):
                self.js(200,{"status":"updated","id":self.safe(repo.update_coa,self.me("accounting.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])})
            elif path.startswith("/api/roles/"):
                item=self.safe(repo.update_role,self.me("users.manage"),
                  path.rsplit("/",1)[1],self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/users/"):
                item=self.safe(repo.update_user,self.me("users.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/departments/"):
                item=self.safe(repo.update_department,self.me("departments.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/projects/"):
                item=self.safe(repo.update_project,self.me("projects.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/partners/"):
                self.me("partners.view");item=repo.get_partner(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Pelanggan/supplier tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/assemblies":self.me("inventory.view");self.js(200,{"items":repo.list_assemblies(q.get("limit",["200"])[0])})
            elif path.startswith("/api/assemblies/"):
                self.me("inventory.view");item=repo.get_assembly(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Assembly tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/inventory/summary":self.me("inventory.view");self.js(200,repo.inventory_summary())
            elif path=="/api/inventory-engine/summary":self.me("inventory.view");self.js(200,repo.inventory_engine_summary())
            elif path=="/api/warehouses":self.me("inventory.view");self.js(200,{"items":repo.list_warehouses(q.get("active",["0"])[0]=="1")})
            elif path=="/api/inventory-balances":
                user=self.me("inventory.view");items=repo.inventory_balances(q.get("warehouse_id",[None])[0],q.get("q",[""])[0],q.get("low_stock",["0"])[0]=="1")
                self.js(200,{"items":items if self.cost_allowed(user) else self.mask_cost_items(items)})
            elif path=="/api/inventory-card":
                user=self.me("inventory.view");items=repo.inventory_card(q.get("product_id",[None])[0],q.get("warehouse_id",[None])[0],q.get("limit",["200"])[0])
                self.js(200,{"items":items if self.cost_allowed(user) else self.mask_cost_items(items)})
            elif path=="/api/departments":
                self.me("departments.view");self.js(200,{"items":self.safe(repo.list_departments,q.get("active",["0"])[0]=="1") if IS_ULTIMA else []})
            elif path=="/api/projects":
                self.me("projects.view");self.js(200,{"items":self.safe(repo.list_projects,q.get("active",["0"])[0]=="1") if IS_ULTIMA else []})
            elif path=="/api/project-documents/file":
                user=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not user or not repo.allowed(user,"projects.view"):raise E(401,"Sesi download dokumen tidak valid.")
                item,content=self.safe(repo.project_document_file,int(q.get("id",["0"])[0]))
                mime=item.get("mime_type") or "application/octet-stream"
                self.send_response(200);self.send_header("Content-Type",mime)
                disposition="inline" if mime.startswith("image/") or mime=="application/pdf" else "attachment"
                clean_name=str(item.get("original_filename") or "dokumen").replace('"',"")
                self.send_header("Content-Disposition",f'{disposition}; filename="{clean_name}"')
                self.send_header("Content-Length",str(len(content)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(content)
            elif path=="/api/project-documents":
                self.me("projects.view")
                self.js(200,{"items":self.safe(repo.list_project_documents,q.get("project_id",[None])[0],q.get("category",[None])[0],q.get("q",[None])[0],q.get("history",["0"])[0]=="1"),"categories":repo.PROJECT_DOCUMENT_CATEGORIES})
            elif path=="/api/project-progress": self.me("projects.view");self.js(200,{"items":self.safe(repo.list_project_progress,q.get("project_id",[None])[0])})
            elif path=="/api/project-terms": self.me("projects.view");self.js(200,{"items":self.safe(repo.list_project_terms,q.get("project_id",[None])[0])})
            elif path=="/api/project-contractor-dashboard": self.me("projects.view");self.js(200,self.safe(repo.project_contractor_dashboard,q.get("project_id",[None])[0]))
            elif path=="/api/project-cost-realizations":
                self.me("projects.view")
                project_id=q.get("project_id",[None])[0]
                if project_id in (None,""):raise E(400,"Proyek wajib dipilih.")
                self.js(200,self.safe(repo.project_cost_realization_details,
                  project_id,q.get("limit",["500"])[0]))
            elif path=="/api/assemblies":self.js(201,{"status":"created","result":self.safe(repo.create_assembly,self.me("inventory.manage"),d,self.client_address[0])})
            elif path.startswith("/api/assemblies/") and path.endswith("/finish"):
                aid=int(path.split("/")[3]);self.js(201,{"status":"finished","result":self.safe(repo.finish_assembly,self.me("inventory.manage"),aid,d,self.client_address[0])})
            elif path=="/api/project-material-issues":
                self.me("inventory.view")
                self.js(200,{"items":self.safe(repo.list_project_material_issues,
                  q.get("project_id",[None])[0],q.get("limit",["300"])[0])})
            elif path=="/api/project-budgets":
                self.me("inventory.view")
                project_id=q.get("project_id",[None])[0]
                self.js(200,{"items":self.safe(repo.list_project_budgets,project_id)})
            elif path=="/api/project-budgets/overview":
                self.me("inventory.view")
                self.js(200,self.safe(repo.project_budget_overview))
            elif path=="/api/service-categories":
                self.me("services.view")
                self.js(200,{"items":self.safe(
                  repo.list_service_categories,q.get("active",["0"])[0]=="1")})
            elif path=="/api/services":
                self.me("services.view")
                active=q.get("active",[None])[0]
                active_value=None if active is None else active=="1"
                self.js(200,{"items":self.safe(repo.list_services,
                  q.get("q",[""])[0],active_value,q.get("category_id",[None])[0])})
            elif path=="/api/categories":self.me("inventory.view");self.js(200,{"items":repo.list_categories(q.get("active",["0"])[0]=="1")})
            elif path=="/api/units":self.me("inventory.view");self.js(200,{"items":repo.list_units(q.get("active",["0"])[0]=="1")})
            elif path=="/api/products":
                user=self.me("inventory.view");active=q.get("active",[None])[0];av=None if active is None else active=="1"
                items=repo.list_products(q.get("q",[""])[0],av,q.get("low_stock",["0"])[0]=="1")
                self.js(200,{"items":items if self.cost_allowed(user) else self.mask_cost_items(items)})
            elif path.startswith("/api/products/"):
                user=self.me("inventory.view");item=repo.get_product(int(path.rsplit("/",1)[1]));
                if item and not self.cost_allowed(user): item=self.mask_cost_item(item)
                if not item:raise E(404,"Barang tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/stock-movements":
                self.me("inventory.view");self.js(200,{"items":repo.stock_movements(q.get("product_id",[None])[0],q.get("limit",["100"])[0])})
            elif path=="/api/coa-templates":
                self.me("accounting.view")
                self.js(200,{"items":self.safe(coa_templates.list_templates)})
            elif path=="/api/coa-template-preview":
                self.me("accounting.view")
                self.js(200,self.safe(coa_templates.preview,q.get("template",[""])[0]))
            elif path=="/api/project-cost-accounts":
                user=self.me("reports.view")
                if not repo.allowed(user,"projects.view"):raise E(403,"Anda tidak memiliki akses laporan proyek.")
                self.js(200,{"items":self.safe(repo.list_project_cost_accounts)})
            elif path=="/api/coa":self.me("accounting.view");self.js(200,{"items":repo.list_coa(q.get("active",["0"])[0]=="1")})
            elif path=="/api/journals":self.me("accounting.view");self.js(200,{"items":repo.list_journals(q.get("q",[""])[0],q.get("date_from",[None])[0],q.get("date_to",[None])[0],q.get("limit",["300"])[0])})
            elif path.startswith("/api/journals/"):
                self.me("accounting.view");item=repo.get_journal(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Jurnal tidak ditemukan.")
                self.js(200,item)
            elif path.startswith("/api/transaction-maintenance/"):
                self.me();parts=path.strip("/").split("/");kind=parts[2]
                if len(parts)==3:self.js(200,{"items":self.safe(repo.list_transaction_maintenance,kind,q.get("limit",["500"])[0])})
                else:
                    item=self.safe(repo.get_transaction_maintenance,kind,parts[3])
                    if not item:raise E(404,"Transaksi tidak ditemukan.")
                    self.js(200,item)
            elif path=="/api/reports":
                user=self.me("reports.view")
                if q.get("type",[""])[0].startswith("project_") and not repo.allowed(user,"projects.view"):
                    raise E(403,"Anda tidak memiliki akses laporan proyek.")
                filters={k:v[0] for k,v in q.items()}
                data=self.safe(reporting.report_data,q.get("type",[""])[0],filters)
                if not self.cost_allowed(user): data=reporting.redact_cost_data(data)
                self.js(200,data)
            elif path=="/api/reports/export":
                export_user=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not export_user or not repo.allowed(export_user,"reports.view"):raise E(401,"Sesi ekspor tidak valid.")
                if q.get("type",[""])[0].startswith("project_") and not repo.allowed(export_user,"projects.view"):
                    raise E(403,"Anda tidak memiliki akses laporan proyek.")
                filters={k:v[0] for k,v in q.items()}
                content,mime,filename=self.safe(reporting.export_report,q.get("type",[""])[0],q.get("format",["xlsx"])[0],filters,repo.allowed(export_user,"cost.view"))
                self.send_response(200);self.send_header("Content-Type",mime)
                self.send_header("Content-Disposition",'attachment; filename="'+filename.replace('"','')+'"')
                self.send_header("Content-Length",str(len(content)));self.send_header("Cache-Control","no-store")
                self.end_headers();self.wfile.write(content)

            elif path=="/api/sales/template":
                u=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not u:raise E(401,"Sesi tidak valid.")
                content=self.safe(repo.sales_excel_template);self.fileout(content,"Template_Impor_Penjualan.xlsx")
            elif path=="/api/purchases/template":
                u=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not u:raise E(401,"Sesi tidak valid.")
                content=self.safe(repo.purchase_excel_template);self.fileout(content,"Template_Impor_Pembelian.xlsx")
            elif path=="/api/cash-transactions/template":
                u=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not u:raise E(401,"Sesi tidak valid.")
                content=self.safe(repo.cash_excel_template);self.fileout(content,"Template_Impor_Kas_Bank.xlsx")
            elif path=="/api/manual-journals/template":
                user=repo.authenticate(q.get("token",[""])[0] or self.token())
                if not user or not repo.allowed(user,"accounting.manage"):raise E(401,"Sesi tidak valid.")
                content=self.safe(repo.manual_journal_excel_template)
                self.send_response(200)
                self.send_header("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition",'attachment; filename="Template_Impor_Jurnal_Manual.xlsx"')
                self.send_header("Content-Length",str(len(content)));self.end_headers();self.wfile.write(content)
            elif path=="/api/general-ledger":self.me("accounting.view");self.js(200,self.safe(repo.general_ledger,q.get("account_id",[None])[0],q.get("date_from",[None])[0],q.get("date_to",[None])[0],q.get("partner_id",[None])[0]))
            elif path=="/api/income-statement":self.me("accounting.view");self.js(200,repo.income_statement(q.get("date_from",[None])[0],q.get("date_to",[None])[0]))
            elif path=="/api/trial-balance":self.me("accounting.view");self.js(200,self.safe(repo.trial_balance,q.get("date_from",[None])[0],q.get("date_to",[None])[0]))
            elif path=="/api/receivables":self.me("receivables.view");self.js(200,{"items":repo.open_receivables(q.get("customer_id",[None])[0],q.get("as_of",[None])[0])})
            elif path=="/api/payables":self.me("payables.view");self.js(200,{"items":repo.open_payables(q.get("supplier_id",[None])[0],q.get("as_of",[None])[0])})
            elif path=="/api/receivables/aging":self.me("receivables.view");self.js(200,repo.receivables_aging(q.get("as_of",[None])[0]))
            elif path=="/api/payables/aging":self.me("payables.view");self.js(200,repo.payables_aging(q.get("as_of",[None])[0]))
            elif path=="/api/cash/summary":self.me("cash.view");self.js(200,repo.cash_summary())
            elif path=="/api/cash-accounts":self.me("cash.view");self.js(200,{"items":repo.cash_accounts(q.get("active",["0"])[0]=="1")})
            elif path=="/api/cash-transactions":self.me("cash.view");self.js(200,{"items":repo.list_cash_transactions(q.get("account_id",[None])[0],q.get("q",[""])[0],q.get("date_from",[None])[0],q.get("date_to",[None])[0],q.get("limit",["300"])[0])})
            elif path=="/api/purchase-returns":self.me("purchases.view");self.js(200,{"items":repo.list_purchase_returns()})
            elif path.startswith("/api/purchase-returns/"):
                self.me("purchases.view");item=repo.get_purchase_return(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Retur pembelian tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/sales-returns":self.me("sales.view");self.js(200,{"items":repo.list_sales_returns()})
            elif path.startswith("/api/sales-returns/"):
                self.me("sales.view");item=repo.get_sales_return(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Retur penjualan tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/sales-orders":self.me("sales.view");self.js(200,{"items":order_dp.list_orders("sales")})
            elif path.startswith("/api/sales-orders/"):self.me("sales.view");item=order_dp.get_order("sales",int(path.rsplit("/",1)[1]));self.js(200,item or {"error":"Tidak ditemukan"})
            elif path=="/api/purchase-orders":self.me("purchases.view");self.js(200,{"items":order_dp.list_orders("purchase")})
            elif path.startswith("/api/purchase-orders/"):self.me("purchases.view");item=order_dp.get_order("purchase",int(path.rsplit("/",1)[1]));self.js(200,item or {"error":"Tidak ditemukan"})
            elif path=="/api/customer-downpayments":self.me("receivables.view");self.js(200,{"items":order_dp.list_dp("customer")})
            elif path=="/api/supplier-downpayments":self.me("payables.view");self.js(200,{"items":order_dp.list_dp("supplier")})
            elif path=="/api/customer-downpayment-allocations":self.me("receivables.view");self.js(200,{"items":order_dp.list_allocations("customer")})
            elif path=="/api/supplier-downpayment-allocations":self.me("payables.view");self.js(200,{"items":order_dp.list_allocations("supplier")})
            elif path=="/api/purchases/summary":self.me("purchases.view");self.js(200,repo.purchases_summary(q.get("date_from",[None])[0],q.get("date_to",[None])[0]))
            elif path=="/api/purchases":self.me("purchases.view");self.js(200,{"items":repo.list_purchases(q.get("q",[""])[0],q.get("date_from",[None])[0],q.get("date_to",[None])[0],q.get("limit",["200"])[0])})
            elif path.startswith("/api/purchases/"):
                self.me("purchases.view");item=repo.get_purchase(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Pembelian tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/document-numbers":self.me("sales.manage");self.js(200,repo.document_number_suggestions(q.get("date",[None])[0]))
            elif path=="/api/dashboard-analytics":self.me("dashboard.view");self.js(200,repo.dashboard_analytics(q.get("as_of",[None])[0]))
            elif path=="/api/fixed-assets":self.me("accounting.view");self.js(200,{"items":repo.list_fixed_assets()})
            elif path=="/api/fixed-assets/depreciations":self.me("accounting.view");self.js(200,{"items":repo.list_fixed_asset_depreciations(q.get("asset_id",[None])[0])})
            elif path.startswith("/api/fixed-assets/"):
                self.me("accounting.view");item=repo.get_fixed_asset(int(path.rsplit("/",1)[1]))
                if not item:raise E(404,"Aktiva tetap tidak ditemukan.")
                self.js(200,item)
            elif path=="/api/customers":self.me("partners.view");self.js(200,{"items":repo.list_customers(q.get("q",[""])[0],q.get("active",["1"])[0]=="1")})
            elif path=="/api/suppliers":self.me("partners.view");self.js(200,{"items":repo.list_suppliers(q.get("q",[""])[0],q.get("active",["1"])[0]=="1")})
            elif path=="/api/document-templates":self.me("settings.view");self.js(200,{"items":repo.document_templates()})
            elif path=="/api/flexible-invoice-templates":
                self.me("settings.view");self.js(200,{"items":repo.flexible_invoice_templates(q.get("active",["0"])[0]=="1"),"blocks":[{"key":k,"label":v} for k,v in repo.FLEX_INVOICE_BLOCKS]})
            elif path=="/api/active-sessions":self.me("users.manage");self.js(200,{"items":repo.list_active_sessions(),"idle_seconds":licensing.DEVICE_IDLE_SECONDS})
            elif path=="/api/owner-mobile":self.me("dashboard.view");self.js(200,repo.owner_mobile_dashboard())
            elif path=="/api/owner-cloud/status":self.me("settings.manage");self.js(200,owner_cloud.status())
            elif path=="/api/owner-cloud/logs":self.me("settings.manage");self.js(200,{"items":owner_cloud.logs(q.get("limit",["50"])[0])})
            elif path.startswith("/print/"):
                parts=path.strip("/").split("/")
                if len(parts)!=3:raise E(404,"Dokumen tidak ditemukan.")
                print_user=repo.authenticate(q.get("token",[""])[0])
                if not print_user or not repo.allowed(print_user,"reports.view"):
                    raise E(401,"Sesi cetak tidak valid.")
                if parts[1]=="sales-invoice-flex":
                    body=self.safe(repo.render_flexible_invoice_html,int(parts[2]),q.get("template_id",[None])[0]).encode()
                else:
                    body=self.safe(repo.render_document_html,parts[1],int(parts[2])).encode()
                self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
            elif path=="/api/sales/summary":self.me("sales.view");self.js(200,repo.sales_summary(q.get("date_from",[None])[0],q.get("date_to",[None])[0]))
            elif path=="/api/sales":self.me("sales.view");self.js(200,{"items":repo.list_sales(q.get("q",[""])[0],q.get("date_from",[None])[0],q.get("date_to",[None])[0],q.get("limit",["200"])[0])})
            elif path.startswith("/api/sales/"):
                self.me("sales.view");item=repo.get_sale(int(path.rsplit("/",1)[1]));
                if not item:raise E(404,"Penjualan tidak ditemukan.")
                self.js(200,item)
            else:raise E(404,"Endpoint tidak ditemukan.")
        except E as e:self.js(e.s,{"error":e.m})
        except Exception:
            ref=uuid.uuid4().hex[:8].upper();log.exception("GET gagal [%s]",ref)
            self.js(500,{"error":f"Kesalahan internal server. Referensi: {ref}"})
    def do_POST(self):
        try:
            path=urlparse(self.path).path;d=self.body()
            if path=="/api/signup":
                account=self.safe(saas.register_account,d)
                self.js(201,{"status":"created","account":{"account_code":account["account_code"],"company_name":account["company_name"],"email":account["email"],"trial_expires_at":account["trial_expires_at"],"days_remaining":account["days_remaining"]}})
            elif path=="/api/owner/login":
                token=self.safe(saas.owner_login,d.get("password"));self.js(200,{"token":token})
            elif path=="/api/owner/discounts":
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                code=self.safe(saas.save_discount,d);self.js(201,{"status":"saved","code":code})
            elif path.startswith("/api/owner/accounts/") and path.endswith("/activate"):
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                aid=int(path.split("/")[4]);item=self.safe(saas.activate_account,aid,d.get("plan_code"),d.get("addon_users",0),d.get("discount_code",""),d.get("starts_at"),d.get("notes",""));self.js(200,{"status":"activated","item":item})
            elif path.startswith("/api/owner/accounts/") and path.endswith("/reset-trial"):
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                aid=int(path.split("/")[4]);self.js(200,{"status":"trial_reset","item":self.safe(saas.reset_trial,aid)})
            elif path.startswith("/api/owner/accounts/") and path.endswith("/status"):
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                aid=int(path.split("/")[4]);self.js(200,{"status":"updated","item":self.safe(saas.set_account_status,aid,d.get("status"))})
            elif path=="/api/owner-cloud/register":
                self.me("settings.manage");self.js(200,self.safe(owner_cloud.register))
            elif path=="/api/owner-cloud/pairing-code":
                self.me("settings.manage");self.js(200,self.safe(owner_cloud.new_pairing_code))
            elif path=="/api/owner-cloud/sync":
                self.me("settings.manage");self.js(200,self.safe(owner_cloud.sync_now))
            elif path=="/api/system/request-database-switch":
                if WEB_MODE:
                    raise E(400,"Versi Web menggunakan database server yang dikelola melalui storage/volume deployment.")
                global DATABASE_SWITCH_REQUESTED, ACTIVE_SERVER
                DATABASE_SWITCH_REQUESTED = True
                self.js(200,{"status":"switching","database":str(DB_PATH)})
                if ACTIVE_SERVER is not None:
                    threading.Thread(target=ACTIVE_SERVER.shutdown,daemon=True).start()
            elif path=="/api/session/ping":
                if not repo.heartbeat(self.token()):raise E(401,"Sesi tidak aktif.")
                self.js(200,{"status":"active"})
            elif path=="/api/active-sessions/force-logout":
                self.me("users.manage")
                if not repo.force_logout_session(str(d.get("session_id","") or "")):raise E(404,"Sesi tidak ditemukan.")
                self.js(200,{"status":"logged_out"})
            elif path=="/api/logout":
                repo.logout(self.token());self.js(200,{"status":"logged_out"})
            elif path=="/api/subscription-admin/activate":
                u=self.me(); self.js(200,self.safe(repo.subscription_admin_activate,u,d,self.client_address[0]))
            elif path=="/api/subscription-admin/reset-trial":
                u=self.me(); self.js(200,self.safe(repo.subscription_admin_reset_trial,u,self.client_address[0],d.get("admin_key")))
            elif path=="/api/login":
                r=repo.login(str(d.get("username","")),str(d.get("password","")),self.client_address[0],str(d.get("client_name","browser")),str(d.get("device_id","") or ""),self.headers.get("User-Agent",""))
                if not r:raise E(401,"Username atau password salah.")
                self.js(200,r)
            elif path=="/api/bank-import/pdf-preview":self.js(201,{"result":self.safe(repo.preview_bank_pdf,self.me("cash.manage"),str(d.get("pdf_base64","")),str(d.get("file_name","rekening_koran.pdf")))})
            elif path=="/api/bank-import/preview":self.js(201,{"result":self.safe(repo.preview_bank_csv,self.me("cash.manage"),str(d.get("csv_text","")),str(d.get("file_name","rekening.csv")),d.get("bank_name"))})
            elif path=="/api/bank-import/post":self.js(201,{"result":self.safe(repo.post_bank_import,self.me("cash.manage"),d.get("batch_id"),d.get("cash_account_id"),d.get("mappings",[]),self.client_address[0])})
            elif path=="/api/coa-template-apply":self.js(201,{"status":"created","result":self.safe(coa_templates.apply_template,self.me("accounting.manage"),str(d.get("template","")),self.client_address[0])})
            elif path=="/api/coa":self.js(201,{"status":"created","id":self.safe(repo.create_coa,self.me("accounting.manage"),d,self.client_address[0])})

            elif path=="/api/master-import":
                self.js(201,{"result":self.safe(excel_import.import_excel,self.me("inventory.manage"),str(d.get("type","")),str(d.get("excel_base64","")),str(d.get("file_name","import.xlsx")),self.client_address[0])})
            elif path=="/api/sales/import-excel":
                self.js(201,{"result":self.safe(repo.import_sales_excel,self.me("sales.manage"),
                  str(d.get("excel_base64","")),str(d.get("file_name","sales.xlsx")),self.client_address[0])})
            elif path=="/api/purchases/import-excel":
                self.js(201,{"result":self.safe(repo.import_purchase_excel,self.me("purchases.manage"),
                  str(d.get("excel_base64","")),str(d.get("file_name","purchase.xlsx")),self.client_address[0])})
            elif path=="/api/cash-transactions/import-excel":
                self.js(201,{"result":self.safe(repo.import_cash_excel,self.me("cash.manage"),
                  str(d.get("excel_base64","")),str(d.get("file_name","cash.xlsx")),self.client_address[0])})
            elif path=="/api/manual-journals/import-excel":
                self.js(201,{"status":"created","result":self.safe(
                  repo.import_manual_journal_excel,self.me("accounting.manage"),
                  str(d.get("excel_base64","")),str(d.get("file_name","jurnal.xlsx")),
                  self.client_address[0])})
            elif path=="/api/manual-journals":self.js(201,{"status":"created","result":self.safe(repo.create_manual_journal,self.me("accounting.manage"),d,self.client_address[0])})
            elif path=="/api/receivable-payments":self.js(201,{"status":"created","result":self.safe(repo.receive_receivable,self.me("receivables.manage"),d,self.client_address[0])})
            elif path=="/api/payable-payments":self.js(201,{"status":"created","result":self.safe(repo.pay_payable,self.me("payables.manage"),d,self.client_address[0])})
            elif path=="/api/price-levels":self.js(201,{"status":"created","id":self.safe(repo.create_price_level,self.me("partners.manage"),d,self.client_address[0])})
            elif path=="/api/brands":self.js(201,{"status":"created","id":self.safe(repo.create_brand,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/salespersons":self.js(201,{"status":"created","id":self.safe(repo.create_salesperson,self.me("partners.manage"),d,self.client_address[0])})
            elif path.startswith("/api/users/") and path.endswith("/reset-password"):
                user_id=int(path.split("/")[3])
                self.safe(repo.reset_user_password,self.me("users.manage"),user_id,
                  str(d.get("password","")),self.client_address[0])
                self.js(200,{"status":"password_reset"})
            elif path=="/api/roles":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_role,self.me("users.manage"),d,self.client_address[0])})
            elif path=="/api/users":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_user,self.me("users.manage"),d,self.client_address[0])})
            elif path=="/api/fixed-assets/depreciate":self.js(201,{"result":self.safe(repo.run_fixed_asset_depreciation,self.me("accounting.manage"),d.get("period"),self.client_address[0])})
            elif path=="/api/fixed-assets":self.js(201,{"status":"created","id":self.safe(repo.create_fixed_asset,self.me("accounting.manage"),d,self.client_address[0])})
            elif path=="/api/partners":self.js(201,{"status":"created","id":self.safe(repo.create_partner,self.me("partners.manage"),d,self.client_address[0])})
            elif path=="/api/warehouses":self.js(201,{"status":"created","id":self.safe(repo.create_warehouse,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/inventory-transfers":self.js(201,{"status":"created","result":self.safe(repo.transfer_stock,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/departments":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_department,self.me("departments.manage"),d,self.client_address[0])})
            elif path=="/api/projects":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_project,self.me("projects.manage"),d,self.client_address[0])})
            elif path=="/api/assemblies":self.js(201,{"status":"created","result":self.safe(repo.create_assembly,self.me("inventory.manage"),d,self.client_address[0])})
            elif path.startswith("/api/assemblies/") and path.endswith("/finish"):
                aid=int(path.split("/")[3]);self.js(201,{"status":"finished","result":self.safe(repo.finish_assembly,self.me("inventory.manage"),aid,d,self.client_address[0])})
            elif path=="/api/flexible-invoice-templates":
                item=self.safe(repo.save_flexible_invoice_template,self.me("settings.manage"),d,self.client_address[0]);self.js(201,{"status":"created","item":item})
            elif path=="/api/project-documents":
                self.js(201,{"status":"created","id":self.safe(repo.save_project_document,self.me("projects.manage"),d,self.client_address[0])})
            elif path=="/api/project-progress": self.js(201,{"status":"created","id":self.safe(repo.save_project_progress,self.me("projects.manage"),d,self.client_address[0])})
            elif path=="/api/project-terms": self.js(201,{"status":"created","id":self.safe(repo.save_project_term,self.me("projects.manage"),d,self.client_address[0])})
            elif path=="/api/project-material-issues":
                self.js(201,{"status":"created","result":self.safe(
                  repo.create_project_material_issue,self.me("inventory.manage"),
                  d,self.client_address[0])})
            elif path=="/api/project-budgets":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_project_budget,self.me("projects.manage"),d,self.client_address[0])})
            elif path=="/api/service-categories":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_service_category,self.me("services.manage"),
                  d,self.client_address[0])})
            elif path=="/api/services":
                self.js(201,{"status":"created","id":self.safe(
                  repo.create_service,self.me("services.manage"),
                  d,self.client_address[0])})
            elif path=="/api/categories":self.js(201,{"status":"created","id":self.safe(repo.create_category,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/units":self.js(201,{"status":"created","id":self.safe(repo.create_unit,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/products":self.js(201,{"status":"created","id":self.safe(repo.create_product,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/stock-adjustments":self.js(201,{"status":"created","result":self.safe(repo.adjust_stock,self.me("inventory.manage"),d,self.client_address[0])})
            elif path=="/api/cash-accounts":self.js(201,{"status":"created","id":self.safe(repo.create_cash_account,self.me("cash.manage"),d,self.client_address[0])})
            elif path=="/api/cash-transactions":self.js(201,{"status":"created","result":self.safe(repo.create_cash_transaction,self.me("cash.manage"),d,self.client_address[0])})
            elif path=="/api/cash-transfers":self.js(201,{"status":"created","result":self.safe(repo.create_cash_transfer,self.me("cash.manage"),d,self.client_address[0])})
            elif path=="/api/sales-orders":self.js(201,{"status":"created","result":self.safe(order_dp.create_order,self.me("sales.manage"),d,self.client_address[0],"sales")})
            elif path=="/api/purchase-orders":self.js(201,{"status":"created","result":self.safe(order_dp.create_order,self.me("purchases.manage"),d,self.client_address[0],"purchase")})
            elif path=="/api/customer-downpayments":self.js(201,{"status":"created","result":self.safe(order_dp.create_dp,self.me("receivables.manage"),d,self.client_address[0],"customer")})
            elif path=="/api/supplier-downpayments":self.js(201,{"status":"created","result":self.safe(order_dp.create_dp,self.me("payables.manage"),d,self.client_address[0],"supplier")})
            elif path=="/api/customer-downpayment-allocations":self.js(201,{"status":"created","result":self.safe(order_dp.allocate_dp,self.me("receivables.manage"),d,self.client_address[0],"customer")})
            elif path=="/api/supplier-downpayment-allocations":self.js(201,{"status":"created","result":self.safe(order_dp.allocate_dp,self.me("payables.manage"),d,self.client_address[0],"supplier")})
            elif path=="/api/purchase-returns":self.js(201,{"status":"created","result":self.safe(repo.create_purchase_return,self.me("purchases.manage"),d,self.client_address[0])})
            elif path=="/api/sales-returns":self.js(201,{"status":"created","result":self.safe(repo.create_sales_return,self.me("sales.manage"),d,self.client_address[0])})
            elif path=="/api/purchases":self.js(201,{"status":"created","result":self.safe(repo.create_purchase,self.me("purchases.manage"),d,self.client_address[0])})
            elif path=="/api/sales":self.js(201,{"status":"created","result":self.safe(repo.create_sale,self.me("sales.manage"),d,self.client_address[0])})
            else:raise E(404,"Endpoint tidak ditemukan.")
        except E as e:self.js(e.s,{"error":e.m})
        except Exception:
            ref=uuid.uuid4().hex[:8].upper();log.exception("POST gagal [%s]",ref)
            self.js(500,{"error":f"Kesalahan internal server. Referensi: {ref}"})
    def do_PUT(self):
        try:
            path=urlparse(self.path).path
            if path=="/api/owner-cloud/settings":self.js(200,self.safe(owner_cloud.save_settings,self.me("settings.manage") and self.body()))
            elif path=="/api/company-profile":self.safe(repo.update_company_profile,self.me("settings.manage"),self.body(),self.client_address[0]);self.js(200,{"status":"updated"})
            elif path.startswith("/api/document-templates/"):
                item=self.safe(repo.update_document_template,self.me("settings.manage"),
                  path.rsplit("/",1)[1],self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/flexible-invoice-templates/"):
                item=self.safe(repo.save_flexible_invoice_template,self.me("settings.manage"),self.body(),self.client_address[0],int(path.rsplit("/",1)[1]))
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/coa/"):
                self.js(200,{"status":"updated","id":self.safe(repo.update_coa,self.me("accounting.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])})
            elif path.startswith("/api/roles/"):
                item=self.safe(repo.update_role,self.me("users.manage"),
                  path.rsplit("/",1)[1],self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/users/"):
                item=self.safe(repo.update_user,self.me("users.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/departments/"):
                item=self.safe(repo.update_department,self.me("departments.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/projects/"):
                item=self.safe(repo.update_project,self.me("projects.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/assemblies/") and path.endswith("/finish"):
                aid=int(path.split("/")[3]);item=self.safe(repo.update_assembly_finish,self.me("inventory.manage"),aid,self.body(),self.client_address[0]);self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/assemblies/"):
                aid=int(path.rsplit("/",1)[1]);item=self.safe(repo.update_assembly,self.me("inventory.manage"),aid,self.body(),self.client_address[0]);self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/project-documents/"):
                item=self.safe(repo.save_project_document,self.me("projects.manage"),self.body(),self.client_address[0],int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","id":item})
            elif path.startswith("/api/project-progress/"):
                item=self.safe(repo.save_project_progress,self.me("projects.manage"),self.body(),self.client_address[0],int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","id":item})
            elif path.startswith("/api/project-terms/"):
                item=self.safe(repo.save_project_term,self.me("projects.manage"),self.body(),self.client_address[0],int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","id":item})
            elif path.startswith("/api/project-budgets/"):
                item=self.safe(repo.update_project_budget,self.me("projects.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/service-categories/"):
                item=self.safe(repo.update_service_category,self.me("services.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/services/"):
                item=self.safe(repo.update_service,self.me("services.manage"),
                  int(path.rsplit("/",1)[1]),self.body(),self.client_address[0])
                self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/project-material-issues/"):
                issue_id=int(path.rsplit("/",1)[1])
                result=self.safe(repo.update_project_material_issue,self.me("inventory.manage"),issue_id,self.body(),self.client_address[0])
                self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/fixed-assets/"):
                asset_id=int(path.rsplit("/",1)[1])
                item=self.safe(repo.update_fixed_asset,self.me("accounting.manage"),asset_id,self.body(),self.client_address[0]);self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/purchase-returns/"):
                result=self.safe(repo.update_purchase_return,self.me("purchases.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/sales-returns/"):
                result=self.safe(repo.update_sales_return,self.me("sales.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/transaction-maintenance/"):
                parts=path.strip("/").split("/");kind=parts[2];key=parts[3]
                perm={"cash":"cash.manage","transfer":"cash.manage","journal":"accounting.manage","adjustment":"inventory.manage","receivable":"receivables.manage","payable":"payables.manage","warehouse_transfer":"inventory.manage"}[kind]
                result=self.safe(repo.update_transaction_maintenance,self.me(perm),kind,key,self.body(),self.client_address[0])
                self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/departments/"): self.safe(repo.delete_department,self.me("departments.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/sales/"):
                result=self.safe(repo.update_sale,self.me("sales.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/purchases/"):
                result=self.safe(repo.update_purchase,self.me("purchases.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/sales-orders/"):
                result=self.safe(order_dp.update_order,self.me("sales.manage"),self.body(),self.client_address[0],"sales",int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/purchase-orders/"):
                result=self.safe(order_dp.update_order,self.me("purchases.manage"),self.body(),self.client_address[0],"purchase",int(path.rsplit("/",1)[1]));self.js(200,{"status":"updated","result":result})
            elif path.startswith("/api/price-levels/"):
                self.safe(repo.update_price_level,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated"})
            elif path.startswith("/api/price-levels/"):
                self.safe(repo.delete_price_level,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted"})
            elif path.startswith("/api/warehouses/"):
                item=self.safe(repo.update_warehouse,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated","item":item})
            elif path.startswith("/api/brands/"): self.safe(repo.update_brand,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]); self.js(200,{"status":"updated"})
            elif path.startswith("/api/salespersons/"): self.safe(repo.update_salesperson,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]); self.js(200,{"status":"updated"})
            elif path.startswith("/api/categories/"): self.safe(repo.update_category,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]); self.js(200,{"status":"updated"})
            elif path.startswith("/api/units/"): self.safe(repo.update_unit,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]); self.js(200,{"status":"updated"})
            elif path.startswith("/api/partners/"):self.safe(repo.update_partner,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated"})
            elif path.startswith("/api/products/"):self.safe(repo.update_product,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.body(),self.client_address[0]);self.js(200,{"status":"updated"})
            else:raise E(404,"Endpoint tidak ditemukan.")
        except E as e:self.js(e.s,{"error":e.m})
        except Exception:
            ref=uuid.uuid4().hex[:8].upper();log.exception("PUT gagal [%s]",ref)
            self.js(500,{"error":f"Kesalahan internal server. Referensi: {ref}"})
    def do_DELETE(self):
        try:
            path=urlparse(self.path).path
            if path.startswith("/api/owner/discounts/"):
                if not saas.owner_authenticated(self.token()): raise E(401,"Sesi Owner Admin tidak valid.")
                self.safe(saas.delete_discount,path.rsplit("/",1)[1]);self.js(200,{"status":"deleted"});return
            elif path.startswith("/api/coa/"):
                self.js(200,self.safe(repo.delete_coa,self.me("accounting.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]))
            elif False: pass
            if path.startswith("/api/assemblies/") and path.endswith("/finish"):
                aid=int(path.split("/")[3]);self.js(200,{"status":"deleted","result":self.safe(repo.delete_assembly_finish,self.me("inventory.manage"),aid,self.client_address[0])})
            elif path.startswith("/api/assemblies/"):
                aid=int(path.rsplit("/",1)[1]);self.js(200,{"status":"deleted","result":self.safe(repo.delete_assembly,self.me("inventory.manage"),aid,self.client_address[0])})
            elif path.startswith("/api/sales/"):

                self.js(200,{"status":"deleted","result":self.safe(repo.delete_sale,self.me("sales.manage"),int(path.rsplit("/",1)[1]),self.client_address[0])})
            elif path.startswith("/api/purchases/"):
                self.js(200,{"status":"deleted","result":self.safe(repo.delete_purchase,self.me("purchases.manage"),int(path.rsplit("/",1)[1]),self.client_address[0])})
            elif path.startswith("/api/sales-orders/"):
                self.safe(order_dp.delete_order,self.me("sales.manage"),"sales",int(path.rsplit("/",1)[1]));self.js(200,{"status":"deleted"})
            elif path.startswith("/api/purchase-orders/"):
                self.safe(order_dp.delete_order,self.me("purchases.manage"),"purchase",int(path.rsplit("/",1)[1]));self.js(200,{"status":"deleted"})
            elif path.startswith("/api/customer-downpayments/"):
                result=self.safe(order_dp.delete_dp,self.me("receivables.manage"),"customer",int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/supplier-downpayments/"):
                result=self.safe(order_dp.delete_dp,self.me("payables.manage"),"supplier",int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/customer-downpayment-allocations/"):
                result=self.safe(order_dp.delete_allocation,self.me("receivables.manage"),"customer",int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/supplier-downpayment-allocations/"):
                result=self.safe(order_dp.delete_allocation,self.me("payables.manage"),"supplier",int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/service-categories/"):
                self.safe(repo.delete_service_category,self.me("services.manage"),
                  int(path.rsplit("/",1)[1]),self.client_address[0])
                self.js(200,{"status":"deleted"})
            elif path.startswith("/api/services/"):
                self.safe(repo.delete_service,self.me("services.manage"),
                  int(path.rsplit("/",1)[1]),self.client_address[0])
                self.js(200,{"status":"deleted"})
            elif path.startswith("/api/flexible-invoice-templates/"):
                self.safe(repo.delete_flexible_invoice_template,self.me("settings.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted"})
            elif path.startswith("/api/project-documents/"):
                self.safe(repo.delete_project_document,self.me("projects.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted"})
            elif path.startswith("/api/project-progress/"):
                self.safe(repo.delete_project_progress,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted"})
            elif path.startswith("/api/project-terms/"):
                self.safe(repo.delete_project_term,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted"})
            elif path.startswith("/api/project-budgets/"):
                self.safe(repo.delete_project_budget,self.me("inventory.manage"),
                  int(path.rsplit("/",1)[1]),self.client_address[0])
                self.js(200,{"status":"deleted"})
            elif path.startswith("/api/project-material-issues/"):
                issue_id=int(path.rsplit("/",1)[1])
                self.js(200,{"status":"deleted","result":self.safe(repo.delete_project_material_issue,self.me("inventory.manage"),issue_id,self.client_address[0])})
            elif path.startswith("/api/purchase-returns/"):
                result=self.safe(repo.delete_purchase_return,self.me("purchases.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/sales-returns/"):
                result=self.safe(repo.delete_sales_return,self.me("sales.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/transaction-maintenance/"):
                parts=path.strip("/").split("/");kind=parts[2];key=parts[3]
                perm={"cash":"cash.manage","transfer":"cash.manage","journal":"accounting.manage","adjustment":"inventory.manage","receivable":"receivables.manage","payable":"payables.manage","warehouse_transfer":"inventory.manage"}[kind]
                result=self.safe(repo.delete_transaction_maintenance,self.me(perm),kind,key,self.client_address[0],"Dihapus dari daftar transaksi")
                self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/departments/"): self.safe(repo.delete_department,self.me("departments.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/warehouses/"):
                result=self.safe(repo.delete_warehouse,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]);self.js(200,{"status":"deleted","result":result})
            elif path.startswith("/api/brands/"): self.safe(repo.delete_brand,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/salespersons/"): self.safe(repo.delete_salesperson,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/categories/"): self.safe(repo.delete_category,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/units/"): self.safe(repo.delete_unit,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/partners/"): self.safe(repo.delete_partner,self.me("partners.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/products/"): self.safe(repo.delete_product,self.me("inventory.manage"),int(path.rsplit("/",1)[1]),self.client_address[0]); self.js(200,{"status":"deleted"})
            elif path.startswith("/api/fixed-assets/depreciations/"):
                dep_id=int(path.rsplit("/",1)[1])
                self.js(200,{"status":"deleted","result":self.safe(repo.delete_fixed_asset_depreciation,self.me("accounting.manage"),dep_id,self.client_address[0])})
            elif path.startswith("/api/fixed-assets/"):
                asset_id=int(path.rsplit("/",1)[1])
                self.js(200,{"status":"deleted","result":self.safe(repo.delete_fixed_asset,self.me("accounting.manage"),asset_id,self.client_address[0])})
            else:raise E(404,"Endpoint tidak ditemukan.")
        except E as e:self.js(e.s,{"error":e.m})
        except Exception:
            ref=uuid.uuid4().hex[:8].upper();log.exception("DELETE gagal [%s]",ref)
            self.js(500,{"error":f"Kesalahan internal server. Referensi: {ref}"})
def run():
    global DATABASE_SWITCH_REQUESTED, ACTIVE_SERVER
    DATABASE_SWITCH_REQUESTED = False
    init_database()
    if IS_POSTGRES:
        try: saas.ensure_schema()
        except Exception: log.exception("Inisialisasi platform SaaS gagal"); raise
    try: repo.close_prior_fiscal_years()
    except Exception: log.exception("Penutupan otomatis tahun buku gagal")
    try: log.info("Core non-inventory repair: %s",repo.reconcile_core_linkages())
    except Exception: log.exception("Repair inti non-persediaan gagal")
    try: log.info("Legacy sale void valuation repair: %s",repo.repair_legacy_sale_void_valuation())
    except Exception: log.exception("Repair pembatalan penjualan lama gagal")
    try: log.info("Legacy opening edit in-place repair: %s",repo.repair_legacy_opening_edit_rows())
    except Exception: log.exception("Legacy opening edit in-place repair failed")
    try: log.info("Inventory valuation replay: %s",repo.rebuild_inventory_valuation_state())
    except Exception: log.exception("Rebuild nilai persediaan dari mutasi gagal")
    try: log.info("Inventory transaction integrity: %s",repo.enforce_inventory_transaction_integrity())
    except Exception: log.exception("Sinkronisasi persediaan berbasis transaksi gagal")
    try: log.info("Inventory GL source sync: %s",repo.sync_inventory_gl_by_source())
    except Exception: log.exception("Sinkronisasi GL persediaan per sumber gagal")
    s=ThreadingHTTPServer((HOST,PORT),H)
    ACTIVE_SERVER=s
    log.info("Server v%s berjalan di http://%s:%s dengan backend database %s",VERSION,HOST,PORT,DATABASE_BACKEND)
    try:s.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        ACTIVE_SERVER=None
        s.server_close()
        try:
            backup_path=backup_database()
            if backup_path:log.info("Backup otomatis tersimpan: %s",backup_path)
        except Exception:
            log.exception("Backup otomatis saat aplikasi ditutup gagal")
    return DATABASE_SWITCH_REQUESTED
if __name__=="__main__":run()
