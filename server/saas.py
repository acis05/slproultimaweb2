from __future__ import annotations
import os, re, json, hmac, secrets
from datetime import datetime, timezone, timedelta
from .config import DATABASE_URL, IS_POSTGRES
from . import pg_compat, subscription
from .security import hash_password, verify_password

EMAIL_RE=re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

def _now(): return datetime.now(timezone.utc)
def _iso(v=None): return (v or _now()).astimezone(timezone.utc).isoformat()
def _parse(v):
    if not v:return None
    try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).astimezone(timezone.utc)
    except Exception:return None

def _public():
    if not IS_POSTGRES or not DATABASE_URL: raise RuntimeError('Platform akun Web memerlukan PostgreSQL DATABASE_URL.')
    return pg_compat.connect(DATABASE_URL, schema='public')

def ensure_schema():
    c=_public()
    try:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS saas_accounts(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          account_code TEXT NOT NULL UNIQUE,
          schema_name TEXT NOT NULL UNIQUE,
          company_name TEXT NOT NULL,
          owner_name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          phone TEXT,
          status TEXT NOT NULL DEFAULT 'TRIAL',
          trial_started_at TEXT NOT NULL,
          trial_expires_at TEXT NOT NULL,
          plan_code TEXT,
          started_at TEXT,
          expires_at TEXT,
          base_users INTEGER NOT NULL DEFAULT 2,
          addon_users INTEGER NOT NULL DEFAULT 0,
          amount NUMERIC NOT NULL DEFAULT 0,
          discount_code TEXT,
          discount_amount NUMERIC NOT NULL DEFAULT 0,
          notes TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_saas_accounts_email ON saas_accounts(email);
        CREATE INDEX IF NOT EXISTS idx_saas_accounts_status ON saas_accounts(status,trial_expires_at,expires_at);
        CREATE TABLE IF NOT EXISTS saas_sessions(
          token TEXT PRIMARY KEY,
          account_id INTEGER NOT NULL,
          schema_name TEXT NOT NULL,
          created_at TEXT NOT NULL,
          expires_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_saas_sessions_account ON saas_sessions(account_id);
        CREATE TABLE IF NOT EXISTS saas_owner_sessions(
          token TEXT PRIMARY KEY,
          created_at TEXT NOT NULL,
          expires_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS saas_discount_codes(
          code TEXT PRIMARY KEY,
          discount_type TEXT NOT NULL,
          discount_value NUMERIC NOT NULL,
          valid_from TEXT,
          valid_until TEXT,
          max_uses INTEGER,
          used_count INTEGER NOT NULL DEFAULT 0,
          plans_json TEXT NOT NULL DEFAULT '[]',
          is_active INTEGER NOT NULL DEFAULT 1,
          notes TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        ''')
        c.commit()
    finally:c.close()

def _account_dict(r):
    if not r:return None
    d=dict(r)
    n=_now(); mode=d.get('status')
    if mode=='ACTIVE' and _parse(d.get('expires_at')) and _parse(d.get('expires_at'))<=n: mode='EXPIRED'
    if mode=='TRIAL' and _parse(d.get('trial_expires_at')) and _parse(d.get('trial_expires_at'))<=n: mode='TRIAL_EXPIRED'
    d['effective_status']=mode
    exp=_parse(d.get('expires_at')) if d.get('status')=='ACTIVE' else _parse(d.get('trial_expires_at'))
    d['days_remaining']=max(0,int(((exp-n).total_seconds()+86399)//86400)) if exp else 0
    d['max_users']=int(d.get('base_users') or 2)+int(d.get('addon_users') or 0)
    return d

def account_by_email(email):
    ensure_schema(); c=_public()
    try:return _account_dict(c.execute('SELECT * FROM saas_accounts WHERE lower(email)=lower(?)',(str(email or '').strip(),)).fetchone())
    finally:c.close()

def account_by_id(account_id):
    ensure_schema(); c=_public()
    try:return _account_dict(c.execute('SELECT * FROM saas_accounts WHERE id=?',(int(account_id),)).fetchone())
    finally:c.close()

def register_account(data):
    ensure_schema()
    company=str(data.get('company_name') or '').strip()
    owner=str(data.get('owner_name') or '').strip()
    email=str(data.get('email') or '').strip().lower()
    phone=str(data.get('phone') or '').strip()
    password=str(data.get('password') or '')
    if len(company)<2: raise ValueError('Nama perusahaan wajib diisi.')
    if len(owner)<2: raise ValueError('Nama pemilik/admin wajib diisi.')
    if not EMAIL_RE.match(email): raise ValueError('Email tidak valid.')
    if len(password)<8: raise ValueError('Password minimal 8 karakter.')
    if account_by_email(email): raise ValueError('Email sudah terdaftar. Silakan login.')
    code='SLW-'+secrets.token_hex(4).upper()
    schema='tenant_'+secrets.token_hex(8)
    now=_now(); exp=now+timedelta(days=subscription.TRIAL_DAYS)
    c=_public()
    try:
        cur=c.execute('''INSERT INTO saas_accounts(account_code,schema_name,company_name,owner_name,email,phone,status,trial_started_at,trial_expires_at,base_users,addon_users,amount,created_at,updated_at)
          VALUES(?,?,?,?,?,?,'TRIAL',?,?,?,0,0,?,?)''',(code,schema,company,owner,email,phone,_iso(now),_iso(exp),subscription.TRIAL_USERS,_iso(now),_iso(now)))
        account_id=cur.lastrowid
        c.commit()
    finally:c.close()
    try:
        from .database import init_tenant
        init_tenant(schema,email,owner,password,company)
    except Exception:
        c=_public()
        try:
            c.execute('DELETE FROM saas_accounts WHERE id=?',(account_id,)); c.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'); c.commit()
        finally:c.close()
        raise
    return account_by_id(account_id)

def bind_session(token, account_id, schema_name, hours=12):
    ensure_schema(); now=_now(); exp=now+timedelta(hours=max(1,int(hours or 12)))
    c=_public()
    try:
        c.execute('DELETE FROM saas_sessions WHERE expires_at<=?',(_iso(now),))
        c.execute('INSERT INTO saas_sessions(token,account_id,schema_name,created_at,expires_at) VALUES(?,?,?,?,?) ON CONFLICT(token) DO UPDATE SET account_id=excluded.account_id,schema_name=excluded.schema_name,expires_at=excluded.expires_at',(token,int(account_id),schema_name,_iso(now),_iso(exp)))
        c.commit()
    finally:c.close()

def session_info(token):
    if not token:return None
    ensure_schema(); c=_public()
    try:
        r=c.execute('''SELECT s.*,a.status account_status,a.email,a.company_name FROM saas_sessions s JOIN saas_accounts a ON a.id=s.account_id WHERE s.token=? AND s.expires_at>?''',(token,_iso())).fetchone()
        return dict(r) if r else None
    finally:c.close()

def remove_session(token):
    if not token:return
    c=_public()
    try:c.execute('DELETE FROM saas_sessions WHERE token=?',(token,));c.commit()
    finally:c.close()

def owner_login(password):
    configured=str(os.environ.get('STOKLEDGER_OWNER_ADMIN_PASSWORD') or os.environ.get('STOKLEDGER_LICENSE_ADMIN_KEY') or '').strip()
    if len(configured)<8: raise ValueError('STOKLEDGER_OWNER_ADMIN_PASSWORD belum dikonfigurasi di Railway Variables.')
    if not hmac.compare_digest(str(password or ''),configured): raise ValueError('Password Owner Admin salah.')
    ensure_schema(); token=secrets.token_urlsafe(40); now=_now(); exp=now+timedelta(hours=8); c=_public()
    try:
        c.execute('DELETE FROM saas_owner_sessions WHERE expires_at<=?',(_iso(now),))
        c.execute('INSERT INTO saas_owner_sessions(token,created_at,expires_at) VALUES(?,?,?)',(token,_iso(now),_iso(exp))); c.commit()
    finally:c.close()
    return token

def owner_authenticated(token):
    if not token:return False
    ensure_schema(); c=_public()
    try:return bool(c.execute('SELECT 1 FROM saas_owner_sessions WHERE token=? AND expires_at>?',(token,_iso())).fetchone())
    finally:c.close()

def list_accounts(q='',status=''):
    ensure_schema(); c=_public()
    try:
        clauses=[];params=[]
        if q:
            clauses.append('(lower(company_name) LIKE ? OR lower(email) LIKE ? OR lower(account_code) LIKE ?)'); v='%'+str(q).lower()+'%';params += [v,v,v]
        if status:
            clauses.append('status=?');params.append(str(status).upper())
        sql='SELECT * FROM saas_accounts'+((' WHERE '+' AND '.join(clauses)) if clauses else '')+' ORDER BY id DESC'
        return [_account_dict(r) for r in c.execute(sql,params).fetchall()]
    finally:c.close()

def set_account_status(account_id,status):
    status=str(status or '').upper()
    if status not in ('TRIAL','ACTIVE','SUSPENDED'): raise ValueError('Status akun tidak valid.')
    existing=account_by_id(account_id)
    if not existing: raise ValueError('Akun tidak ditemukan.')
    if status=='TRIAL' and existing.get('plan_code') and _parse(existing.get('expires_at')) and _parse(existing.get('expires_at'))>_now():
        status='ACTIVE'
    c=_public(); now=_iso()
    try:c.execute('UPDATE saas_accounts SET status=?,updated_at=? WHERE id=?',(status,now,int(account_id)));c.commit()
    finally:c.close()
    return account_by_id(account_id)

def reset_trial(account_id):
    from .database import tenant_scope, write_transaction
    a=account_by_id(account_id)
    if not a: raise ValueError('Akun tidak ditemukan.')
    now=_now(); exp=now+timedelta(days=subscription.TRIAL_DAYS)
    with tenant_scope(a['schema_name']):
        with write_transaction() as tx: subscription.reset_trial(tx)
    c=_public()
    try:
        c.execute("UPDATE saas_accounts SET status='TRIAL',plan_code=NULL,started_at=NULL,expires_at=NULL,base_users=?,addon_users=0,amount=0,discount_code=NULL,discount_amount=0,trial_started_at=?,trial_expires_at=?,updated_at=? WHERE id=?",(subscription.TRIAL_USERS,_iso(now),_iso(exp),_iso(now),int(account_id)));c.commit()
    finally:c.close()
    return account_by_id(account_id)

def list_discounts():
    ensure_schema(); c=_public()
    try:return [dict(r) for r in c.execute('SELECT * FROM saas_discount_codes ORDER BY code').fetchall()]
    finally:c.close()

def save_discount(data):
    ensure_schema(); code=str(data.get('code') or '').strip().upper().replace(' ','-')
    typ=str(data.get('discount_type') or 'PERCENT').upper(); value=float(data.get('discount_value') or 0)
    if not code or not re.match(r'^[A-Z0-9_-]{3,30}$',code): raise ValueError('Kode diskon 3-30 karakter: huruf, angka, - atau _.')
    if typ not in ('PERCENT','FIXED'): raise ValueError('Tipe diskon harus PERCENT atau FIXED.')
    if value<=0 or (typ=='PERCENT' and value>100): raise ValueError('Nilai diskon tidak valid.')
    plans=data.get('plans') or []
    if isinstance(plans,str): plans=[x.strip().upper() for x in plans.split(',') if x.strip()]
    plans=[p for p in plans if p in subscription.PLANS]
    max_uses=data.get('max_uses'); max_uses=int(max_uses) if str(max_uses or '').strip() else None
    vf=str(data.get('valid_from') or '').strip() or None; vu=str(data.get('valid_until') or '').strip() or None
    notes=str(data.get('notes') or '').strip(); active=1 if data.get('is_active',True) else 0; now=_iso(); c=_public()
    try:
        c.execute('''INSERT INTO saas_discount_codes(code,discount_type,discount_value,valid_from,valid_until,max_uses,used_count,plans_json,is_active,notes,created_at,updated_at)
        VALUES(?,?,?,?,?,?,0,?,?,?,?,?) ON CONFLICT(code) DO UPDATE SET discount_type=excluded.discount_type,discount_value=excluded.discount_value,valid_from=excluded.valid_from,valid_until=excluded.valid_until,max_uses=excluded.max_uses,plans_json=excluded.plans_json,is_active=excluded.is_active,notes=excluded.notes,updated_at=excluded.updated_at''',
        (code,typ,value,vf,vu,max_uses,json.dumps(plans),active,notes,now,now)); c.commit()
    finally:c.close()
    return code

def delete_discount(code):
    c=_public()
    try:c.execute('DELETE FROM saas_discount_codes WHERE code=?',(str(code).upper(),));c.commit()
    finally:c.close()

def _discount(code,plan_code,gross):
    if not code:return 0,None
    c=_public()
    try:r=c.execute('SELECT * FROM saas_discount_codes WHERE code=?',(str(code).strip().upper(),)).fetchone()
    finally:c.close()
    if not r or not r['is_active']: raise ValueError('Kode diskon tidak aktif atau tidak ditemukan.')
    n=_now(); vf=_parse(r['valid_from']); vu=_parse(r['valid_until'])
    if vf and n<vf: raise ValueError('Kode diskon belum berlaku.')
    if vu and n>vu: raise ValueError('Kode diskon sudah kedaluwarsa.')
    if r['max_uses'] is not None and int(r['used_count'] or 0)>=int(r['max_uses']): raise ValueError('Kuota kode diskon sudah habis.')
    plans=json.loads(r['plans_json'] or '[]')
    if plans and plan_code not in plans: raise ValueError('Kode diskon tidak berlaku untuk paket ini.')
    amount=(gross*float(r['discount_value'])/100.0) if r['discount_type']=='PERCENT' else float(r['discount_value'])
    return min(gross,max(0,amount)),dict(r)

def activate_account(account_id,plan_code,addon_users=0,discount_code='',starts_at=None,notes=''):
    from .database import tenant_scope, write_transaction
    a=account_by_id(account_id)
    if not a: raise ValueError('Akun tidak ditemukan.')
    p=subscription.PLANS.get(str(plan_code or '').upper())
    if not p: raise ValueError('Paket langganan tidak valid.')
    addon=max(0,int(addon_users or 0)); gross=float(p['base_price']+addon*p['addon_price']); disc,discrow=_discount(discount_code,p['code'],gross); final=max(0,gross-disc)
    with tenant_scope(a['schema_name']):
        with write_transaction() as tx:
            st=subscription.activate(tx,p['code'],addon,a['company_name'],notes or '',starts_at,amount_override=final)
    c=_public(); now=_iso()
    try:
        c.execute('''UPDATE saas_accounts SET status='ACTIVE',plan_code=?,started_at=?,expires_at=?,base_users=?,addon_users=?,amount=?,discount_code=?,discount_amount=?,notes=?,updated_at=? WHERE id=?''',
          (p['code'],st['started_at'],st['expires_at'],p['base_users'],addon,final,str(discount_code or '').strip().upper() or None,disc,str(notes or ''),now,int(account_id)))
        if discrow:c.execute('UPDATE saas_discount_codes SET used_count=used_count+1,updated_at=? WHERE code=?',(now,discrow['code']))
        c.commit()
    finally:c.close()
    return account_by_id(account_id)

def account_by_schema(schema_name):
    if not schema_name:return None
    ensure_schema(); c=_public()
    try:return _account_dict(c.execute('SELECT * FROM saas_accounts WHERE schema_name=?',(str(schema_name),)).fetchone())
    finally:c.close()

def sync_account_subscription(schema_name, st):
    a=account_by_schema(schema_name)
    if not a:return None
    mode=str(st.get('mode') or '')
    raw_status='ACTIVE' if mode=='SUBSCRIPTION' else 'TRIAL' if mode.startswith('TRIAL') else a.get('status') or 'TRIAL'
    c=_public(); now=_iso()
    try:
        c.execute('''UPDATE saas_accounts SET status=?,plan_code=?,started_at=?,expires_at=?,trial_started_at=?,trial_expires_at=?,base_users=?,addon_users=?,amount=?,company_name=COALESCE(NULLIF(?,''),company_name),notes=?,updated_at=? WHERE id=?''',
          (raw_status,st.get('plan_code'),st.get('started_at'),st.get('expires_at'),st.get('trial_started_at'),st.get('trial_expires_at'),int(st.get('base_users') or 2),int(st.get('addon_users') or 0),float(st.get('amount') or 0),st.get('customer_name') or '',st.get('notes') or '',now,a['id']))
        c.commit()
    finally:c.close()
    return account_by_id(a['id'])
