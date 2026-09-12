from __future__ import annotations
import os, re, json, hmac, secrets
from datetime import datetime, timezone, timedelta
from .config import DATABASE_URL, IS_POSTGRES
from . import pg_compat, subscription
from . import hardening
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
        CREATE TABLE IF NOT EXISTS saas_security_attempts(
          scope TEXT NOT NULL, identifier TEXT NOT NULL, client_ip TEXT NOT NULL,
          fail_count INTEGER NOT NULL DEFAULT 0, window_started_at TEXT NOT NULL,
          blocked_until TEXT, updated_at TEXT NOT NULL,
          PRIMARY KEY(scope,identifier,client_ip)
        );
        CREATE TABLE IF NOT EXISTS saas_rate_limits(
          scope TEXT NOT NULL, rate_key TEXT NOT NULL, client_ip TEXT NOT NULL,
          hit_count INTEGER NOT NULL DEFAULT 0, window_started_at TEXT NOT NULL, updated_at TEXT NOT NULL,
          PRIMARY KEY(scope,rate_key,client_ip)
        );
        CREATE TABLE IF NOT EXISTS saas_security_audit(
          id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT NOT NULL, account_id INTEGER,
          identifier TEXT, client_ip TEXT, details_json TEXT NOT NULL DEFAULT '{}', created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_saas_security_audit_created ON saas_security_audit(created_at);
        CREATE TABLE IF NOT EXISTS saas_tenant_users(
          account_id INTEGER NOT NULL,
          schema_name TEXT NOT NULL,
          username TEXT NOT NULL,
          is_active INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          PRIMARY KEY(account_id,username)
        );
        CREATE INDEX IF NOT EXISTS idx_saas_tenant_users_username ON saas_tenant_users(lower(username));
        CREATE INDEX IF NOT EXISTS idx_saas_tenant_users_schema ON saas_tenant_users(schema_name);
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

def security_audit(event_type, account_id=None, identifier='', client_ip='', details=None):
    try:
        ensure_schema(); c=_public()
        try:c.execute("INSERT INTO saas_security_audit(event_type,account_id,identifier,client_ip,details_json,created_at) VALUES(?,?,?,?,?,?)",(str(event_type or '')[:80],int(account_id) if account_id else None,str(identifier or '')[:180],str(client_ip or '')[:80],json.dumps(details or {},ensure_ascii=False),_iso()));c.commit()
        finally:c.close()
        return True
    except Exception:return False

def list_security_audit(limit=250):
    ensure_schema(); c=_public()
    try:
        rows=c.execute('SELECT * FROM saas_security_audit ORDER BY id DESC LIMIT ?',(max(1,min(1000,int(limit or 250))),)).fetchall();out=[]
        for r in rows:
            d=dict(r)
            try:d['details']=json.loads(d.pop('details_json') or '{}')
            except Exception:d['details']={}
            out.append(d)
        return out
    finally:c.close()

def auth_rate_check(scope,identifier,client_ip,max_failures=5,window_minutes=15,block_minutes=15):
    ensure_schema();scope=str(scope or '').upper()[:40];ident=str(identifier or '').strip().lower()[:180] or '-';ip=str(client_ip or '')[:80] or '-';now=_now();c=_public()
    try:
        r=c.execute('SELECT * FROM saas_security_attempts WHERE scope=? AND identifier=? AND client_ip=?',(scope,ident,ip)).fetchone()
        if not r:return True
        blocked=_parse(r['blocked_until'])
        if blocked and blocked>now:
            wait=max(1,int(((blocked-now).total_seconds()+59)//60));raise ValueError(f'Terlalu banyak percobaan login. Coba lagi sekitar {wait} menit.')
        started=_parse(r['window_started_at'])
        if not started or (now-started)>timedelta(minutes=max(1,int(window_minutes))):c.execute('DELETE FROM saas_security_attempts WHERE scope=? AND identifier=? AND client_ip=?',(scope,ident,ip));c.commit()
        return True
    finally:c.close()

def auth_rate_failure(scope,identifier,client_ip,max_failures=5,window_minutes=15,block_minutes=15,account_id=None):
    ensure_schema();scope=str(scope or '').upper()[:40];ident=str(identifier or '').strip().lower()[:180] or '-';ip=str(client_ip or '')[:80] or '-';now=_now();c=_public()
    try:
        r=c.execute('SELECT * FROM saas_security_attempts WHERE scope=? AND identifier=? AND client_ip=?',(scope,ident,ip)).fetchone();started=_parse(r['window_started_at']) if r else None
        if not r or not started or (now-started)>timedelta(minutes=max(1,int(window_minutes))):count=1;started=now
        else:count=int(r['fail_count'] or 0)+1
        blocked=(now+timedelta(minutes=max(1,int(block_minutes)))) if count>=max(1,int(max_failures)) else None
        c.execute("INSERT INTO saas_security_attempts(scope,identifier,client_ip,fail_count,window_started_at,blocked_until,updated_at) VALUES(?,?,?,?,?,?,?) ON CONFLICT(scope,identifier,client_ip) DO UPDATE SET fail_count=excluded.fail_count,window_started_at=excluded.window_started_at,blocked_until=excluded.blocked_until,updated_at=excluded.updated_at",(scope,ident,ip,count,_iso(started),_iso(blocked) if blocked else None,_iso(now)));c.commit()
    finally:c.close()
    security_audit(scope+'_FAILED',account_id,ident,ip,{'fail_count':count,'blocked':bool(blocked)});return count

def auth_rate_success(scope,identifier,client_ip,account_id=None):
    scope=str(scope or '').upper()[:40];ident=str(identifier or '').strip().lower()[:180] or '-';ip=str(client_ip or '')[:80] or '-';c=_public()
    try:c.execute('DELETE FROM saas_security_attempts WHERE scope=? AND identifier=? AND client_ip=?',(scope,ident,ip));c.commit()
    finally:c.close()
    security_audit(scope+'_SUCCESS',account_id,ident,ip,{})

def consume_rate_limit(scope,rate_key,client_ip,max_hits=5,window_minutes=60):
    ensure_schema();scope=str(scope or '').upper()[:40];key=str(rate_key or '').strip().lower()[:180] or '-';ip=str(client_ip or '')[:80] or '-';now=_now();c=_public()
    try:
        r=c.execute('SELECT * FROM saas_rate_limits WHERE scope=? AND rate_key=? AND client_ip=?',(scope,key,ip)).fetchone();started=_parse(r['window_started_at']) if r else None
        if not r or not started or (now-started)>timedelta(minutes=max(1,int(window_minutes))):count=1;started=now
        else:count=int(r['hit_count'] or 0)+1
        if count>max(1,int(max_hits)):
            wait=max(1,int(((timedelta(minutes=max(1,int(window_minutes)))-(now-started)).total_seconds()+59)//60));raise ValueError(f'Terlalu banyak permintaan. Coba lagi sekitar {wait} menit.')
        c.execute("INSERT INTO saas_rate_limits(scope,rate_key,client_ip,hit_count,window_started_at,updated_at) VALUES(?,?,?,?,?,?) ON CONFLICT(scope,rate_key,client_ip) DO UPDATE SET hit_count=excluded.hit_count,window_started_at=excluded.window_started_at,updated_at=excluded.updated_at",(scope,key,ip,count,_iso(started),_iso(now)));c.commit();return count
    finally:c.close()

def security_status():return {'owner_2fa_configured':hardening.owner_totp_configured(),'login_lockout':'5 kegagalan / 15 menit','signup_rate_limit':'5 akun / IP / 60 menit','owner_session_hours':4,'tenant_isolation':'PostgreSQL schema + session binding','token_storage':'sessionStorage','security_headers':True}

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



def account_by_code(account_code):
    ensure_schema(); c=_public()
    try:return _account_dict(c.execute('SELECT * FROM saas_accounts WHERE upper(account_code)=upper(?)',(str(account_code or '').strip(),)).fetchone())
    finally:c.close()

def register_tenant_user(schema_name, username, is_active=True):
    schema_name=str(schema_name or '').strip(); username=str(username or '').strip()
    if not schema_name or not username:return None
    account=account_by_schema(schema_name)
    if not account:return None
    ensure_schema(); now=_iso(); c=_public()
    try:
        c.execute('''INSERT INTO saas_tenant_users(account_id,schema_name,username,is_active,created_at,updated_at)
          VALUES(?,?,?,?,?,?) ON CONFLICT(account_id,username) DO UPDATE SET schema_name=excluded.schema_name,is_active=excluded.is_active,updated_at=excluded.updated_at''',
          (int(account['id']),schema_name,username,1 if is_active else 0,now,now))
        c.commit()
    finally:c.close()
    return account

def set_tenant_user_active(schema_name, username, is_active):
    schema_name=str(schema_name or '').strip(); username=str(username or '').strip()
    if not schema_name or not username:return None
    register_tenant_user(schema_name,username,is_active)
    c=_public()
    try:
        c.execute('UPDATE saas_tenant_users SET is_active=?,updated_at=? WHERE schema_name=? AND lower(username)=lower(?)',
          (1 if is_active else 0,_iso(),schema_name,username)); c.commit()
    finally:c.close()
    return True

def _tenant_user_exists(schema_name, username):
    if not schema_name or not username:return False
    try:
        c=pg_compat.connect(DATABASE_URL,schema=schema_name)
        try:return bool(c.execute('SELECT 1 FROM users WHERE lower(username)=lower(?) LIMIT 1',(str(username).strip(),)).fetchone())
        finally:c.close()
    except Exception:
        return False

def account_for_user_login(login_name):
    """Resolve non-owner tenant users to their company schema.

    Supports plain username when it is unique across tenants and ACCOUNT_CODE/username
    when the same username exists in more than one company. Existing users created on
    older builds are discovered lazily and backfilled into saas_tenant_users.
    """
    ensure_schema(); raw=str(login_name or '').strip()
    if not raw:return None,None
    account_code=None; username=raw
    if '/' in raw:
        prefix,rest=raw.split('/',1)
        if prefix.strip() and rest.strip(): account_code=prefix.strip(); username=rest.strip()
    if account_code:
        acc=account_by_code(account_code)
        if acc and _tenant_user_exists(acc['schema_name'],username):
            register_tenant_user(acc['schema_name'],username,True)
            return acc,username
        return None,username
    c=_public()
    try:
        rows=c.execute('''SELECT a.* FROM saas_tenant_users u JOIN saas_accounts a ON a.id=u.account_id
          WHERE lower(u.username)=lower(?) AND u.is_active=1 ORDER BY a.id''',(username,)).fetchall()
    finally:c.close()
    if len(rows)==1:return _account_dict(rows[0]),username
    if len(rows)>1:raise ValueError('Username dipakai di lebih dari satu perusahaan. Login dengan format KODE_AKUN/username.')
    # Backward-compatible discovery for users created before the login index existed.
    c=_public()
    try:accounts=[_account_dict(x) for x in c.execute('SELECT * FROM saas_accounts ORDER BY id').fetchall()]
    finally:c.close()
    found=[]
    for acc in accounts:
        if _tenant_user_exists(acc.get('schema_name'),username):
            register_tenant_user(acc['schema_name'],username,True); found.append(acc)
    if len(found)==1:return found[0],username
    if len(found)>1:raise ValueError('Username dipakai di lebih dari satu perusahaan. Login dengan format KODE_AKUN/username.')
    return None,username

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
        register_tenant_user(schema,email,True)
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

def owner_login(password, otp=''):
    configured=str(os.environ.get('STOKLEDGER_OWNER_ADMIN_PASSWORD') or os.environ.get('STOKLEDGER_LICENSE_ADMIN_KEY') or '').strip()
    if len(configured)<12: raise ValueError('STOKLEDGER_OWNER_ADMIN_PASSWORD minimal 12 karakter.')
    if not hardening.owner_totp_configured(): raise ValueError('2FA Owner Admin belum dikonfigurasi. Set STOKLEDGER_OWNER_TOTP_SECRET di Railway.')
    if not hmac.compare_digest(str(password or ''),configured): raise ValueError('Password Owner Admin salah.')
    if not hardening.verify_owner_totp(otp): raise ValueError('Kode authenticator tidak valid atau sudah kedaluwarsa.')
    ensure_schema(); token=secrets.token_urlsafe(40); now=_now(); exp=now+timedelta(hours=4); c=_public()
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


def reset_primary_admin_password(account_id, client_ip=''):
    from .database import tenant_scope, write_transaction, ensure_password_security_schema
    a=account_by_id(account_id)
    if not a: raise ValueError('Akun tidak ditemukan.')
    alphabet='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%'
    temporary=''.join(secrets.choice(alphabet) for _ in range(14))
    with tenant_scope(a['schema_name']):
        ensure_password_security_schema()
        with write_transaction() as tx:
            user=tx.execute("SELECT u.id,u.username FROM users u JOIN roles r ON r.id=u.role_id WHERE lower(u.username)=lower(?) AND r.code='ADMIN' ORDER BY u.id LIMIT 1",(a['email'],)).fetchone()
            if not user:user=tx.execute("SELECT u.id,u.username FROM users u JOIN roles r ON r.id=u.role_id WHERE r.code='ADMIN' AND u.is_active=1 ORDER BY u.id LIMIT 1").fetchone()
            if not user: raise ValueError('Administrator utama akun tidak ditemukan.')
            tx.execute("UPDATE users SET password_hash=?,must_change_password=1,updated_at=? WHERE id=?",(hash_password(temporary),_iso(),user['id']))
            tx.execute("DELETE FROM sessions WHERE user_id=?",(user['id'],))
    c=_public()
    try:c.execute('DELETE FROM saas_sessions WHERE account_id=?',(int(account_id),));c.commit()
    finally:c.close()
    security_audit('OWNER_ADMIN_PASSWORD_RESET',int(account_id),a.get('email') or '',client_ip,{'username':user['username']})
    return {'username':user['username'],'temporary_password':temporary,'must_change_password':True}

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
