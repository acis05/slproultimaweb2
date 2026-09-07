import json, secrets, hashlib
from datetime import datetime, timezone, date
from urllib import request, error
from .database import connect, write_transaction
from . import repository as repo
from . import reporting
from .product import PRODUCT_NAME, VERSION, IS_ULTIMA

def _now(): return datetime.now(timezone.utc).isoformat()
def _row():
    c=connect()
    try:
        r=c.execute("SELECT * FROM owner_cloud_settings WHERE id=1").fetchone()
        return dict(r) if r else {}
    finally:c.close()

def status():
    s=_row(); s.pop('client_secret',None)
    s['configured']=bool(s.get('cloud_url'))
    s['registered']=bool(s.get('installation_id') and s.get('company_id'))
    return s

def save_settings(data):
    url=str(data.get('cloud_url','')).strip().rstrip('/')
    if url and not url.startswith('https://') and not url.startswith('http://localhost') and not url.startswith('http://127.0.0.1'):
        raise ValueError('Cloud URL wajib memakai HTTPS.')
    interval=max(1,min(60,int(data.get('sync_interval_minutes') or 5)))
    with write_transaction() as tx:
        tx.execute("UPDATE owner_cloud_settings SET cloud_url=?,sync_interval_minutes=?,enabled=?,updated_at=? WHERE id=1",(url,interval,1 if data.get('enabled') else 0,_now()))
    return status()

def _call(path,payload,secret=None):
    s=_row(); base=(s.get('cloud_url') or '').rstrip('/')
    if not base: raise ValueError('Cloud URL belum diisi.')
    body=json.dumps(payload,ensure_ascii=False).encode('utf-8')
    headers={'Content-Type':'application/json','User-Agent':f'{PRODUCT_NAME}/{VERSION}'}
    if secret:headers['X-Installation-Secret']=secret
    req=request.Request(base+path,data=body,headers=headers,method='POST')
    try:
        with request.urlopen(req,timeout=20) as r:return json.loads(r.read().decode('utf-8'))
    except error.HTTPError as e:
        try:detail=json.loads(e.read().decode()).get('detail')
        except Exception:detail=None
        raise ValueError(detail or f'Cloud menolak permintaan (HTTP {e.code}).')
    except Exception as e:raise ValueError('Tidak dapat terhubung ke cloud: '+str(e))

def register():
    s=_row(); profile=repo.company_profile()
    payload={'company_name':profile.get('name') or PRODUCT_NAME,'edition':PRODUCT_NAME,'desktop_version':VERSION}
    d=_call('/api/v1/installations/register',payload)
    with write_transaction() as tx:
        tx.execute("UPDATE owner_cloud_settings SET company_id=?,installation_id=?,client_secret=?,pairing_code=?,pairing_expires_at=?,last_error=NULL,updated_at=? WHERE id=1",(d['company_id'],d['installation_id'],d['client_secret'],d.get('pairing_code'),d.get('pairing_expires_at'),_now()))
    return status()

def new_pairing_code():
    s=_row()
    if not s.get('installation_id'):raise ValueError('Daftarkan instalasi terlebih dahulu.')
    d=_call('/api/v1/installations/pairing-code',{'installation_id':s['installation_id']},s.get('client_secret'))
    with write_transaction() as tx:tx.execute("UPDATE owner_cloud_settings SET pairing_code=?,pairing_expires_at=?,updated_at=? WHERE id=1",(d['pairing_code'],d['pairing_expires_at'],_now()))
    return status()

REPORT_KINDS = [
    "finance_income", "finance_balance", "finance_cashflow", "finance_ledger",
    "finance_receivables", "finance_payables", "stock_list", "stock_mutation",
    "sales_product", "sales_customer", "purchase_product", "purchase_supplier",
]
if IS_ULTIMA:
    REPORT_KINDS += ["project_summary"]

def _report_snapshot():
    today=date.today()
    filters={"date_from":today.replace(day=1).isoformat(),"date_to":today.isoformat()}
    reports={}
    errors={}
    for kind in REPORT_KINDS:
        try:
            reports[kind]=reporting.report_data(kind,dict(filters))
        except Exception as exc:
            errors[kind]=str(exc)
    if IS_ULTIMA:
        try:
            project_ids=[str(x['id']) for x in repo.list_projects(True)]
            if project_ids:
                pf=dict(filters);pf['project_ids']=','.join(project_ids)
                reports['project_income']=reporting.report_data('project_income',pf)
            else:
                reports['project_income']={"title":"Laba Rugi per Proyek","projects":[],"columns":[],"rows":[],"summary":{"project_count":0}}
        except Exception as exc:
            errors['project_income']=str(exc)
    return {"period":filters,"reports":reports,"errors":errors}

def sync_now():
    s=_row()
    if not s.get('installation_id') or not s.get('client_secret'):raise ValueError('Instalasi belum terdaftar.')
    snapshot=repo.owner_mobile_dashboard()
    report_bundle=_report_snapshot()
    payload={'company_id':s['company_id'],'installation_id':s['installation_id'],'snapshot_at':_now(),'desktop_version':VERSION,'edition':PRODUCT_NAME,'dashboard':snapshot,'reports':report_bundle['reports'],'report_period':report_bundle['period'],'report_errors':report_bundle['errors']}
    try:
        d=_call('/api/v1/sync/dashboard',payload,s['client_secret'])
        with write_transaction() as tx:
            tx.execute("UPDATE owner_cloud_settings SET last_sync_at=?,last_sync_status='SUCCESS',last_error=NULL,updated_at=? WHERE id=1",(_now(),_now()))
            tx.execute("INSERT INTO owner_cloud_sync_logs(status,message,created_at) VALUES('SUCCESS',?,?)",(f"Dashboard dan {len(report_bundle['reports'])} laporan berhasil disinkronkan.",_now()))
        return {'status':'SUCCESS','cloud':d,'settings':status()}
    except Exception as e:
        with write_transaction() as tx:
            tx.execute("UPDATE owner_cloud_settings SET last_sync_status='ERROR',last_error=?,updated_at=? WHERE id=1",(str(e),_now()))
            tx.execute("INSERT INTO owner_cloud_sync_logs(status,message,created_at) VALUES('ERROR',?,?)",(str(e),_now()))
        raise

def logs(limit=50):
    c=connect()
    try:return [dict(x) for x in c.execute("SELECT * FROM owner_cloud_sync_logs ORDER BY id DESC LIMIT ?",(max(1,min(200,int(limit))),)).fetchall()]
    finally:c.close()
