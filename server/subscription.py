from datetime import datetime, timezone
import calendar, os, hmac

TRIAL_DAYS = 7
TRIAL_USERS = 2
PLANS = {
    'YEAR': {'code':'YEAR','label':'1 Tahun','months':12,'base_price':2000000,'base_users':2,'addon_price':200000},
    'HALF': {'code':'HALF','label':'6 Bulan','months':6,'base_price':1200000,'base_users':2,'addon_price':100000},
}

def _now(): return datetime.now(timezone.utc)
def _iso(dt): return dt.astimezone(timezone.utc).isoformat()
def _parse(v):
    if not v:return None
    try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).astimezone(timezone.utc)
    except Exception:return None

def _add_months(dt, months):
    m=dt.month-1+months; y=dt.year+m//12; mo=m%12+1
    day=min(dt.day, calendar.monthrange(y,mo)[1])
    return dt.replace(year=y,month=mo,day=day)

def ensure_schema(c):
    c.execute('''CREATE TABLE IF NOT EXISTS web_subscription(
      id INTEGER PRIMARY KEY CHECK(id=1), status TEXT NOT NULL DEFAULT 'TRIAL',
      trial_started_at TEXT NOT NULL, trial_expires_at TEXT NOT NULL,
      plan_code TEXT, started_at TEXT, expires_at TEXT,
      base_users INTEGER NOT NULL DEFAULT 2, addon_users INTEGER NOT NULL DEFAULT 0,
      amount NUMERIC NOT NULL DEFAULT 0, customer_name TEXT, notes TEXT,
      updated_at TEXT NOT NULL)''')
    if not c.execute('SELECT 1 FROM web_subscription WHERE id=1').fetchone():
        n=_now(); e=n.replace(microsecond=0)
        from datetime import timedelta
        e=e+timedelta(days=TRIAL_DAYS)
        c.execute('''INSERT INTO web_subscription(id,status,trial_started_at,trial_expires_at,base_users,addon_users,amount,updated_at)
                     VALUES(1,'TRIAL',?,?,?,0,0,?)''',(_iso(n),_iso(e),TRIAL_USERS,_iso(n)))

def catalog(): return list(PLANS.values())

def validate_admin_key(value):
    configured=str(os.environ.get('STOKLEDGER_LICENSE_ADMIN_KEY','')).strip()
    if len(configured)<8: raise ValueError('STOKLEDGER_LICENSE_ADMIN_KEY belum dikonfigurasi di server.')
    if not hmac.compare_digest(str(value or ''), configured): raise ValueError('Kunci Admin Aktivasi tidak valid.')
    return True

def status(c):
    ensure_schema(c); r=c.execute('SELECT * FROM web_subscription WHERE id=1').fetchone(); n=_now()
    plan=PLANS.get(r['plan_code']) if r['plan_code'] else None
    if r['status']=='ACTIVE' and _parse(r['expires_at']) and _parse(r['expires_at'])>n:
        exp=_parse(r['expires_at']); mode='SUBSCRIPTION'; valid=True
    elif r['status']=='ACTIVE':
        exp=_parse(r['expires_at']); mode='SUBSCRIPTION_EXPIRED'; valid=False
    else:
        exp=_parse(r['trial_expires_at']); valid=bool(exp and exp>n); mode='TRIAL' if valid else 'TRIAL_EXPIRED'
    secs=max(0,(exp-n).total_seconds()) if exp else 0
    return {'mode':mode,'license_type':'WEB_SUBSCRIPTION','license_valid':valid,'plan_code':r['plan_code'],
      'plan_name':plan['label'] if plan else 'Trial 7 Hari','trial_started_at':r['trial_started_at'],'trial_expires_at':r['trial_expires_at'],
      'started_at':r['started_at'],'expires_at':r['expires_at'],'days_remaining':int((secs+86399)//86400),
      'base_users':int(r['base_users'] or TRIAL_USERS),'addon_users':int(r['addon_users'] or 0),
      'max_users':int(r['base_users'] or TRIAL_USERS)+int(r['addon_users'] or 0),'device_limit':int(r['base_users'] or TRIAL_USERS)+int(r['addon_users'] or 0),
      'amount':float(r['amount'] or 0),'customer_name':r['customer_name'] or '','notes':r['notes'] or '',
      'transaction_limit':None,'transactions_remaining':None}

def activate(c, plan_code, addon_users=0, customer_name='', notes='', starts_at=None):
    ensure_schema(c); p=PLANS.get(str(plan_code or '').upper())
    if not p: raise ValueError('Paket langganan tidak valid.')
    addon=max(0,int(addon_users or 0)); start=_parse(starts_at) or _now(); exp=_add_months(start,p['months'])
    amount=p['base_price']+addon*p['addon_price']; n=_iso(_now())
    c.execute('''UPDATE web_subscription SET status='ACTIVE',plan_code=?,started_at=?,expires_at=?,base_users=?,addon_users=?,amount=?,customer_name=?,notes=?,updated_at=? WHERE id=1''',
      (p['code'],_iso(start),_iso(exp),p['base_users'],addon,amount,str(customer_name or ''),str(notes or ''),n))
    return status(c)

def reset_trial(c):
    from datetime import timedelta
    ensure_schema(c); n=_now(); exp=n+timedelta(days=TRIAL_DAYS)
    c.execute('''UPDATE web_subscription SET status='TRIAL',plan_code=NULL,started_at=NULL,expires_at=NULL,base_users=?,addon_users=0,amount=0,trial_started_at=?,trial_expires_at=?,updated_at=? WHERE id=1''',(TRIAL_USERS,_iso(n),_iso(exp),_iso(n)))
    return status(c)
