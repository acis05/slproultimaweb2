from __future__ import annotations
import shutil, sqlite3
from datetime import datetime
from pathlib import Path

TARGET_SCHEMA_VERSION = 1310
LEGACY_PREFIX = 'legacy_standard_'

INCOMPATIBLE = {
 'users':'role_id',
 'sales':'sale_date',
 'purchases':'purchase_date',
 'journal_entries':'journal_date',
 'journal_lines':'journal_id',
 'cash_transactions':'transaction_no',
 'receivable_payments':'payment_no',
 'payable_payments':'payment_no',
 'audit_logs':'user_id',
}
OPTIONAL_RENAME = ['sales_lines','purchase_lines']

def _tables(c):
 return {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}

def _cols(c,t):
 return {r[1] for r in c.execute(f'PRAGMA table_info("{t}")')}

def detect_database(path):
 p=Path(path)
 if not p.exists() or p.stat().st_size<16: return {'kind':'NEW','needs_migration':False}
 with sqlite3.connect(p) as c:
  tabs=_tables(c)
  if 'sales' in tabs:
   cols=_cols(c,'sales')
   if 'trx_date' in cols and 'sale_date' not in cols:
    return {'kind':'STANDARD','needs_migration':True,'schema_version':0}
  if 'app_metadata' in tabs:
   try:
    v=c.execute("SELECT value FROM app_metadata WHERE key='schema_version'").fetchone()
    return {'kind':'PRO','needs_migration':False,'schema_version':int(v[0]) if v else None}
   except Exception: pass
  return {'kind':'PRO','needs_migration':False,'schema_version':None}

def backup_before_upgrade(path, backup_dir=None):
 p=Path(path); d=Path(backup_dir) if backup_dir else p.parent/'backups'; d.mkdir(parents=True,exist_ok=True)
 target=d/f'{p.stem}_before_upgrade_{datetime.now():%Y%m%d_%H%M%S}.db'
 src=sqlite3.connect(str(p)); dst=sqlite3.connect(str(target))
 try: src.backup(dst); dst.commit()
 finally: dst.close(); src.close()
 return target

def prepare_legacy_schema(path, edition, backup_dir=None):
 info=detect_database(path)
 if not info['needs_migration']: return None
 backup=backup_before_upgrade(path,backup_dir)
 with sqlite3.connect(path) as c:
  c.execute('PRAGMA foreign_keys=OFF')
  tabs=_tables(c)
  for table, required in INCOMPATIBLE.items():
   if table in tabs and required not in _cols(c,table):
    dst=LEGACY_PREFIX+table
    if dst not in tabs: c.execute(f'ALTER TABLE "{table}" RENAME TO "{dst}"'); tabs.add(dst)
  # detail tables are tied to legacy headers and must be preserved separately
  for table in OPTIONAL_RENAME:
   if table in tabs:
    dst=LEGACY_PREFIX+table
    if dst not in tabs: c.execute(f'ALTER TABLE "{table}" RENAME TO "{dst}"'); tabs.add(dst)
  c.execute('CREATE TABLE IF NOT EXISTS app_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
  c.execute("INSERT OR REPLACE INTO app_metadata VALUES('migration_state','PREPARED')")
  c.execute("INSERT OR REPLACE INTO app_metadata VALUES('edition_created','STANDARD')")
  c.execute("INSERT OR REPLACE INTO app_metadata VALUES('current_edition',?)",(edition,))
  c.execute("INSERT OR REPLACE INTO app_metadata VALUES('backup_path',?)",(str(backup),))
  c.commit()
 return backup

def _account_type(t):
 x=(t or '').upper()
 if x in ('ASSET','ASET'): return 'ASSET','DEBIT'
 if x in ('LIABILITY','KEWAJIBAN','HUTANG'): return 'LIABILITY','CREDIT'
 if x in ('EQUITY','MODAL'): return 'EQUITY','CREDIT'
 if x in ('REVENUE','PENDAPATAN'): return 'REVENUE','CREDIT'
 return 'EXPENSE','DEBIT'

def migrate_legacy_data(c, edition, now):
 tabs=_tables(c)
 if 'app_metadata' in tabs:
  row=c.execute("SELECT value FROM app_metadata WHERE key='migration_state'").fetchone()
  if row and row[0]=='COMPLETED': return {'migrated':False,'already_completed':True}
 if LEGACY_PREFIX+'sales' not in tabs: return {'migrated':False}
 admin=c.execute("SELECT id FROM users WHERE username='admin' ORDER BY id LIMIT 1").fetchone()[0]
 wh=c.execute("SELECT id FROM warehouses WHERE is_default=1 ORDER BY id LIMIT 1").fetchone()[0]
 unit=c.execute("SELECT id FROM units ORDER BY id LIMIT 1").fetchone()[0]
 cat=c.execute("SELECT id FROM item_categories ORDER BY id LIMIT 1").fetchone()[0]
 inv=c.execute("SELECT id FROM chart_of_accounts WHERE code='1200'").fetchone()[0]
 sales_acc=c.execute("SELECT id FROM chart_of_accounts WHERE code='4000'").fetchone()[0]
 cogs=c.execute("SELECT id FROM chart_of_accounts WHERE code='5000'").fetchone()[0]

 # Accounts
 account_map={}
 if 'accounts' in tabs:
  for r in c.execute('SELECT id,code,name,type,active FROM accounts'):
   at,normal=_account_type(r[3]); code=str(r[1] or f'LEG-{r[0]}')
   c.execute('''INSERT INTO chart_of_accounts(code,name,account_type,normal_balance,is_system,is_active,created_at,updated_at)
    VALUES(?,?,?,?,0,?,?,?) ON CONFLICT(code) DO NOTHING''',(code,r[2] or code,at,normal,int(r[4] or 0),now,now))
   account_map[r[0]]=c.execute('SELECT id FROM chart_of_accounts WHERE code=?',(code,)).fetchone()[0]

 # Partners from legacy parties (existing business_partners are retained)
 partner_map={}
 if 'parties' in tabs:
  for r in c.execute('SELECT id,code,name,kind,phone,address,opening_balance,opening_date,active FROM parties'):
   kind=(r[3] or '').upper(); ptype='CUSTOMER' if 'CUSTOM' in kind or 'PELANG' in kind else ('SUPPLIER' if 'SUP' in kind or 'PEMAS' in kind else 'BOTH')
   code=(r[1] or f'LEG-P{r[0]}').strip()
   c.execute('''INSERT INTO business_partners(partner_type,code,name,phone,address,opening_balance,opening_balance_date,is_active,created_at,updated_at)
    VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(code) DO NOTHING''',(ptype,code,r[2] or code,r[4],r[5],float(r[6] or 0),r[7],int(r[8] or 0),now,now))
   partner_map[r[0]]=c.execute('SELECT id FROM business_partners WHERE code=?',(code,)).fetchone()[0]

 # Products from legacy items; existing products retained
 product_map={}
 if 'items' in tabs:
  for r in c.execute('SELECT id,sku,name,opening_date,stock,cost,price,min_stock,active FROM items'):
   sku=(r[1] or f'LEG-I{r[0]}').strip()
   c.execute('''INSERT INTO products(sku,name,category_id,unit_id,product_type,purchase_price,selling_price,stock_qty,minimum_stock,
    inventory_account_id,sales_account_id,cogs_account_id,is_active,created_at,updated_at,opening_balance_date)
    VALUES(?,?,?,?,'STOCK',?,?,?,?,?,?,?, ?,?,?,?) ON CONFLICT(sku) DO NOTHING''',
    (sku,r[2] or sku,cat,unit,float(r[5] or 0),float(r[6] or 0),float(r[4] or 0),float(r[7] or 0),inv,sales_acc,cogs,int(r[8] or 0),now,now,r[3]))
   product_map[r[0]]=c.execute('SELECT id FROM products WHERE sku=?',(sku,)).fetchone()[0]

 # map already existing partners/products by same legacy IDs as fallback
 for r in c.execute('SELECT id FROM business_partners'): partner_map.setdefault(r[0],r[0])
 for r in c.execute('SELECT id FROM products'): product_map.setdefault(r[0],r[0])

 sale_map={}
 ls=LEGACY_PREFIX+'sales'; lsl=LEGACY_PREFIX+'sales_lines'
 for r in c.execute(f'SELECT * FROM {ls} ORDER BY id'):
  customer=partner_map.get(r['customer_id']) if r['customer_id'] is not None else None
  status='POSTED' if int(r['active'] or 0) else 'VOID'; ptype='CREDIT' if float(r['balance'] or 0)>0 else 'CASH'
  cur=c.execute('''INSERT INTO sales(invoice_no,sale_date,customer_id,payment_type,subtotal,discount_amount,total_amount,paid_amount,balance_due,notes,status,user_id,created_at,updated_at,due_date,tax_amount,tax_percent,warehouse_id,payment_method)
   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(r['invoice_no'],r['trx_date'],customer,ptype,float(r['subtotal'] or 0),float(r['discount'] or 0),float(r['total'] or 0),float(r['paid'] or 0),float(r['balance'] or 0),r['note'],status,admin,now,now,r['due_date'],float(r['ppn_amount'] or 0),0,wh,'CREDIT' if ptype=='CREDIT' else 'CASH'))
  sale_map[r['id']]=cur.lastrowid
 if lsl in tabs:
  for r in c.execute(f'SELECT * FROM {lsl} ORDER BY id'):
   pid=product_map.get(r['item_id']); sid=sale_map.get(r['sale_id'])
   if not pid or not sid: continue
   p=c.execute('SELECT sku,product_type FROM products WHERE id=?',(pid,)).fetchone()
   c.execute('''INSERT INTO sales_items(sale_id,product_id,sku,product_name,product_type,qty,unit_price,discount_amount,line_total,purchase_price_snapshot,discount_percent)
    VALUES(?,?,?,?,?,?,?,?,?,?,0)''',(sid,pid,p['sku'],r['display_name'],p['product_type'],float(r['qty'] or 0),float(r['price'] or 0),float(r['discount'] or 0),float(r['line_total'] or 0),float(r['cost'] or 0)))

 purchase_map={}; lp=LEGACY_PREFIX+'purchases'; lpl=LEGACY_PREFIX+'purchase_lines'
 for r in c.execute(f'SELECT * FROM {lp} ORDER BY id'):
  supplier=partner_map.get(r['supplier_id'])
  if not supplier: continue
  status='POSTED' if int(r['active'] or 0) else 'VOID'; ptype='CREDIT' if float(r['balance'] or 0)>0 else 'CASH'
  cur=c.execute('''INSERT INTO purchases(purchase_no,supplier_invoice_no,purchase_date,supplier_id,warehouse_id,payment_type,subtotal,discount_amount,total_amount,paid_amount,balance_due,notes,status,user_id,created_at,updated_at,due_date,tax_amount,tax_percent,payment_method)
   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(r['invoice_no'],r['invoice_no'],r['trx_date'],supplier,wh,ptype,float(r['subtotal'] or 0),float(r['discount'] or 0),float(r['total'] or 0),float(r['paid'] or 0),float(r['balance'] or 0),r['note'],status,admin,now,now,r['due_date'],float(r['ppn_amount'] or 0),0,'CREDIT' if ptype=='CREDIT' else 'CASH'))
  purchase_map[r['id']]=cur.lastrowid
 if lpl in tabs:
  for r in c.execute(f'SELECT * FROM {lpl} ORDER BY id'):
   pid=product_map.get(r['item_id']); pur=purchase_map.get(r['purchase_id'])
   if not pid or not pur: continue
   p=c.execute('SELECT sku,product_type FROM products WHERE id=?',(pid,)).fetchone()
   c.execute('''INSERT INTO purchase_items(purchase_id,product_id,sku,product_name,product_type,qty,unit_cost,discount_amount,line_total,discount_percent)
    VALUES(?,?,?,?,?,?,?,?,?,0)''',(pur,pid,p['sku'],r['display_name'],p['product_type'],float(r['qty'] or 0),float(r['cost'] or 0),float(r['discount'] or 0),float(r['line_total'] or 0)))

 # Legacy journals retained as posted journals with mapped accounts
 je=LEGACY_PREFIX+'journal_entries'; jl=LEGACY_PREFIX+'journal_lines'; journal_map={}
 if je in tabs:
  for r in c.execute(f'SELECT * FROM {je} ORDER BY id'):
   lines=c.execute(f'SELECT * FROM {jl} WHERE entry_id=?',(r['id'],)).fetchall() if jl in tabs else []
   td=sum(float(x['debit'] or 0) for x in lines); tc=sum(float(x['credit'] or 0) for x in lines)
   no=f"MIG-{r['id']:06d}"
   cur=c.execute('''INSERT INTO journal_entries(journal_no,journal_date,description,source_type,source_id,reference_no,status,total_debit,total_credit,user_id,created_at,updated_at)
    VALUES(?,?,?,?,?,?, 'POSTED',?,?,?,?,?)''',(no,r['entry_date'],r['description'],'STANDARD_MIGRATION',str(r['id']),r['ref'],td,tc,admin,r['created_at'] or now,now))
   journal_map[r['id']]=cur.lastrowid
   for x in lines:
    aid=account_map.get(x['account_id'])
    if aid: c.execute('INSERT INTO journal_lines(journal_id,account_id,debit,credit,memo) VALUES(?,?,?,?,?)',(cur.lastrowid,aid,float(x['debit'] or 0),float(x['credit'] or 0),'Migrasi Standard'))

 # inventory balances sync to actual product stock
 c.execute('''INSERT INTO inventory_balances(warehouse_id,product_id,quantity,average_cost,updated_at)
  SELECT ?,p.id,p.stock_qty,p.purchase_price,? FROM products p WHERE p.product_type='STOCK'
  ON CONFLICT(warehouse_id,product_id) DO UPDATE SET quantity=excluded.quantity,average_cost=excluded.average_cost,updated_at=excluded.updated_at''',(wh,now))
 c.execute('CREATE TABLE IF NOT EXISTS app_metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
 vals={'schema_version':str(TARGET_SCHEMA_VERSION),'edition_created':'STANDARD','current_edition':edition,'migration_state':'COMPLETED','migration_date':now}
 for k,v in vals.items(): c.execute('INSERT OR REPLACE INTO app_metadata(key,value) VALUES(?,?)',(k,v))
 return {'migrated':True,'sales':len(sale_map),'purchases':len(purchase_map),'products':len(product_map),'partners':len(partner_map)}
