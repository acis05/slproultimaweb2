from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from ..security import utc_now
from . import inventory_service, accounting_service
MONEY=Decimal("0.01"); QTY=Decimal("0.0001")
def D(v): return Decimal(str(v if v not in (None,'') else 0))
def money(v): return D(v).quantize(MONEY,rounding=ROUND_HALF_UP)
def qty(v): return D(v).quantize(QTY,rounding=ROUND_HALF_UP)
def next_no(tx,prefix,doc_date):
 period=str(doc_date)[:7].replace('-',''); key=f"{prefix}-{period}"
 r=tx.execute("SELECT current_value FROM document_sequences WHERE sequence_key=?",(key,)).fetchone(); n=int(r['current_value'])+1 if r else 1
 tx.execute("INSERT INTO document_sequences(sequence_key,current_value,updated_at) VALUES(?,?,?) ON CONFLICT(sequence_key) DO UPDATE SET current_value=excluded.current_value,updated_at=excluded.updated_at",(key,n,utc_now()))
 return f"{prefix}-{period}-{n:06d}"
def _account(tx,product,field,default): return int(product[field] or accounting_service.account_id(tx,default))
def create_purchase_return(tx,actor,data,ip,audit):
 dt=str(data.get('return_date') or date.today().isoformat())[:10]; supplier_id=int(data.get('supplier_id')); warehouse_id=int(data.get('warehouse_id')); purchase_id=data.get('purchase_id') or None
 supplier=tx.execute("SELECT * FROM business_partners WHERE id=? AND is_active=1 AND partner_type IN ('SUPPLIER','BOTH')",(supplier_id,)).fetchone()
 if not supplier: raise ValueError('Pemasok tidak valid.')
 items=data.get('items') or []
 if not items: raise ValueError('Minimal satu barang retur wajib diisi.')
 no=next_no(tx,'RPB',dt); now=utc_now(); total_payable=Decimal('0'); total_inventory=Decimal('0'); rows=[]; inv_groups={}
 for i,x in enumerate(items,1):
  p=tx.execute("SELECT * FROM products WHERE id=? AND is_active=1",(int(x.get('product_id')),)).fetchone()
  if not p or p['product_type']!='STOCK': raise ValueError(f'Barang retur baris {i} tidak valid.')
  q=qty(x.get('qty')); unit=money(x.get('unit_value'))
  if q<=0: raise ValueError(f'Qty retur baris {i} harus lebih dari nol.')
  before,avg=inventory_service.get_balance(tx,warehouse_id,p['id'])
  if purchase_id:
   src=tx.execute("SELECT unit_cost,qty,line_total FROM purchase_items WHERE purchase_id=? AND product_id=? ORDER BY id LIMIT 1",(purchase_id,p['id'])).fetchone()
   if src and D(src['qty'])>0: avg=money(D(src['line_total'])/D(src['qty']))
  if before<q: raise ValueError(f"Stok {p['name']} tidak cukup untuk diretur. Tersedia {before}.")
  payable=(q*unit).quantize(MONEY); inv=(q*avg).quantize(MONEY)
  total_payable+=payable; total_inventory+=inv; aid=_account(tx,p,'inventory_account_id','1200'); inv_groups[aid]=inv_groups.get(aid,Decimal('0'))+inv
  rows.append((p,q,unit,avg,payable,inv))
 cur=tx.execute("INSERT INTO purchase_returns(return_no,return_date,purchase_id,supplier_id,warehouse_id,total_payable,total_inventory,difference,notes,status,user_id,created_at) VALUES(?,?,?,?,?,?,?,?,?,'POSTED',?,?)",(no,dt,purchase_id,supplier_id,warehouse_id,str(total_payable),str(total_inventory),str(total_payable-total_inventory),str(data.get('notes') or '').strip() or None,actor['id'],now)); rid=cur.lastrowid
 for p,q,unit,avg,payable,inv in rows:
  tx.execute("INSERT INTO purchase_return_items(return_id,product_id,sku,product_name,qty,unit_value,average_cost,payable_value,inventory_value) VALUES(?,?,?,?,?,?,?,?,?)",(rid,p['id'],p['sku'],p['name'],str(q),str(unit),str(avg),str(payable),str(inv)))
  inventory_service.post_movement(tx,product_id=p['id'],warehouse_id=warehouse_id,movement_type='PURCHASE_RETURN',quantity_change=-q,unit_cost=avg,reference_type='PURCHASE_RETURN',reference_no=no,reason=f'Retur pembelian {no}',user_id=actor['id'],created_at=now)
 lines=[{'account_id':int(supplier['payable_account_id']) if supplier['payable_account_id'] else accounting_service.account_id(tx,'2000'),'debit':total_payable,'partner_id':supplier_id}]
 lines += [{'account_id':aid,'credit':amt} for aid,amt in inv_groups.items()]
 diff=total_payable-total_inventory
 if diff>0: lines.append({'account_code':'5000','credit':diff})
 elif diff<0: lines.append({'account_code':'5000','debit':-diff})
 accounting_service.post_journal(tx,journal_date=dt,description=f'Retur pembelian {no}',source_type='PURCHASE_RETURN',source_id=rid,reference_no=no,lines=lines,user_id=actor['id'])
 audit(actor['id'],'PURCHASE_RETURN_CREATED','purchase_return',rid,{'return_no':no,'total_payable':float(total_payable),'inventory_value':float(total_inventory)},ip,tx)
 return {'id':rid,'return_no':no,'total_payable':float(total_payable),'inventory_value':float(total_inventory),'difference':float(diff)}
def create_sales_return(tx,actor,data,ip,audit):
 dt=str(data.get('return_date') or date.today().isoformat())[:10]; customer_id=int(data.get('customer_id')); warehouse_id=int(data.get('warehouse_id')); sale_id=data.get('sale_id') or None
 customer=tx.execute("SELECT * FROM business_partners WHERE id=? AND is_active=1 AND partner_type IN ('CUSTOMER','BOTH')",(customer_id,)).fetchone()
 if not customer: raise ValueError('Pelanggan tidak valid.')
 items=data.get('items') or []
 if not items: raise ValueError('Minimal satu barang retur wajib diisi.')
 no=next_no(tx,'RPJ',dt); now=utc_now(); total_sales=Decimal('0'); total_cogs=Decimal('0'); rows=[]; inv_groups={}; cogs_groups={}
 for i,x in enumerate(items,1):
  p=tx.execute("SELECT * FROM products WHERE id=? AND is_active=1",(int(x.get('product_id')),)).fetchone()
  if not p: raise ValueError(f'Barang retur baris {i} tidak valid.')
  q=qty(x.get('qty')); unit=money(x.get('unit_value'))
  if q<=0: raise ValueError(f'Qty retur baris {i} harus lebih dari nol.')
  sales=(q*unit).quantize(MONEY); cogs=Decimal('0'); avg=Decimal('0')
  if p['product_type']=='STOCK':
   _,avg=inventory_service.get_balance(tx,warehouse_id,p['id'])
   if sale_id:
    src=tx.execute("SELECT purchase_price_snapshot FROM sales_items WHERE sale_id=? AND product_id=? ORDER BY id LIMIT 1",(sale_id,p['id'])).fetchone()
    if src:avg=money(src['purchase_price_snapshot'])
   cogs=(q*avg).quantize(MONEY); ia=_account(tx,p,'inventory_account_id','1200'); ca=_account(tx,p,'cogs_account_id','5000'); inv_groups[ia]=inv_groups.get(ia,Decimal('0'))+cogs; cogs_groups[ca]=cogs_groups.get(ca,Decimal('0'))+cogs
  total_sales+=sales; total_cogs+=cogs; rows.append((p,q,unit,avg,sales,cogs))
 cur=tx.execute("INSERT INTO sales_returns(return_no,return_date,sale_id,customer_id,warehouse_id,total_sales,total_cogs,notes,status,user_id,created_at) VALUES(?,?,?,?,?,?,?,?, 'POSTED',?,?)",(no,dt,sale_id,customer_id,warehouse_id,str(total_sales),str(total_cogs),str(data.get('notes') or '').strip() or None,actor['id'],now)); rid=cur.lastrowid
 for p,q,unit,avg,sales,cogs in rows:
  tx.execute("INSERT INTO sales_return_items(return_id,product_id,sku,product_name,product_type,qty,unit_value,average_cost,sales_value,cogs_value) VALUES(?,?,?,?,?,?,?,?,?,?)",(rid,p['id'],p['sku'],p['name'],p['product_type'],str(q),str(unit),str(avg),str(sales),str(cogs)))
  if p['product_type']=='STOCK': inventory_service.post_movement(tx,product_id=p['id'],warehouse_id=warehouse_id,movement_type='SALES_RETURN',quantity_change=q,unit_cost=avg,reference_type='SALES_RETURN',reference_no=no,reason=f'Retur penjualan {no}',user_id=actor['id'],created_at=now)
 lines=[{'account_code':'4100','debit':total_sales},{'account_id':int(customer['receivable_account_id']) if customer['receivable_account_id'] else accounting_service.account_id(tx,'1100'),'credit':total_sales,'partner_id':customer_id}]
 lines += [{'account_id':aid,'debit':amt} for aid,amt in inv_groups.items()] + [{'account_id':aid,'credit':amt} for aid,amt in cogs_groups.items()]
 accounting_service.post_journal(tx,journal_date=dt,description=f'Retur penjualan {no}',source_type='SALES_RETURN',source_id=rid,reference_no=no,lines=lines,user_id=actor['id'])
 audit(actor['id'],'SALES_RETURN_CREATED','sales_return',rid,{'return_no':no,'total_sales':float(total_sales),'cogs':float(total_cogs)},ip,tx)
 return {'id':rid,'return_no':no,'total_sales':float(total_sales),'cogs':float(total_cogs)}
