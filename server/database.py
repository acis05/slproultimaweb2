import sqlite3, threading, os
from datetime import datetime
from contextlib import contextmanager
from .config import DB_PATH, BACKUP_DIR, DATABASE_URL, IS_POSTGRES
from .security import hash_password, utc_now
from .db_migration import prepare_legacy_schema, migrate_legacy_data
from . import pg_compat
from . import subscription

WRITE_LOCK = threading.RLock()
DB_OPERATIONAL_ERRORS = (sqlite3.OperationalError, pg_compat.OperationalError)
DB_INTEGRITY_ERRORS = (sqlite3.IntegrityError, pg_compat.IntegrityError)

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
PRAGMA busy_timeout=10000;

CREATE TABLE IF NOT EXISTS owner_cloud_settings(id INTEGER PRIMARY KEY CHECK(id=1),cloud_url TEXT NOT NULL DEFAULT '',enabled INTEGER NOT NULL DEFAULT 0,sync_interval_minutes INTEGER NOT NULL DEFAULT 5,company_id TEXT,installation_id TEXT,client_secret TEXT,pairing_code TEXT,pairing_expires_at TEXT,last_sync_at TEXT,last_sync_status TEXT,last_error TEXT,updated_at TEXT);
CREATE TABLE IF NOT EXISTS owner_cloud_sync_logs(id INTEGER PRIMARY KEY AUTOINCREMENT,status TEXT NOT NULL,message TEXT,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS roles(
 id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE NOT NULL,
 name TEXT NOT NULL, permissions_json TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE COLLATE NOCASE NOT NULL,
 full_name TEXT NOT NULL, password_hash TEXT NOT NULL, role_id INTEGER NOT NULL,
 is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
 FOREIGN KEY(role_id) REFERENCES roles(id));
CREATE TABLE IF NOT EXISTS sessions(
 token TEXT PRIMARY KEY, user_id INTEGER NOT NULL, client_ip TEXT, client_name TEXT,
 created_at TEXT NOT NULL, expires_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
 FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS audit_logs(
 id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT NOT NULL,
 entity_type TEXT, entity_id TEXT, details_json TEXT NOT NULL DEFAULT '{}',
 client_ip TEXT, created_at TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));


CREATE TABLE IF NOT EXISTS company_profile(
 id INTEGER PRIMARY KEY CHECK(id=1),
 company_name TEXT NOT NULL DEFAULT 'Perusahaan Saya',
 address TEXT, city TEXT, phone TEXT, email TEXT, tax_id TEXT,
 website TEXT, logo_path TEXT, logo_content BLOB, logo_mime TEXT,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS brands(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS salespersons(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 phone TEXT, email TEXT,
 commission_percent NUMERIC NOT NULL DEFAULT 0 CHECK(commission_percent>=0),
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_brands_name ON brands(name);
CREATE INDEX IF NOT EXISTS idx_salespersons_name ON salespersons(name);


CREATE TABLE IF NOT EXISTS departments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL UNIQUE COLLATE NOCASE,
  name TEXT NOT NULL,
  manager_name TEXT,
  notes TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL UNIQUE COLLATE NOCASE,
  name TEXT NOT NULL,
  customer_id INTEGER,
  start_date TEXT,
  end_date TEXT,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  notes TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES business_partners(id)
);



CREATE TABLE IF NOT EXISTS project_progress(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL,
  progress_date TEXT NOT NULL,
  progress_percent NUMERIC NOT NULL DEFAULT 0 CHECK(progress_percent>=0 AND progress_percent<=100),
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_project_progress_project_date ON project_progress(project_id,progress_date);

CREATE TABLE IF NOT EXISTS project_terms(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL,
  term_no TEXT NOT NULL,
  description TEXT,
  percentage NUMERIC NOT NULL DEFAULT 0 CHECK(percentage>=0),
  amount NUMERIC NOT NULL DEFAULT 0 CHECK(amount>=0),
  invoice_date TEXT,
  due_date TEXT,
  sale_id INTEGER,
  status TEXT NOT NULL DEFAULT 'DRAFT' CHECK(status IN ('DRAFT','BILLED','PARTIAL','PAID','CANCELLED')),
  retention_percent NUMERIC NOT NULL DEFAULT 0 CHECK(retention_percent>=0),
  retention_amount NUMERIC NOT NULL DEFAULT 0 CHECK(retention_amount>=0),
  retention_due_date TEXT,
  retention_status TEXT NOT NULL DEFAULT 'PENDING' CHECK(retention_status IN ('PENDING','RELEASED','CANCELLED')),
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(project_id,term_no),
  FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY(sale_id) REFERENCES sales(id)
);
CREATE INDEX IF NOT EXISTS idx_project_terms_project ON project_terms(project_id);


CREATE TABLE IF NOT EXISTS project_documents(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL,
  category TEXT NOT NULL DEFAULT 'LAIN-LAIN',
  title TEXT NOT NULL,
  document_no TEXT,
  document_date TEXT,
  valid_until TEXT,
  description TEXT,
  original_filename TEXT NOT NULL,
  stored_filename TEXT NOT NULL,
  relative_path TEXT NOT NULL,
  mime_type TEXT,
  file_size INTEGER NOT NULL DEFAULT 0,
  file_content BLOB,
  version_no INTEGER NOT NULL DEFAULT 1,
  replaces_id INTEGER,
  is_current INTEGER NOT NULL DEFAULT 1,
  uploaded_by INTEGER,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY(replaces_id) REFERENCES project_documents(id),
  FOREIGN KEY(uploaded_by) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS idx_project_documents_project ON project_documents(project_id,is_current,category,document_date);
CREATE INDEX IF NOT EXISTS idx_project_documents_replace ON project_documents(replaces_id);


CREATE TABLE IF NOT EXISTS flexible_invoice_templates(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL UNIQUE COLLATE NOCASE,
  name TEXT NOT NULL,
  template_kind TEXT NOT NULL DEFAULT 'STANDARD',
  blocks_json TEXT NOT NULL,
  options_json TEXT NOT NULL,
  is_default INTEGER NOT NULL DEFAULT 0,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_flexible_invoice_templates_active ON flexible_invoice_templates(is_active,is_default,name);

CREATE TABLE IF NOT EXISTS sale_invoice_materials(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
  project_material_issue_id INTEGER, product_id INTEGER, sku TEXT,
  material_name TEXT NOT NULL, qty REAL NOT NULL DEFAULT 0, unit_code TEXT,
  unit_cost REAL NOT NULL DEFAULT 0, total_cost REAL NOT NULL DEFAULT 0,
  issue_date TEXT, issue_no TEXT, sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_sale_invoice_materials_sale ON sale_invoice_materials(sale_id,sort_order,id);

CREATE TABLE IF NOT EXISTS project_budgets(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL UNIQUE,
  material_budget NUMERIC NOT NULL DEFAULT 0 CHECK(material_budget>=0),
  expense_budget NUMERIC NOT NULL DEFAULT 0 CHECK(expense_budget>=0),
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_project_budgets_project
  ON project_budgets(project_id);

CREATE TABLE IF NOT EXISTS project_material_issues(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
  issue_date TEXT NOT NULL,
  project_id INTEGER NOT NULL,
  department_id INTEGER,
  warehouse_id INTEGER NOT NULL,
  expense_account_id INTEGER NOT NULL,
  notes TEXT,
  status TEXT NOT NULL DEFAULT 'POSTED' CHECK(status IN ('POSTED','VOID')),
  total_cost NUMERIC NOT NULL DEFAULT 0 CHECK(total_cost>=0),
  user_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(id),
  FOREIGN KEY(department_id) REFERENCES departments(id),
  FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
  FOREIGN KEY(expense_account_id) REFERENCES chart_of_accounts(id),
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS project_material_issue_items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  issue_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  qty NUMERIC NOT NULL CHECK(qty>0),
  average_cost NUMERIC NOT NULL DEFAULT 0 CHECK(average_cost>=0),
  total_cost NUMERIC NOT NULL DEFAULT 0 CHECK(total_cost>=0),
  inventory_transaction_id INTEGER,
  FOREIGN KEY(issue_id) REFERENCES project_material_issues(id) ON DELETE CASCADE,
  FOREIGN KEY(product_id) REFERENCES products(id),
  FOREIGN KEY(inventory_transaction_id) REFERENCES inventory_transactions(id)
);

CREATE INDEX IF NOT EXISTS idx_project_material_issues_project
  ON project_material_issues(project_id,issue_date,id);
CREATE INDEX IF NOT EXISTS idx_project_material_issue_items_issue
  ON project_material_issue_items(issue_id);

CREATE TABLE IF NOT EXISTS assembly_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 assembly_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 assembly_date TEXT NOT NULL,
 warehouse_id INTEGER NOT NULL,
 wip_account_id INTEGER NOT NULL,
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('OPEN','FINISHED','VOID')),
 material_cost NUMERIC NOT NULL DEFAULT 0,
 additional_cost NUMERIC NOT NULL DEFAULT 0,
 total_cost NUMERIC NOT NULL DEFAULT 0,
 user_id INTEGER NOT NULL,
 finished_at TEXT,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
 FOREIGN KEY(wip_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS assembly_materials(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 assembly_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 qty NUMERIC NOT NULL CHECK(qty>0),
 unit_cost NUMERIC NOT NULL DEFAULT 0,
 total_cost NUMERIC NOT NULL DEFAULT 0,
 inventory_transaction_id INTEGER,
 FOREIGN KEY(assembly_id) REFERENCES assembly_orders(id) ON DELETE CASCADE,
 FOREIGN KEY(product_id) REFERENCES products(id),
 FOREIGN KEY(inventory_transaction_id) REFERENCES inventory_transactions(id)
);
CREATE TABLE IF NOT EXISTS assembly_costs(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 assembly_id INTEGER NOT NULL,
 account_id INTEGER NOT NULL,
 description TEXT NOT NULL,
 amount NUMERIC NOT NULL CHECK(amount>0),
 FOREIGN KEY(assembly_id) REFERENCES assembly_orders(id) ON DELETE CASCADE,
 FOREIGN KEY(account_id) REFERENCES chart_of_accounts(id)
);
CREATE TABLE IF NOT EXISTS assembly_outputs(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 assembly_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 qty NUMERIC NOT NULL CHECK(qty>0),
 allocation_percent NUMERIC NOT NULL CHECK(allocation_percent>=0),
 allocated_cost NUMERIC NOT NULL DEFAULT 0,
 unit_cost NUMERIC NOT NULL DEFAULT 0,
 inventory_transaction_id INTEGER,
 FOREIGN KEY(assembly_id) REFERENCES assembly_orders(id) ON DELETE CASCADE,
 FOREIGN KEY(product_id) REFERENCES products(id),
 FOREIGN KEY(inventory_transaction_id) REFERENCES inventory_transactions(id)
);
CREATE INDEX IF NOT EXISTS idx_assembly_orders_date ON assembly_orders(assembly_date,status,id);
CREATE INDEX IF NOT EXISTS idx_assembly_materials_order ON assembly_materials(assembly_id);
CREATE INDEX IF NOT EXISTS idx_assembly_outputs_order ON assembly_outputs(assembly_id);

CREATE TABLE IF NOT EXISTS item_categories(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS units(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 decimals INTEGER NOT NULL DEFAULT 0 CHECK(decimals BETWEEN 0 AND 4),
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);


CREATE TABLE IF NOT EXISTS service_categories(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 notes TEXT,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS services(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 service_code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 service_name TEXT NOT NULL,
 category_id INTEGER,
 unit_id INTEGER NOT NULL,
 purchase_price NUMERIC NOT NULL DEFAULT 0 CHECK(purchase_price>=0),
 selling_price NUMERIC NOT NULL DEFAULT 0 CHECK(selling_price>=0),
 tax_percent NUMERIC NOT NULL DEFAULT 0 CHECK(tax_percent>=0 AND tax_percent<=100),
 purchase_account_id INTEGER NOT NULL,
 sales_account_id INTEGER NOT NULL,
 product_id INTEGER UNIQUE,
 notes TEXT,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(category_id) REFERENCES service_categories(id),
 FOREIGN KEY(unit_id) REFERENCES units(id),
 FOREIGN KEY(purchase_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(sales_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE INDEX IF NOT EXISTS idx_services_name ON services(service_name);
CREATE INDEX IF NOT EXISTS idx_services_category ON services(category_id,is_active);

CREATE TABLE IF NOT EXISTS products(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 sku TEXT NOT NULL UNIQUE COLLATE NOCASE,
 barcode TEXT UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 category_id INTEGER,
 unit_id INTEGER NOT NULL,
 product_type TEXT NOT NULL DEFAULT 'STOCK' CHECK(product_type IN ('STOCK','SERVICE')),
 purchase_price NUMERIC NOT NULL DEFAULT 0 CHECK(purchase_price >= 0),
 selling_price NUMERIC NOT NULL DEFAULT 0 CHECK(selling_price >= 0),
 stock_qty NUMERIC NOT NULL DEFAULT 0,
 minimum_stock NUMERIC NOT NULL DEFAULT 0 CHECK(minimum_stock >= 0),
 notes TEXT,
 inventory_account_id INTEGER,
 sales_account_id INTEGER,
 cogs_account_id INTEGER,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(category_id) REFERENCES item_categories(id),
 FOREIGN KEY(unit_id) REFERENCES units(id));

CREATE TABLE IF NOT EXISTS product_units(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 unit_id INTEGER NOT NULL,
 conversion_ratio NUMERIC NOT NULL CHECK(conversion_ratio>0),
 purchase_price NUMERIC NOT NULL DEFAULT 0,
 selling_price NUMERIC NOT NULL DEFAULT 0,
 is_base INTEGER NOT NULL DEFAULT 0,
 is_active INTEGER NOT NULL DEFAULT 1,
 UNIQUE(product_id,unit_id),
 FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
 FOREIGN KEY(unit_id) REFERENCES units(id));
CREATE INDEX IF NOT EXISTS idx_product_units_product ON product_units(product_id,is_active);

CREATE TABLE IF NOT EXISTS stock_movements(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 movement_type TEXT NOT NULL,
 qty_change NUMERIC NOT NULL,
 qty_before NUMERIC NOT NULL,
 qty_after NUMERIC NOT NULL,
 reference_no TEXT,
 reason TEXT NOT NULL,
 department_id INTEGER,
 project_id INTEGER,
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 FOREIGN KEY(product_id) REFERENCES products(id),
 FOREIGN KEY(user_id) REFERENCES users(id));


CREATE TABLE IF NOT EXISTS business_partners(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 partner_type TEXT NOT NULL CHECK(partner_type IN ('CUSTOMER','SUPPLIER','BOTH')),
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 tax_id TEXT,
 phone TEXT,
 email TEXT,
 address TEXT,
 city TEXT,
 credit_limit NUMERIC NOT NULL DEFAULT 0 CHECK(credit_limit >= 0),
 payment_term_days INTEGER NOT NULL DEFAULT 0 CHECK(payment_term_days >= 0),
 notes TEXT,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_partners_name ON business_partners(name);
CREATE INDEX IF NOT EXISTS idx_partners_type ON business_partners(partner_type,is_active);




CREATE TABLE IF NOT EXISTS price_levels(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 description TEXT,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS product_price_levels(
 product_id INTEGER NOT NULL,
 price_level_id INTEGER NOT NULL,
 selling_price NUMERIC NOT NULL DEFAULT 0 CHECK(selling_price>=0),
 updated_at TEXT NOT NULL,
 PRIMARY KEY(product_id,price_level_id),
 FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
 FOREIGN KEY(price_level_id) REFERENCES price_levels(id));

CREATE TABLE IF NOT EXISTS document_sequences(
 sequence_key TEXT PRIMARY KEY,
 current_value INTEGER NOT NULL DEFAULT 0,
 updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS sales(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 invoice_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 delivery_no TEXT UNIQUE COLLATE NOCASE,
 sale_date TEXT NOT NULL,
 customer_id INTEGER,
 department_id INTEGER,
 project_id INTEGER,
 payment_type TEXT NOT NULL CHECK(payment_type IN ('CASH','CREDIT')),
 subtotal NUMERIC NOT NULL DEFAULT 0 CHECK(subtotal >= 0),
 discount_amount NUMERIC NOT NULL DEFAULT 0 CHECK(discount_amount >= 0),
 total_amount NUMERIC NOT NULL DEFAULT 0 CHECK(total_amount >= 0),
 paid_amount NUMERIC NOT NULL DEFAULT 0 CHECK(paid_amount >= 0),
 balance_due NUMERIC NOT NULL DEFAULT 0 CHECK(balance_due >= 0),
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'POSTED' CHECK(status IN ('POSTED','VOID')),
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(customer_id) REFERENCES business_partners(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));

CREATE TABLE IF NOT EXISTS sales_items(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 sale_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 sku TEXT NOT NULL,
 product_name TEXT NOT NULL,
 product_type TEXT NOT NULL,
 qty NUMERIC NOT NULL CHECK(qty > 0),
 unit_price NUMERIC NOT NULL CHECK(unit_price >= 0),
 discount_amount NUMERIC NOT NULL DEFAULT 0 CHECK(discount_amount >= 0),
 line_total NUMERIC NOT NULL CHECK(line_total >= 0),
 purchase_price_snapshot NUMERIC NOT NULL DEFAULT 0,
 FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
 FOREIGN KEY(product_id) REFERENCES products(id));

CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date,id DESC);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id,sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_items_sale ON sales_items(sale_id);

CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id,id DESC);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(id DESC);

CREATE TABLE IF NOT EXISTS document_templates(
 document_type TEXT PRIMARY KEY,title TEXT NOT NULL,header_text TEXT,footer_text TEXT,
 show_logo INTEGER NOT NULL DEFAULT 1,show_prices INTEGER NOT NULL DEFAULT 1,
 paper_size TEXT NOT NULL DEFAULT 'A5',updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS bank_import_batches(
 id INTEGER PRIMARY KEY AUTOINCREMENT,file_name TEXT NOT NULL,bank_name TEXT,row_count INTEGER NOT NULL DEFAULT 0,
 posted_count INTEGER NOT NULL DEFAULT 0,status TEXT NOT NULL DEFAULT 'PREVIEW',user_id INTEGER NOT NULL,created_at TEXT NOT NULL,
 FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS bank_import_rows(
 id INTEGER PRIMARY KEY AUTOINCREMENT,batch_id INTEGER NOT NULL,transaction_date TEXT NOT NULL,description TEXT NOT NULL,
 debit NUMERIC NOT NULL DEFAULT 0,credit NUMERIC NOT NULL DEFAULT 0,balance NUMERIC,cash_account_id INTEGER,counter_coa_id INTEGER,
 posted_transaction_id INTEGER,status TEXT NOT NULL DEFAULT 'PREVIEW',
 FOREIGN KEY(batch_id) REFERENCES bank_import_batches(id) ON DELETE CASCADE,
 FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id),FOREIGN KEY(counter_coa_id) REFERENCES chart_of_accounts(id));
CREATE INDEX IF NOT EXISTS idx_bank_import_rows_batch ON bank_import_rows(batch_id,id);



CREATE TABLE IF NOT EXISTS warehouses(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 address TEXT,
 is_default INTEGER NOT NULL DEFAULT 0,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS inventory_balances(
 warehouse_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 quantity NUMERIC NOT NULL DEFAULT 0,
 average_cost NUMERIC NOT NULL DEFAULT 0,
 updated_at TEXT NOT NULL,
 PRIMARY KEY(warehouse_id, product_id),
 FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
 FOREIGN KEY(product_id) REFERENCES products(id));

CREATE TABLE IF NOT EXISTS inventory_transactions(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 warehouse_id INTEGER NOT NULL,
 movement_type TEXT NOT NULL,
 quantity_change NUMERIC NOT NULL,
 quantity_before NUMERIC NOT NULL,
 quantity_after NUMERIC NOT NULL,
 unit_cost NUMERIC NOT NULL DEFAULT 0,
 average_cost_before NUMERIC NOT NULL DEFAULT 0,
 average_cost_after NUMERIC NOT NULL DEFAULT 0,
 reference_type TEXT,
 reference_no TEXT,
 reason TEXT NOT NULL,
 department_id INTEGER,
 project_id INTEGER,
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 FOREIGN KEY(product_id) REFERENCES products(id),
 FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));

CREATE INDEX IF NOT EXISTS idx_inv_balance_product ON inventory_balances(product_id);
CREATE INDEX IF NOT EXISTS idx_inv_tx_product_wh ON inventory_transactions(product_id,warehouse_id,id DESC);
CREATE INDEX IF NOT EXISTS idx_inv_tx_reference ON inventory_transactions(reference_type,reference_no);


CREATE TABLE IF NOT EXISTS purchases(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 purchase_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 supplier_invoice_no TEXT,
 goods_receipt_no TEXT UNIQUE COLLATE NOCASE,
 purchase_date TEXT NOT NULL,
 supplier_id INTEGER NOT NULL,
 warehouse_id INTEGER NOT NULL,
 department_id INTEGER,
 project_id INTEGER,
 payment_type TEXT NOT NULL CHECK(payment_type IN ('CASH','CREDIT')),
 subtotal NUMERIC NOT NULL DEFAULT 0 CHECK(subtotal >= 0),
 discount_amount NUMERIC NOT NULL DEFAULT 0 CHECK(discount_amount >= 0),
 total_amount NUMERIC NOT NULL DEFAULT 0 CHECK(total_amount >= 0),
 paid_amount NUMERIC NOT NULL DEFAULT 0 CHECK(paid_amount >= 0),
 balance_due NUMERIC NOT NULL DEFAULT 0 CHECK(balance_due >= 0),
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'POSTED' CHECK(status IN ('POSTED','VOID')),
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(supplier_id) REFERENCES business_partners(id),
 FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));

CREATE TABLE IF NOT EXISTS purchase_items(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 purchase_id INTEGER NOT NULL,
 product_id INTEGER NOT NULL,
 sku TEXT NOT NULL,
 product_name TEXT NOT NULL,
 product_type TEXT NOT NULL,
 qty NUMERIC NOT NULL CHECK(qty > 0),
 unit_cost NUMERIC NOT NULL CHECK(unit_cost >= 0),
 discount_amount NUMERIC NOT NULL DEFAULT 0 CHECK(discount_amount >= 0),
 line_total NUMERIC NOT NULL CHECK(line_total >= 0),
 FOREIGN KEY(purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
 FOREIGN KEY(product_id) REFERENCES products(id));

CREATE INDEX IF NOT EXISTS idx_purchases_date ON purchases(purchase_date,id DESC);
CREATE INDEX IF NOT EXISTS idx_purchases_supplier ON purchases(supplier_id,purchase_date);
CREATE INDEX IF NOT EXISTS idx_purchase_items_purchase ON purchase_items(purchase_id);

CREATE TABLE IF NOT EXISTS cash_accounts(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 account_type TEXT NOT NULL CHECK(account_type IN ('CASH','BANK')),
 bank_name TEXT,
 account_number TEXT,
 opening_balance NUMERIC NOT NULL DEFAULT 0,
 current_balance NUMERIC NOT NULL DEFAULT 0,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS cash_transactions(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 transaction_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 transaction_date TEXT NOT NULL,
 account_id INTEGER NOT NULL,
 transaction_type TEXT NOT NULL CHECK(transaction_type IN ('IN','OUT','TRANSFER_IN','TRANSFER_OUT')),
 amount NUMERIC NOT NULL CHECK(amount > 0),
 balance_before NUMERIC NOT NULL,
 balance_after NUMERIC NOT NULL,
 description TEXT NOT NULL,
 reference_no TEXT,
 transfer_group TEXT,
 department_id INTEGER,
 project_id INTEGER,
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 FOREIGN KEY(account_id) REFERENCES cash_accounts(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));

CREATE INDEX IF NOT EXISTS idx_cash_tx_account_date ON cash_transactions(account_id,transaction_date,id DESC);
CREATE INDEX IF NOT EXISTS idx_cash_tx_reference ON cash_transactions(reference_no);


CREATE TABLE IF NOT EXISTS chart_of_accounts(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 name TEXT NOT NULL,
 account_type TEXT NOT NULL CHECK(account_type IN ('ASSET','LIABILITY','EQUITY','REVENUE','EXPENSE')),
 account_subtype TEXT,
 normal_balance TEXT NOT NULL CHECK(normal_balance IN ('DEBIT','CREDIT')),
 parent_id INTEGER,
 is_system INTEGER NOT NULL DEFAULT 0,
 is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(parent_id) REFERENCES chart_of_accounts(id));

CREATE TABLE IF NOT EXISTS purchase_returns(id INTEGER PRIMARY KEY AUTOINCREMENT,return_no TEXT NOT NULL UNIQUE COLLATE NOCASE,return_date TEXT NOT NULL,purchase_id INTEGER,supplier_id INTEGER NOT NULL,warehouse_id INTEGER NOT NULL,total_payable NUMERIC NOT NULL,total_inventory NUMERIC NOT NULL,difference NUMERIC NOT NULL DEFAULT 0,notes TEXT,status TEXT NOT NULL DEFAULT 'POSTED',user_id INTEGER NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS purchase_return_items(id INTEGER PRIMARY KEY AUTOINCREMENT,return_id INTEGER NOT NULL,product_id INTEGER NOT NULL,sku TEXT NOT NULL,product_name TEXT NOT NULL,qty NUMERIC NOT NULL,unit_value NUMERIC NOT NULL,average_cost NUMERIC NOT NULL,payable_value NUMERIC NOT NULL,inventory_value NUMERIC NOT NULL,FOREIGN KEY(return_id) REFERENCES purchase_returns(id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS sales_returns(id INTEGER PRIMARY KEY AUTOINCREMENT,return_no TEXT NOT NULL UNIQUE COLLATE NOCASE,return_date TEXT NOT NULL,sale_id INTEGER,customer_id INTEGER NOT NULL,warehouse_id INTEGER NOT NULL,total_sales NUMERIC NOT NULL,total_cogs NUMERIC NOT NULL,notes TEXT,status TEXT NOT NULL DEFAULT 'POSTED',user_id INTEGER NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sales_return_items(id INTEGER PRIMARY KEY AUTOINCREMENT,return_id INTEGER NOT NULL,product_id INTEGER NOT NULL,sku TEXT NOT NULL,product_name TEXT NOT NULL,product_type TEXT NOT NULL,qty NUMERIC NOT NULL,unit_value NUMERIC NOT NULL,average_cost NUMERIC NOT NULL,sales_value NUMERIC NOT NULL,cogs_value NUMERIC NOT NULL,FOREIGN KEY(return_id) REFERENCES sales_returns(id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS fiscal_year_closings(id INTEGER PRIMARY KEY AUTOINCREMENT,fiscal_year INTEGER NOT NULL UNIQUE,closing_date TEXT NOT NULL,net_profit NUMERIC NOT NULL,journal_id INTEGER,created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS fixed_assets(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 asset_code TEXT NOT NULL UNIQUE COLLATE NOCASE,
 asset_name TEXT NOT NULL,
 acquisition_date TEXT NOT NULL,
 acquisition_cost NUMERIC NOT NULL CHECK(acquisition_cost>0),
 residual_value NUMERIC NOT NULL DEFAULT 0 CHECK(residual_value>=0),
 useful_life_months INTEGER NOT NULL CHECK(useful_life_months>=0),
 asset_account_id INTEGER NOT NULL,
 accumulated_depreciation_account_id INTEGER NOT NULL,
 depreciation_expense_account_id INTEGER NOT NULL,
 contra_account_id INTEGER NOT NULL,
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(status IN ('ACTIVE','DISPOSED')),
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(asset_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(accumulated_depreciation_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(depreciation_expense_account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(contra_account_id) REFERENCES chart_of_accounts(id));
CREATE TABLE IF NOT EXISTS fixed_asset_depreciations(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 asset_id INTEGER NOT NULL,
 period TEXT NOT NULL,
 depreciation_date TEXT NOT NULL,
 amount NUMERIC NOT NULL CHECK(amount>=0),
 journal_id INTEGER,
 created_at TEXT NOT NULL,
 UNIQUE(asset_id,period),
 FOREIGN KEY(asset_id) REFERENCES fixed_assets(id) ON DELETE CASCADE,
 FOREIGN KEY(journal_id) REFERENCES journal_entries(id));
CREATE INDEX IF NOT EXISTS idx_fixed_assets_status ON fixed_assets(status,acquisition_date);



CREATE TABLE IF NOT EXISTS sales_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 order_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 order_date TEXT NOT NULL,
 customer_id INTEGER NOT NULL,
 department_id INTEGER,
 project_id INTEGER,
 expected_date TEXT,
 subtotal NUMERIC NOT NULL DEFAULT 0,
 discount_amount NUMERIC NOT NULL DEFAULT 0,
 tax_percent NUMERIC NOT NULL DEFAULT 0,
 tax_amount NUMERIC NOT NULL DEFAULT 0,
 total_amount NUMERIC NOT NULL DEFAULT 0,
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('DRAFT','OPEN','COMPLETED','CANCELLED')),
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(customer_id) REFERENCES business_partners(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS sales_order_items(
 id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,product_id INTEGER NOT NULL,
 description TEXT,qty NUMERIC NOT NULL,unit_id INTEGER,unit_code TEXT,conversion_ratio NUMERIC NOT NULL DEFAULT 1,unit_price NUMERIC NOT NULL,discount_amount NUMERIC NOT NULL DEFAULT 0,line_total NUMERIC NOT NULL,
 FOREIGN KEY(order_id) REFERENCES sales_orders(id) ON DELETE CASCADE,FOREIGN KEY(product_id) REFERENCES products(id));
CREATE INDEX IF NOT EXISTS idx_sales_orders_date ON sales_orders(order_date,id DESC);

CREATE TABLE IF NOT EXISTS purchase_orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 order_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 order_date TEXT NOT NULL,
 supplier_id INTEGER NOT NULL,
 warehouse_id INTEGER NOT NULL,
 department_id INTEGER,
 project_id INTEGER,
 expected_date TEXT,
 subtotal NUMERIC NOT NULL DEFAULT 0,
 discount_amount NUMERIC NOT NULL DEFAULT 0,
 tax_percent NUMERIC NOT NULL DEFAULT 0,
 tax_amount NUMERIC NOT NULL DEFAULT 0,
 total_amount NUMERIC NOT NULL DEFAULT 0,
 notes TEXT,
 status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN ('DRAFT','OPEN','COMPLETED','CANCELLED')),
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(supplier_id) REFERENCES business_partners(id),FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),FOREIGN KEY(project_id) REFERENCES projects(id),FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS purchase_order_items(
 id INTEGER PRIMARY KEY AUTOINCREMENT,order_id INTEGER NOT NULL,product_id INTEGER NOT NULL,
 description TEXT,qty NUMERIC NOT NULL,unit_id INTEGER,unit_code TEXT,conversion_ratio NUMERIC NOT NULL DEFAULT 1,unit_cost NUMERIC NOT NULL,discount_amount NUMERIC NOT NULL DEFAULT 0,line_total NUMERIC NOT NULL,
 FOREIGN KEY(order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,FOREIGN KEY(product_id) REFERENCES products(id));
CREATE INDEX IF NOT EXISTS idx_purchase_orders_date ON purchase_orders(order_date,id DESC);

CREATE TABLE IF NOT EXISTS customer_downpayments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,dp_no TEXT NOT NULL UNIQUE COLLATE NOCASE,dp_date TEXT NOT NULL,
 customer_id INTEGER NOT NULL,sales_order_id INTEGER,cash_account_id INTEGER NOT NULL,amount NUMERIC NOT NULL,
 allocated_amount NUMERIC NOT NULL DEFAULT 0,notes TEXT,status TEXT NOT NULL DEFAULT 'POSTED',journal_id INTEGER,user_id INTEGER NOT NULL,created_at TEXT NOT NULL,
 FOREIGN KEY(customer_id) REFERENCES business_partners(id),FOREIGN KEY(sales_order_id) REFERENCES sales_orders(id),
 FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id),FOREIGN KEY(journal_id) REFERENCES journal_entries(id),FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS supplier_downpayments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,dp_no TEXT NOT NULL UNIQUE COLLATE NOCASE,dp_date TEXT NOT NULL,
 supplier_id INTEGER NOT NULL,purchase_order_id INTEGER,cash_account_id INTEGER NOT NULL,amount NUMERIC NOT NULL,
 allocated_amount NUMERIC NOT NULL DEFAULT 0,notes TEXT,status TEXT NOT NULL DEFAULT 'POSTED',journal_id INTEGER,user_id INTEGER NOT NULL,created_at TEXT NOT NULL,
 FOREIGN KEY(supplier_id) REFERENCES business_partners(id),FOREIGN KEY(purchase_order_id) REFERENCES purchase_orders(id),
 FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id),FOREIGN KEY(journal_id) REFERENCES journal_entries(id),FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS downpayment_allocations(
 id INTEGER PRIMARY KEY AUTOINCREMENT,allocation_no TEXT NOT NULL UNIQUE COLLATE NOCASE,allocation_date TEXT NOT NULL,
 allocation_type TEXT NOT NULL CHECK(allocation_type IN ('CUSTOMER','SUPPLIER')),downpayment_id INTEGER NOT NULL,
 invoice_id INTEGER NOT NULL,amount NUMERIC NOT NULL,status TEXT NOT NULL DEFAULT 'POSTED',journal_id INTEGER,user_id INTEGER NOT NULL,created_at TEXT NOT NULL,
 FOREIGN KEY(journal_id) REFERENCES journal_entries(id),FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX IF NOT EXISTS idx_dp_alloc_type_invoice ON downpayment_allocations(allocation_type,invoice_id,status);

CREATE TABLE IF NOT EXISTS transaction_voids(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 transaction_kind TEXT NOT NULL,
 transaction_key TEXT NOT NULL,
 reason TEXT,
 replacement_key TEXT,
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 UNIQUE(transaction_kind,transaction_key));

CREATE TABLE IF NOT EXISTS journal_entries(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 journal_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
 journal_date TEXT NOT NULL,
 description TEXT NOT NULL,
 source_type TEXT,
 source_id TEXT,
 reference_no TEXT,
 department_id INTEGER,
 project_id INTEGER,
 status TEXT NOT NULL DEFAULT 'POSTED' CHECK(status IN ('POSTED','VOID')),
 total_debit NUMERIC NOT NULL DEFAULT 0,
 total_credit NUMERIC NOT NULL DEFAULT 0,
 user_id INTEGER NOT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL,
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id),
 FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE IF NOT EXISTS journal_lines(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 journal_id INTEGER NOT NULL,
 account_id INTEGER NOT NULL,
 debit NUMERIC NOT NULL DEFAULT 0,
 credit NUMERIC NOT NULL DEFAULT 0,
 memo TEXT,
 partner_id INTEGER,
 partner_type TEXT,
 department_id INTEGER,
 project_id INTEGER,
 FOREIGN KEY(journal_id) REFERENCES journal_entries(id) ON DELETE CASCADE,
 FOREIGN KEY(account_id) REFERENCES chart_of_accounts(id),
 FOREIGN KEY(department_id) REFERENCES departments(id),
 FOREIGN KEY(project_id) REFERENCES projects(id));
CREATE UNIQUE INDEX IF NOT EXISTS uq_journal_source ON journal_entries(source_type,source_id) WHERE source_type IS NOT NULL AND source_id IS NOT NULL AND status='POSTED';
CREATE INDEX IF NOT EXISTS idx_journal_date ON journal_entries(journal_date,id DESC);
CREATE INDEX IF NOT EXISTS idx_journal_lines_account ON journal_lines(account_id,journal_id);

CREATE TABLE IF NOT EXISTS receivable_payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_no TEXT NOT NULL UNIQUE COLLATE NOCASE, payment_date TEXT NOT NULL, sale_id INTEGER NOT NULL, customer_id INTEGER NOT NULL, cash_account_id INTEGER NOT NULL, amount NUMERIC NOT NULL CHECK(amount > 0), notes TEXT, user_id INTEGER NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(sale_id) REFERENCES sales(id), FOREIGN KEY(customer_id) REFERENCES business_partners(id), FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX IF NOT EXISTS idx_receivable_sale ON receivable_payments(sale_id,payment_date);
CREATE TABLE IF NOT EXISTS payable_payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_no TEXT NOT NULL UNIQUE COLLATE NOCASE, payment_date TEXT NOT NULL, purchase_id INTEGER NOT NULL, supplier_id INTEGER NOT NULL, cash_account_id INTEGER NOT NULL, amount NUMERIC NOT NULL CHECK(amount > 0), notes TEXT, user_id INTEGER NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(purchase_id) REFERENCES purchases(id), FOREIGN KEY(supplier_id) REFERENCES business_partners(id), FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX IF NOT EXISTS idx_payable_purchase ON payable_payments(purchase_id,payment_date);
CREATE TABLE IF NOT EXISTS opening_receivable_payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_no TEXT NOT NULL UNIQUE COLLATE NOCASE, payment_date TEXT NOT NULL, customer_id INTEGER NOT NULL, cash_account_id INTEGER NOT NULL, amount NUMERIC NOT NULL CHECK(amount > 0), notes TEXT, user_id INTEGER NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES business_partners(id), FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX IF NOT EXISTS idx_opening_receivable_customer ON opening_receivable_payments(customer_id,payment_date);
CREATE TABLE IF NOT EXISTS opening_payable_payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT, payment_no TEXT NOT NULL UNIQUE COLLATE NOCASE, payment_date TEXT NOT NULL, supplier_id INTEGER NOT NULL, cash_account_id INTEGER NOT NULL, amount NUMERIC NOT NULL CHECK(amount > 0), notes TEXT, user_id INTEGER NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(supplier_id) REFERENCES business_partners(id), FOREIGN KEY(cash_account_id) REFERENCES cash_accounts(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX IF NOT EXISTS idx_opening_payable_supplier ON opening_payable_payments(supplier_id,payment_date);

"""

ROLES=[
("ADMIN","Administrator",'["*"]'),
("OWNER","Owner",'["dashboard.view","reports.view","audit.view","inventory.view","partners.view","sales.view","purchases.view","cash.view","accounting.view"]'),
("ACCOUNTING","Accounting",'["dashboard.view","accounting.manage","reports.view","inventory.view","partners.view","partners.manage","sales.view","purchases.view","purchases.manage","cash.view","cash.manage","accounting.view","accounting.manage","receivables.view","receivables.manage","payables.view","payables.manage"]'),
("CASHIER","Kasir",'["dashboard.view","sales.view","sales.manage","inventory.view","partners.view","partners.manage","cash.view","cash.manage","accounting.view","accounting.manage","receivables.view","receivables.manage","payables.view","payables.manage"]'),
("WAREHOUSE","Gudang",'["dashboard.view","inventory.view","inventory.manage","partners.view","purchases.view","purchases.manage"]')]

def connect():
    if IS_POSTGRES:
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL PostgreSQL belum dikonfigurasi.")
        return pg_compat.connect(DATABASE_URL)
    c=sqlite3.connect(DB_PATH,timeout=15,check_same_thread=False); c.row_factory=sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=10000"); return c

@contextmanager
def write_transaction():
    # PostgreSQL handles row-level concurrency; the process lock is kept only to
    # preserve ordering assumptions in the legacy repository.
    with WRITE_LOCK:
        c=connect()
        try:
            if not IS_POSTGRES:
                c.execute("BEGIN IMMEDIATE")
            yield c; c.commit()
        except Exception:
            c.rollback(); raise
        finally: c.close()


def _ensure_column(conn, table, column, ddl):
    if IS_POSTGRES:
        row=conn.execute("""SELECT 1 FROM information_schema.columns
            WHERE table_schema=current_schema() AND table_name=? AND column_name=?""",(table,column)).fetchone()
        if not row:
            ddl_pg=ddl.replace(" BLOB"," BYTEA").replace(" REAL"," DOUBLE PRECISION")
            ddl_pg=__import__('re').sub(r"\s+REFERENCES\s+[\w\"]+\s*\([^)]*\)(?:\s+ON\s+DELETE\s+\w+)?", "", ddl_pg, flags=__import__('re').I)
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl_pg}")
        return
    cols={r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")

def _prepare_audit_logs_schema(conn):
    """Preserve legacy Standard audit table before the Pro schema is created."""
    if IS_POSTGRES:
        return None
    tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'audit_logs' not in tables:
        return None
    cols={r[1] for r in conn.execute('PRAGMA table_info("audit_logs")')}
    required={'user_id','action','entity_type','entity_id','details_json','client_ip','created_at'}
    if required.issubset(cols):
        return None
    base='legacy_standard_audit_logs'
    target=base
    n=2
    while target in tables:
        target=f'{base}_{n}'
        n+=1
    conn.execute(f'ALTER TABLE "audit_logs" RENAME TO "{target}"')
    return target


def _migrate_legacy_audit_logs(conn, now):
    """Copy legacy audit rows into the current audit table once."""
    if IS_POSTGRES:
        return 0
    import json as _json
    tables=[r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'legacy_standard_audit_logs%'")]
    if not tables:
        return 0
    users={r['username'].lower():r['id'] for r in conn.execute('SELECT id,username FROM users') if r['username']}
    count=0
    for table in tables:
        cols={r[1] for r in conn.execute(f'PRAGMA table_info("{table}")')}
        if 'migration_audit_marker' in cols:
            continue
        rows=conn.execute(f'SELECT * FROM "{table}" ORDER BY id').fetchall()
        for r in rows:
            keys=set(r.keys())
            username=(r['username'] if 'username' in keys else None) or ''
            uid=users.get(str(username).lower())
            action=(r['action'] if 'action' in keys else None) or 'LEGACY'
            entity=(r['table_name'] if 'table_name' in keys else None) or (r['entity_type'] if 'entity_type' in keys else None)
            if 'record_id' in keys:
                entity_id=r['record_id']
            elif 'entity_id' in keys:
                entity_id=r['entity_id']
            else:
                entity_id=None
            description=(r['description'] if 'description' in keys else None) or ''
            created=(r['log_time'] if 'log_time' in keys else None) or (r['created_at'] if 'created_at' in keys else None) or now
            details=_json.dumps({'legacy':True,'description':description},ensure_ascii=False)
            conn.execute("""INSERT INTO audit_logs(user_id,action,entity_type,entity_id,details_json,client_ip,created_at)
                            VALUES(?,?,?,?,?,?,?)""",(uid,action,entity,str(entity_id) if entity_id is not None else None,details,None,created))
            count+=1
        conn.execute(f'ALTER TABLE "{table}" ADD COLUMN migration_audit_marker INTEGER NOT NULL DEFAULT 1')
    return count

def _allow_zero_useful_life(c):
    """Relax legacy fixed_assets CHECK from >0 to >=0 without dropping asset history."""
    if IS_POSTGRES:
        return
    row=c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='fixed_assets'").fetchone()
    if not row:return
    sql=row["sql"] if hasattr(row,"keys") else row[0]
    if not sql:return
    new_sql=sql.replace("CHECK(useful_life_months>0)","CHECK(useful_life_months>=0)")
    new_sql=new_sql.replace("CHECK (useful_life_months>0)","CHECK (useful_life_months>=0)")
    new_sql=new_sql.replace("CHECK(useful_life_months > 0)","CHECK(useful_life_months >= 0)")
    if new_sql==sql:return
    version=int(c.execute("PRAGMA schema_version").fetchone()[0])
    try:
        c.execute("PRAGMA writable_schema=ON")
        c.execute("UPDATE sqlite_master SET sql=? WHERE type='table' AND name='fixed_assets'",(new_sql,))
    finally:
        c.execute("PRAGMA writable_schema=OFF")
    c.execute(f"PRAGMA schema_version={version+1}")

def init_database():
    if not IS_POSTGRES:
        prepare_legacy_schema(DB_PATH, 'ULTIMA', BACKUP_DIR)
    with WRITE_LOCK:
        c=connect()
        try:
            _prepare_audit_logs_schema(c)
            c.executescript(SCHEMA)
            subscription.ensure_schema(c)
            _allow_zero_useful_life(c)
            now=utc_now()
            c.execute("INSERT OR IGNORE INTO owner_cloud_settings(id,updated_at) VALUES(1,?)",(now,))
            _ensure_column(c,"sessions","device_id","device_id TEXT")
            _ensure_column(c,"sessions","user_agent","user_agent TEXT")
            _ensure_column(c,"project_documents","file_content","file_content BLOB")
            _ensure_column(c,"company_profile","logo_content","logo_content BLOB")
            _ensure_column(c,"company_profile","logo_mime","logo_mime TEXT")
            _ensure_column(c,"sales_order_items","unit_id","unit_id INTEGER")
            _ensure_column(c,"sales_order_items","unit_code","unit_code TEXT")
            _ensure_column(c,"sales_order_items","conversion_ratio","conversion_ratio NUMERIC NOT NULL DEFAULT 1")
            _ensure_column(c,"purchase_order_items","unit_id","unit_id INTEGER")
            _ensure_column(c,"purchase_order_items","unit_code","unit_code TEXT")
            _ensure_column(c,"purchase_order_items","conversion_ratio","conversion_ratio NUMERIC NOT NULL DEFAULT 1")
            _ensure_column(c,"products","opening_stock_qty","opening_stock_qty NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"products","opening_warehouse_id","opening_warehouse_id INTEGER")
            _ensure_column(c,"products","brand_id","brand_id INTEGER REFERENCES brands(id)")
            _ensure_column(c,"products","inventory_account_id","inventory_account_id INTEGER")
            _ensure_column(c,"products","sales_account_id","sales_account_id INTEGER")
            # Opening-stock metadata for databases created before editable saldo awal.
            c.execute("""UPDATE products SET opening_stock_qty=COALESCE((SELECT SUM(quantity_change) FROM inventory_transactions it WHERE it.product_id=products.id AND it.reference_type='OPENING'),0)
              WHERE COALESCE(opening_stock_qty,0)=0""")
            c.execute("""UPDATE products SET opening_warehouse_id=(SELECT warehouse_id FROM inventory_transactions it WHERE it.product_id=products.id AND it.reference_type='OPENING' ORDER BY it.id LIMIT 1)
              WHERE opening_warehouse_id IS NULL""")
            # HPP snapshot repair from actual inventory transaction / moving-average cost.
            c.execute("""UPDATE sales_items SET purchase_price_snapshot=COALESCE((
              SELECT CASE WHEN ABS(SUM(it.quantity_change))>0 THEN SUM(ABS(it.quantity_change)*it.unit_cost)/SUM(ABS(it.quantity_change)) END
              FROM inventory_transactions it JOIN sales s ON s.invoice_no=it.reference_no
              WHERE s.id=sales_items.sale_id AND it.product_id=sales_items.product_id AND it.reference_type='SALE'
            ),purchase_price_snapshot) WHERE product_type='STOCK'""")

            _ensure_column(c,"products","cogs_account_id","cogs_account_id INTEGER")
            _ensure_column(c,"sales","delivery_no","delivery_no TEXT")
            _ensure_column(c,"sales","sales_order_id","sales_order_id INTEGER REFERENCES sales_orders(id)")
            _ensure_column(c,"purchases","purchase_order_id","purchase_order_id INTEGER REFERENCES purchase_orders(id)")
            _ensure_column(c,"purchases","supplier_invoice_no","supplier_invoice_no TEXT")
            _ensure_column(c,"purchases","goods_receipt_no","goods_receipt_no TEXT")
            _ensure_column(c,"business_partners","partner_group","partner_group TEXT")
            _ensure_column(c,"business_partners","opening_balance","opening_balance NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"business_partners","contact_person","contact_person TEXT")
            _ensure_column(c,"business_partners","price_level_id","price_level_id INTEGER REFERENCES price_levels(id)")
            _ensure_column(c,"business_partners","receivable_account_id","receivable_account_id INTEGER REFERENCES chart_of_accounts(id)")
            _ensure_column(c,"business_partners","payable_account_id","payable_account_id INTEGER REFERENCES chart_of_accounts(id)")
            _ensure_column(c,"sales","salesperson_id","salesperson_id INTEGER REFERENCES salespersons(id)")
            _ensure_column(c,"sales","warehouse_id","warehouse_id INTEGER REFERENCES warehouses(id)")
            _ensure_column(c,"sales","payment_method","payment_method TEXT NOT NULL DEFAULT 'CASH'")
            _ensure_column(c,"sales","cash_account_id","cash_account_id INTEGER REFERENCES cash_accounts(id)")
            _ensure_column(c,"sales","due_date","due_date TEXT")
            _ensure_column(c,"sales","tax_percent","tax_percent NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"sales","tax_amount","tax_amount NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"sales_items","discount_percent","discount_percent NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"sales_items","entered_qty","entered_qty NUMERIC")
            _ensure_column(c,"sales_items","unit_id","unit_id INTEGER")
            _ensure_column(c,"sales_items","unit_code","unit_code TEXT")
            _ensure_column(c,"sales_items","conversion_ratio","conversion_ratio NUMERIC NOT NULL DEFAULT 1")

            _ensure_column(c,"purchases","payment_method","payment_method TEXT NOT NULL DEFAULT 'CASH'")
            _ensure_column(c,"purchases","cash_account_id","cash_account_id INTEGER REFERENCES cash_accounts(id)")
            _ensure_column(c,"purchases","due_date","due_date TEXT")
            _ensure_column(c,"purchases","tax_percent","tax_percent NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"purchases","tax_amount","tax_amount NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"purchase_items","discount_percent","discount_percent NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"purchase_items","entered_qty","entered_qty NUMERIC")
            _ensure_column(c,"purchase_items","unit_id","unit_id INTEGER")
            _ensure_column(c,"purchase_items","unit_code","unit_code TEXT")
            _ensure_column(c,"purchase_items","conversion_ratio","conversion_ratio NUMERIC NOT NULL DEFAULT 1")

            _ensure_column(c,"cash_accounts","coa_account_id","coa_account_id INTEGER REFERENCES chart_of_accounts(id)")
            _ensure_column(c,"chart_of_accounts","account_subtype","account_subtype TEXT")
            _ensure_column(c,"journal_lines","partner_id","partner_id INTEGER")
            _ensure_column(c,"journal_lines","partner_type","partner_type TEXT")
            _ensure_column(c,"business_partners","opening_balance_date","opening_balance_date TEXT")
            _ensure_column(c,"products","opening_balance_date","opening_balance_date TEXT")
            _ensure_column(c,"services","product_id","product_id INTEGER REFERENCES products(id)")
            _ensure_column(c,"document_templates","options_json","options_json TEXT")
            _ensure_column(c,"sales","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"sales","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"purchases","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"purchases","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"cash_transactions","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"cash_transactions","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"inventory_transactions","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"inventory_transactions","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"inventory_transactions","value_change","value_change NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"inventory_transactions","value_before","value_before NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"inventory_transactions","value_after","value_after NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"inventory_balances","book_value","book_value NUMERIC NOT NULL DEFAULT 0")
            
            _ensure_column(c,"journal_entries","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"journal_entries","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"journal_lines","department_id","department_id INTEGER REFERENCES departments(id)")
            _ensure_column(c,"journal_lines","project_id","project_id INTEGER REFERENCES projects(id)")
            _ensure_column(c,"projects","contract_no","contract_no TEXT")
            _ensure_column(c,"projects","contract_value","contract_value NUMERIC NOT NULL DEFAULT 0")
            _ensure_column(c,"projects","location","location TEXT")
            _ensure_column(c,"projects","pic_name","pic_name TEXT")
            _ensure_column(c,"projects","project_type","project_type TEXT")
            _ensure_column(c,"projects","retention_percent","retention_percent NUMERIC NOT NULL DEFAULT 0")
            c.execute("""INSERT INTO company_profile(id,company_name,created_at,updated_at)
                         VALUES(1,'Perusahaan Saya',?,?) ON CONFLICT(id) DO NOTHING""",(now,now))
            c.execute("""INSERT INTO brands(code,name,is_active,created_at,updated_at)
                         VALUES('UMUM','Tanpa Merk',1,?,?) ON CONFLICT(code) DO NOTHING""",(now,now))
            for code,name,perms in ROLES:
                c.execute("""INSERT INTO roles(code,name,permissions_json,created_at) VALUES(?,?,?,?)
                ON CONFLICT(code) DO NOTHING""",
                (code,name,perms,now))
            rid=c.execute("SELECT id FROM roles WHERE code='ADMIN'").fetchone()["id"]
            if not c.execute("SELECT 1 FROM users WHERE username='admin'").fetchone():
                initial_password=str(os.environ.get("STOKLEDGER_ADMIN_PASSWORD", "")).strip()
                if not initial_password:
                    # Local-only convenience. Public/Railway deployment must set the secret.
                    if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_PROJECT_ID"):
                        raise RuntimeError("Set STOKLEDGER_ADMIN_PASSWORD (minimal 8 karakter) pada Railway Variables sebelum deploy.")
                    initial_password="admin123"
                if len(initial_password)<8:
                    raise RuntimeError("STOKLEDGER_ADMIN_PASSWORD minimal 8 karakter.")
                c.execute("""INSERT INTO users(username,full_name,password_hash,role_id,is_active,created_at,updated_at)
                VALUES(?,?,?,?,1,?,?)""",("admin","Administrator",hash_password(initial_password),rid,now,now))
            _migrate_legacy_audit_logs(c, now)
            c.execute("""INSERT INTO item_categories(code,name,is_active,created_at,updated_at)
                         VALUES('UMUM','Umum',1,?,?) ON CONFLICT(code) DO NOTHING""",(now,now))
            c.execute("""INSERT INTO units(code,name,decimals,is_active,created_at,updated_at)
                         VALUES('PCS','Pieces',0,1,?,?) ON CONFLICT(code) DO NOTHING""",(now,now))

            c.execute("""INSERT INTO warehouses(code,name,address,is_default,is_active,created_at,updated_at)
                         VALUES('UTAMA','Gudang Utama',NULL,1,1,?,?)
                         ON CONFLICT(code) DO NOTHING""",(now,now))
            default_wh=c.execute("SELECT id FROM warehouses WHERE is_default=1 ORDER BY id LIMIT 1").fetchone()
            if not default_wh:
                default_wh=c.execute("SELECT id FROM warehouses WHERE code='UTAMA'").fetchone()
                c.execute("UPDATE warehouses SET is_default=1 WHERE id=?",(default_wh["id"],))
            # Migrasi otomatis stok total versi lama ke Gudang Utama satu kali per produk.
            c.execute("""INSERT INTO inventory_balances(warehouse_id,product_id,quantity,average_cost,updated_at)
                         SELECT ?,p.id,p.stock_qty,p.purchase_price,?
                         FROM products p
                         WHERE p.product_type='STOCK'
                           AND NOT EXISTS(
                             SELECT 1 FROM inventory_balances b WHERE b.product_id=p.id
                           )""",(default_wh["id"],now))
            c.execute("""INSERT INTO cash_accounts(code,name,account_type,opening_balance,current_balance,is_active,created_at,updated_at)
                         VALUES('KAS','Kas Utama','CASH',0,0,1,?,?) ON CONFLICT(code) DO NOTHING""",(now,now))
            c.execute("""INSERT INTO cash_accounts(code,name,account_type,opening_balance,current_balance,is_active,created_at,updated_at)
                         VALUES('BANK','Bank Utama','BANK',0,0,1,?,?) ON CONFLICT(code) DO NOTHING""",(now,now))

            coa_seed=[('1000','Kas','ASSET','DEBIT',1),('1010','Bank','ASSET','DEBIT',1),('1100','Piutang Usaha','ASSET','DEBIT',1),('1200','Persediaan','ASSET','DEBIT',1),('1300','PPN Masukan','ASSET','DEBIT',1),('1400','Aktiva Tetap','ASSET','DEBIT',0),('1410','Akumulasi Penyusutan Aktiva Tetap','ASSET','CREDIT',0),('2000','Hutang Usaha','LIABILITY','CREDIT',1),('2100','PPN Keluaran','LIABILITY','CREDIT',1),('3000','Modal','EQUITY','CREDIT',1),('3100','Laba Ditahan','EQUITY','CREDIT',1),('3200','Opening Balance','EQUITY','CREDIT',1),('4000','Penjualan','REVENUE','CREDIT',1),('4100','Retur Penjualan','REVENUE','DEBIT',0),('5000','Harga Pokok Penjualan','EXPENSE','DEBIT',1),('5100','Beban Pembelian/Jasa','EXPENSE','DEBIT',1),('5200','Beban Penyusutan','EXPENSE','DEBIT',0),('5140','Beban Diskon Penjualan','EXPENSE','DEBIT',1),('5150','Beban Komisi Salesman','EXPENSE','DEBIT',1),('2150','Hutang Komisi Salesman','LIABILITY','CREDIT',1)]
            for code,name,atype,normal,system in coa_seed:
                c.execute("""INSERT INTO chart_of_accounts(code,name,account_type,normal_balance,is_system,is_active,created_at,updated_at)
                             VALUES(?,?,?,?,?,1,?,?) ON CONFLICT(code) DO UPDATE SET name=excluded.name,account_type=excluded.account_type,normal_balance=excluded.normal_balance""",(code,name,atype,normal,system,now,now))
            subtype_by_code={'1000':'CASH_BANK','1010':'CASH_BANK','1100':'RECEIVABLE','1200':'ASSET','1300':'ASSET','1400':'ASSET','1410':'ASSET','2000':'PAYABLE','2100':'LIABILITY','3000':'EQUITY','3100':'EQUITY','3200':'EQUITY','4000':'REVENUE','5000':'HPP','5100':'OPERATING_EXPENSE','5200':'OPERATING_EXPENSE','5140':'OPERATING_EXPENSE','5150':'OPERATING_EXPENSE','2150':'LIABILITY'}
            for code,subtype in subtype_by_code.items():
                c.execute("UPDATE chart_of_accounts SET account_subtype=? WHERE code=?",(subtype,code))
            for code,name,atype,normal,subtype in [("1250","Uang Muka Pembelian","ASSET","DEBIT","ASSET"),("2200","Uang Muka Pelanggan","LIABILITY","CREDIT","LIABILITY")]:
                c.execute("""INSERT INTO chart_of_accounts(code,name,account_type,normal_balance,is_system,is_active,created_at,updated_at) VALUES(?,?,?,?,1,1,?,?) ON CONFLICT(code) DO NOTHING""",(code,name,atype,normal,now,now))
                c.execute("UPDATE chart_of_accounts SET account_subtype=? WHERE code=?",(subtype,code))
            c.execute("""UPDATE chart_of_accounts SET account_subtype=CASE account_type WHEN 'ASSET' THEN 'ASSET' WHEN 'LIABILITY' THEN 'LIABILITY' WHEN 'EQUITY' THEN 'EQUITY' WHEN 'REVENUE' THEN 'REVENUE' WHEN 'EXPENSE' THEN 'OPERATING_EXPENSE' END WHERE account_subtype IS NULL OR account_subtype=''""")

            default_inventory=c.execute("SELECT id FROM chart_of_accounts WHERE code='1200'").fetchone()
            default_sales=c.execute("SELECT id FROM chart_of_accounts WHERE code='4000'").fetchone()
            default_cogs=c.execute("SELECT id FROM chart_of_accounts WHERE code='5000'").fetchone()
            if default_inventory and default_sales and default_cogs:
                c.execute("""UPDATE products SET
                  inventory_account_id=COALESCE(inventory_account_id,?),
                  sales_account_id=COALESCE(sales_account_id,?),
                  cogs_account_id=COALESCE(cogs_account_id,?)""",
                  (default_inventory["id"],default_sales["id"],default_cogs["id"]))
            kas_coa=c.execute("SELECT id FROM chart_of_accounts WHERE code='1000'").fetchone()['id']
            bank_coa=c.execute("SELECT id FROM chart_of_accounts WHERE code='1010'").fetchone()['id']
            c.execute("UPDATE cash_accounts SET coa_account_id=COALESCE(coa_account_id,?) WHERE code='KAS'",(kas_coa,))
            c.execute("UPDATE cash_accounts SET coa_account_id=COALESCE(coa_account_id,?) WHERE code='BANK'",(bank_coa,))

            if not IS_POSTGRES:
                migrate_legacy_data(c, 'ULTIMA', now)

            templates=[
              ('SALES_INVOICE','NOTA PENJUALAN','Terima kasih atas kepercayaan Anda.','Barang diterima dalam kondisi baik.',1,1,'A5'),
              ('DELIVERY_ORDER','SURAT JALAN','Mohon diterima barang berikut dengan baik.','Barang diterima lengkap dan dalam kondisi baik.',1,0,'A5'),
              ('PURCHASE_INVOICE','FAKTUR PEMBELIAN','Dokumen pembelian dari pemasok.','Dokumen telah diperiksa.',1,1,'A5'),
              ('GOODS_RECEIPT','GOOD RECEIVE','Bukti penerimaan barang.','Barang diterima lengkap dan dalam kondisi baik.',1,0,'A5')]
            # Sinkronisasi Master Jasa ke item transaksi internal bertipe SERVICE.
            service_rows=c.execute("""SELECT * FROM services ORDER BY id""").fetchall()
            for service in service_rows:
                product_id=service["product_id"] if "product_id" in service.keys() else None
                shadow_sku="@SVC:"+service["service_code"]
                if product_id:
                    exists=c.execute("SELECT id FROM products WHERE id=?",(product_id,)).fetchone()
                else:
                    exists=None
                if not exists:
                    cur=c.execute("""INSERT INTO products(
                      sku,barcode,name,category_id,brand_id,unit_id,product_type,
                      purchase_price,selling_price,stock_qty,minimum_stock,notes,
                      inventory_account_id,sales_account_id,cogs_account_id,
                      is_active,created_at,updated_at
                    ) VALUES(?,NULL,?,NULL,NULL,?,'SERVICE',?,?,0,0,?,
                      NULL,?,?,?, ?,?)""",(
                      shadow_sku,service["service_name"],service["unit_id"],
                      service["purchase_price"],service["selling_price"],
                      "Internal Master Jasa",service["sales_account_id"],
                      service["purchase_account_id"],service["is_active"],
                      service["created_at"],service["updated_at"]))
                    product_id=cur.lastrowid
                    c.execute("UPDATE services SET product_id=? WHERE id=?",(product_id,service["id"]))
                else:
                    c.execute("""UPDATE products SET sku=?,name=?,unit_id=?,product_type='SERVICE',
                      purchase_price=?,selling_price=?,stock_qty=0,minimum_stock=0,
                      inventory_account_id=NULL,sales_account_id=?,cogs_account_id=?,
                      is_active=?,updated_at=? WHERE id=?""",(
                      shadow_sku,service["service_name"],service["unit_id"],
                      service["purchase_price"],service["selling_price"],
                      service["sales_account_id"],service["purchase_account_id"],
                      service["is_active"],service["updated_at"],product_id))
            c.execute("UPDATE document_templates SET paper_size='A5' WHERE paper_size='A4'")
            for dtype,title,header,footer,logo,prices,paper in templates:
                c.execute("""INSERT INTO document_templates(document_type,title,header_text,footer_text,show_logo,show_prices,paper_size,updated_at)
                             VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(document_type) DO NOTHING""",
                          (dtype,title,header,footer,logo,prices,paper,now))
            c.commit()
        finally: c.close()


def backup_database(keep_last=30):
    """SQLite local backup. Railway PostgreSQL uses Railway-managed backups."""
    if IS_POSTGRES:
        return None
    if not DB_PATH.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"{DB_PATH.stem}_{stamp}.db"
    with WRITE_LOCK:
        source = sqlite3.connect(str(DB_PATH), timeout=30)
        destination = sqlite3.connect(str(target))
        try:
            source.execute("PRAGMA wal_checkpoint(FULL)")
            source.backup(destination)
            destination.commit()
        finally:
            destination.close()
            source.close()
    # Dokumen proyek disimpan di luar SQLite agar database tetap ringan.
    # Saat backup otomatis, salin folder dokumen dengan timestamp yang sama.
    project_docs = DB_PATH.parent / "project_documents"
    if project_docs.exists():
        import shutil
        docs_target = BACKUP_DIR / f"{DB_PATH.stem}_{stamp}_project_documents"
        try:
            shutil.copytree(project_docs, docs_target, dirs_exist_ok=True)
        except OSError:
            pass
    backups = sorted(BACKUP_DIR.glob(f"{DB_PATH.stem}_*.db"), key=lambda x: x.stat().st_mtime, reverse=True)
    for old in backups[max(1, int(keep_last)):]:
        try:
            old.unlink()
        except OSError:
            pass
    return target
