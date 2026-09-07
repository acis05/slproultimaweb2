from datetime import date
from decimal import Decimal
from .database import connect, write_transaction
from .security import utc_now
from .services import accounting_service, cash_service
from . import licensing


def _m(v):
    if v in (None,''): return Decimal('0.00')
    text=str(v).strip().replace('Rp','').replace('rp','').replace(' ','')
    if ',' in text and '.' in text:
        text=text.replace('.','').replace(',','.') if text.rfind(',')>text.rfind('.') else text.replace(',','')
    elif ',' in text:
        parts=text.split(','); text=parts[0].replace('.','')+'.'+parts[1] if len(parts)==2 and len(parts[1])<=2 else ''.join(parts)
    elif text.count('.')>1 or (text.count('.')==1 and len(text.rsplit('.',1)[1])==3): text=text.replace('.','')
    try:
        value=Decimal(text).quantize(Decimal('0.01'))
        if not value.is_finite(): raise ValueError
        return value
    except: raise ValueError('Nilai tidak valid.')

def _seq(tx,prefix,d):
    period=str(d)[:7].replace('-',''); key=f'{prefix}-{period}'
    r=tx.execute('SELECT current_value FROM document_sequences WHERE sequence_key=?',(key,)).fetchone(); n=int(r['current_value'])+1 if r else 1
    tx.execute("INSERT INTO document_sequences(sequence_key,current_value,updated_at) VALUES(?,?,?) ON CONFLICT(sequence_key) DO UPDATE SET current_value=excluded.current_value,updated_at=excluded.updated_at",(key,n,utc_now()))
    return f'{prefix}-{period}-{n:05d}'

def _resolve_order_unit(tx,product_id,unit_id):
    p=tx.execute("""SELECT p.id,p.unit_id base_unit_id,u.code base_unit_code
      FROM products p LEFT JOIN units u ON u.id=p.unit_id WHERE p.id=? AND p.is_active=1""",(int(product_id),)).fetchone()
    if not p:raise ValueError("Barang/Jasa tidak ditemukan atau nonaktif.")
    selected=int(unit_id) if unit_id not in (None,"") else int(p["base_unit_id"])
    row=tx.execute("""SELECT pu.unit_id,u.code,pu.conversion_ratio FROM product_units pu
      JOIN units u ON u.id=pu.unit_id WHERE pu.product_id=? AND pu.unit_id=? AND pu.is_active=1""",(int(product_id),selected)).fetchone()
    if row:return selected,str(row["code"]),_m(row["conversion_ratio"])
    if selected==int(p["base_unit_id"]):return selected,str(p["base_unit_code"] or ""),Decimal("1")
    raise ValueError("Satuan tidak tersedia untuk barang ini.")

def _order_totals(tx,items,tax_percent=0,header_discount=0,price_key='unit_price'):
    if not items:raise ValueError('Minimal satu item wajib diisi.')
    out=[];subtotal=Decimal('0')
    for x in items:
        pid=int(x.get('product_id'));qty=_m(x.get('qty'));price=_m(x.get(price_key));disc=_m(x.get('discount_amount',0))
        if qty<=0 or price<0:raise ValueError('Qty dan harga item tidak valid.')
        unit_id,unit_code,ratio=_resolve_order_unit(tx,pid,x.get("unit_id"))
        line=(qty*price-disc).quantize(Decimal('0.01'))
        if line<0:raise ValueError('Diskon item melebihi nilai item.')
        out.append((pid,str(x.get('description','')).strip() or None,qty,unit_id,unit_code,ratio,price,disc,line));subtotal+=line
    hd=_m(header_discount)
    if hd<0 or hd>subtotal:raise ValueError("Diskon header tidak valid.")
    taxable=max(Decimal('0'),subtotal-hd);tp=_m(tax_percent);tax=(taxable*tp/Decimal('100')).quantize(Decimal('0.01'));total=taxable+tax
    return out,subtotal,hd,tp,tax,total

def create_order(actor,d,ip,kind):
    is_sale=kind=='sales';order_date=str(d.get('order_date') or date.today().isoformat())[:10];now=utc_now()
    partner_key='customer_id' if is_sale else 'supplier_id';partner=int(d.get(partner_key))
    with write_transaction() as tx:
        items,sub,disc,tp,tax,total=_order_totals(tx,d.get('items') or [],d.get('tax_percent',0),d.get('discount_amount',0),'unit_price' if is_sale else 'unit_cost')
        licensing.enforce_transaction_capacity(tx,1)
        prefix='SO' if is_sale else 'PO';no=str(d.get('order_no','')).strip().upper() or _seq(tx,prefix,order_date);target='sales_orders' if is_sale else 'purchase_orders'
        if tx.execute(f'SELECT 1 FROM {target} WHERE UPPER(order_no)=UPPER(?)',(no,)).fetchone():raise ValueError('Nomor pesanan sudah digunakan.')
        if is_sale:
            cur=tx.execute("INSERT INTO sales_orders(order_no,order_date,customer_id,department_id,project_id,expected_date,subtotal,discount_amount,tax_percent,tax_amount,total_amount,notes,status,user_id,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,'OPEN',?,?,?)",(no,order_date,partner,d.get('department_id') or None,d.get('project_id') or None,d.get('expected_date') or None,str(sub),str(disc),str(tp),str(tax),str(total),str(d.get('notes','')).strip() or None,actor['id'],now,now))
            for pid,desc,qty,uid,ucode,ratio,price,ld,line in items:tx.execute("INSERT INTO sales_order_items(order_id,product_id,description,qty,unit_id,unit_code,conversion_ratio,unit_price,discount_amount,line_total) VALUES(?,?,?,?,?,?,?,?,?,?)",(cur.lastrowid,pid,desc,str(qty),uid,ucode,str(ratio),str(price),str(ld),str(line)))
        else:
            wh=int(d.get('warehouse_id'));cur=tx.execute("INSERT INTO purchase_orders(order_no,order_date,supplier_id,warehouse_id,department_id,project_id,expected_date,subtotal,discount_amount,tax_percent,tax_amount,total_amount,notes,status,user_id,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'OPEN',?,?,?)",(no,order_date,partner,wh,d.get('department_id') or None,d.get('project_id') or None,d.get('expected_date') or None,str(sub),str(disc),str(tp),str(tax),str(total),str(d.get('notes','')).strip() or None,actor['id'],now,now))
            for pid,desc,qty,uid,ucode,ratio,price,ld,line in items:tx.execute("INSERT INTO purchase_order_items(order_id,product_id,description,qty,unit_id,unit_code,conversion_ratio,unit_cost,discount_amount,line_total) VALUES(?,?,?,?,?,?,?,?,?,?)",(cur.lastrowid,pid,desc,str(qty),uid,ucode,str(ratio),str(price),str(ld),str(line)))
        licensing.record_transaction_usage(tx,event_key=f"{'SO' if is_sale else 'PO'}-{cur.lastrowid}",event_type='SALES_ORDER' if is_sale else 'PURCHASE_ORDER',reference_no=no,source_table=target,source_id=cur.lastrowid,units=1)
        return {'id':cur.lastrowid,'order_no':no,'total_amount':float(total)}

def update_order(actor,d,ip,kind,oid):
    is_sale=kind=='sales';oid=int(oid);table='sales_orders' if is_sale else 'purchase_orders';oit='sales_order_items' if is_sale else 'purchase_order_items'
    doc='sales' if is_sale else 'purchases';dit='sales_items' if is_sale else 'purchase_items';fk='sales_order_id' if is_sale else 'purchase_order_id';idcol='sale_id' if is_sale else 'purchase_id'
    order_date=str(d.get('order_date') or date.today().isoformat())[:10];partner=int(d.get('customer_id' if is_sale else 'supplier_id'));now=utc_now()
    with write_transaction() as tx:
        old=tx.execute(f"SELECT * FROM {table} WHERE id=?",(oid,)).fetchone()
        if not old:raise ValueError("Pesanan tidak ditemukan.")
        if old["status"] not in ("OPEN","DRAFT"):raise ValueError("Hanya pesanan outstanding yang dapat diedit.")
        rows,sub,disc,tp,tax,total=_order_totals(tx,d.get('items') or [],d.get('tax_percent',0),d.get('discount_amount',0),'unit_price' if is_sale else 'unit_cost')
        used={int(x["product_id"]):Decimal(str(x["qty"] or 0)) for x in tx.execute(f"SELECT di.product_id,SUM(di.qty) qty FROM {dit} di JOIN {doc} d ON d.id=di.{idcol} WHERE d.{fk}=? AND d.status='POSTED' GROUP BY di.product_id",(oid,)).fetchall()}
        newbase={}
        for pid,desc,qty,uid,ucode,ratio,price,ld,line in rows:newbase[pid]=newbase.get(pid,Decimal("0"))+qty*ratio
        for pid,usedqty in used.items():
            if newbase.get(pid,Decimal("0"))<usedqty:raise ValueError(f"Qty produk ID {pid} tidak boleh lebih kecil dari qty yang sudah diinvois ({usedqty}).")
        no=str(d.get("order_no") or old["order_no"]).strip().upper()
        if tx.execute(f"SELECT 1 FROM {table} WHERE UPPER(order_no)=UPPER(?) AND id<>?",(no,oid)).fetchone():raise ValueError("Nomor pesanan sudah digunakan.")
        if is_sale:
            tx.execute("UPDATE sales_orders SET order_no=?,order_date=?,customer_id=?,department_id=?,project_id=?,expected_date=?,subtotal=?,discount_amount=?,tax_percent=?,tax_amount=?,total_amount=?,notes=?,updated_at=? WHERE id=?",(no,order_date,partner,d.get("department_id") or None,d.get("project_id") or None,d.get("expected_date") or None,str(sub),str(disc),str(tp),str(tax),str(total),str(d.get("notes","")).strip() or None,now,oid))
        else:
            tx.execute("UPDATE purchase_orders SET order_no=?,order_date=?,supplier_id=?,warehouse_id=?,department_id=?,project_id=?,expected_date=?,subtotal=?,discount_amount=?,tax_percent=?,tax_amount=?,total_amount=?,notes=?,updated_at=? WHERE id=?",(no,order_date,partner,int(d.get("warehouse_id")),d.get("department_id") or None,d.get("project_id") or None,d.get("expected_date") or None,str(sub),str(disc),str(tp),str(tax),str(total),str(d.get("notes","")).strip() or None,now,oid))
        tx.execute(f"DELETE FROM {oit} WHERE order_id=?",(oid,))
        pricecol='unit_price' if is_sale else 'unit_cost'
        for pid,desc,qty,uid,ucode,ratio,price,ld,line in rows:tx.execute(f"INSERT INTO {oit}(order_id,product_id,description,qty,unit_id,unit_code,conversion_ratio,{pricecol},discount_amount,line_total) VALUES(?,?,?,?,?,?,?,?,?,?)",(oid,pid,desc,str(qty),uid,ucode,str(ratio),str(price),str(ld),str(line)))
        return {"id":oid,"order_no":no,"total_amount":float(total)}

def list_orders(kind):
    c=connect();is_sale=kind=='sales'
    try:
        if is_sale: rows=c.execute('''SELECT o.*,b.name partner_name,COALESCE((SELECT SUM(amount) FROM customer_downpayments d WHERE d.sales_order_id=o.id AND d.status='POSTED'),0) dp_total FROM sales_orders o JOIN business_partners b ON b.id=o.customer_id ORDER BY o.order_date DESC,o.id DESC''').fetchall()
        else: rows=c.execute('''SELECT o.*,b.name partner_name,COALESCE((SELECT SUM(amount) FROM supplier_downpayments d WHERE d.purchase_order_id=o.id AND d.status='POSTED'),0) dp_total FROM purchase_orders o JOIN business_partners b ON b.id=o.supplier_id ORDER BY o.order_date DESC,o.id DESC''').fetchall()
        return [{**dict(r),'subtotal':float(r['subtotal']),'total_amount':float(r['total_amount']),'dp_total':float(r['dp_total'])} for r in rows]
    finally:c.close()

def get_order(kind,oid):
    c=connect();is_sale=kind=='sales'
    try:
        table='sales_orders' if is_sale else 'purchase_orders';it='sales_order_items' if is_sale else 'purchase_order_items';r=c.execute(f'SELECT * FROM {table} WHERE id=?',(oid,)).fetchone()
        if not r:return None
        x=dict(r);x['items']=[dict(a) for a in c.execute(f'''SELECT oi.*,COALESCE(oi.unit_id,p.unit_id) resolved_unit_id,COALESCE(oi.unit_code,u.code) resolved_unit_code,COALESCE(oi.conversion_ratio,1) resolved_ratio FROM {it} oi JOIN products p ON p.id=oi.product_id LEFT JOIN units u ON u.id=p.unit_id WHERE oi.order_id=? ORDER BY oi.id''',(oid,)).fetchall()]
        for k in ('subtotal','discount_amount','tax_percent','tax_amount','total_amount'):x[k]=float(x[k])
        for a in x['items']:
            for k in ('qty','discount_amount','line_total','unit_price' if is_sale else 'unit_cost'):a[k]=float(a[k])
            a['unit_id']=a.get('resolved_unit_id');a['unit_code']=a.get('resolved_unit_code');a['conversion_ratio']=float(a.get('resolved_ratio') or 1)
        return x
    finally:c.close()

def delete_order(actor,kind,oid):
    with write_transaction() as tx:
        table='sales_orders' if kind=='sales' else 'purchase_orders';dp='customer_downpayments' if kind=='sales' else 'supplier_downpayments';fk='sales_order_id' if kind=='sales' else 'purchase_order_id'
        row=tx.execute(f'SELECT status,order_no FROM {table} WHERE id=?',(oid,)).fetchone()
        if not row: raise ValueError('Pesanan tidak ditemukan.')
        if row['status']=='CANCELLED': raise ValueError('Pesanan sudah dibatalkan.')
        if tx.execute(f"SELECT 1 FROM {dp} WHERE {fk}=? AND status='POSTED'",(oid,)).fetchone():raise ValueError('Pesanan sudah memiliki DP. Batalkan DP terlebih dahulu.')
        tx.execute(f"UPDATE {table} SET status='CANCELLED',updated_at=? WHERE id=?",(utc_now(),oid));return {'id':oid,'order_no':row['order_no']}

def create_dp(actor,d,ip,kind):
    customer=kind=='customer'; dp_date=str(d.get('dp_date') or date.today().isoformat())[:10]; partner=int(d.get('customer_id' if customer else 'supplier_id'));cash=int(d.get('cash_account_id'));amount=_m(d.get('amount'))
    if amount<=0:raise ValueError('Nilai DP harus lebih dari nol.')
    now=utc_now()
    with write_transaction() as tx:
        no=_seq(tx,'DPC' if customer else 'DPS',dp_date);order_id=d.get('order_id') or None
        table='customer_downpayments' if customer else 'supplier_downpayments'; partner_col='customer_id' if customer else 'supplier_id';order_col='sales_order_id' if customer else 'purchase_order_id'
        cur=tx.execute(f'INSERT INTO {table}(dp_no,dp_date,{partner_col},{order_col},cash_account_id,amount,allocated_amount,notes,status,user_id,created_at) VALUES(?,?,?,?,?,?,0,?,\'POSTED\',?,?)',(no,dp_date,partner,order_id,cash,str(amount),str(d.get('notes','')).strip() or None,actor['id'],now))
        coa=tx.execute('SELECT coa_account_id FROM cash_accounts WHERE id=?',(cash,)).fetchone();cash_coa=coa['coa_account_id'] if coa and coa['coa_account_id'] else accounting_service.account_id(tx,'1000')
        if customer:
            cash_service.post(tx,account_id=cash,transaction_date=dp_date,transaction_type='IN',amount=amount,description=f'Penerimaan DP {no}',reference_no=no,user_id=actor['id'])
            lines=[{'account_id':cash_coa,'debit':amount},{'account_code':'2200','credit':amount,'partner_id':partner}]
        else:
            cash_service.post(tx,account_id=cash,transaction_date=dp_date,transaction_type='OUT',amount=amount,description=f'Pembayaran DP {no}',reference_no=no,user_id=actor['id'])
            lines=[{'account_code':'1250','debit':amount,'partner_id':partner},{'account_id':cash_coa,'credit':amount}]
        j=accounting_service.post_journal(tx,journal_date=dp_date,description=('Penerimaan' if customer else 'Pembayaran')+f' DP {no}',source_type='CUSTOMER_DP' if customer else 'SUPPLIER_DP',source_id=cur.lastrowid,reference_no=no,lines=lines,user_id=actor['id'])
        tx.execute(f'UPDATE {table} SET journal_id=? WHERE id=?',(j['id'],cur.lastrowid));return {'id':cur.lastrowid,'dp_no':no,'amount':float(amount)}

def list_dp(kind):
    c=connect();customer=kind=='customer'
    try:
        table='customer_downpayments' if customer else 'supplier_downpayments';pcol='customer_id' if customer else 'supplier_id';ocol='sales_order_id' if customer else 'purchase_order_id';ot='sales_orders' if customer else 'purchase_orders'
        rows=c.execute(f'''SELECT d.*,b.name partner_name,o.order_no FROM {table} d JOIN business_partners b ON b.id=d.{pcol} LEFT JOIN {ot} o ON o.id=d.{ocol} WHERE d.status='POSTED' ORDER BY d.dp_date DESC,d.id DESC''').fetchall()
        return [{**dict(r),'amount':float(r['amount']),'allocated_amount':float(r['allocated_amount']),'available_amount':float(r['amount'])-float(r['allocated_amount'])} for r in rows]
    finally:c.close()

def allocate_dp(actor,d,ip,kind):
    customer=kind=='customer';alloc_date=str(d.get('allocation_date') or date.today().isoformat())[:10];dpid=int(d.get('downpayment_id'));invoice_key=str(d.get('invoice_id') or '').strip();amount=_m(d.get('amount'));now=utc_now()
    opening_partner_id=int(invoice_key.split(':',1)[1]) if invoice_key.startswith('OPENING:') else None
    try: invoice=(-opening_partner_id) if opening_partner_id else int(invoice_key)
    except Exception: raise ValueError('Invoice untuk alokasi DP tidak valid.')
    with write_transaction() as tx:
        table='customer_downpayments' if customer else 'supplier_downpayments';invtable='sales' if customer else 'purchases';partner='customer_id' if customer else 'supplier_id';dp=tx.execute(f"SELECT * FROM {table} WHERE id=? AND status='POSTED'",(dpid,)).fetchone()
        if opening_partner_id:
            ptype='CUSTOMER' if customer else 'SUPPLIER'
            inv=tx.execute("SELECT id,opening_balance,code,name FROM business_partners WHERE id=? AND partner_type IN (?,'BOTH')",(opening_partner_id,ptype)).fetchone()
            if not dp or not inv:raise ValueError('DP atau saldo awal tidak ditemukan.')
            if int(dp[partner])!=int(opening_partner_id):raise ValueError('Partner DP dan saldo awal tidak sama.')
            paid_table='opening_receivable_payments' if customer else 'opening_payable_payments'; paid_fk='customer_id' if customer else 'supplier_id'; typ='CUSTOMER' if customer else 'SUPPLIER'
            settled=_m(tx.execute(f"SELECT COALESCE(SUM(amount),0) v FROM {paid_table} WHERE {paid_fk}=?",(opening_partner_id,)).fetchone()['v'])
            allocated=_m(tx.execute("SELECT COALESCE(SUM(amount),0) v FROM downpayment_allocations WHERE allocation_type=? AND invoice_id=? AND status='POSTED'",(typ,-opening_partner_id)).fetchone()['v'])
            due=max(Decimal('0.00'),_m(inv['opening_balance'])-settled-allocated)
        else:
            inv=tx.execute(f"SELECT * FROM {invtable} WHERE id=? AND status='POSTED'",(invoice,)).fetchone()
            if not dp or not inv:raise ValueError('DP atau invoice tidak ditemukan.')
            if int(dp[partner])!=int(inv[partner]):raise ValueError('Partner DP dan invoice tidak sama.')
            due=max(Decimal('0.00'),_m(inv['balance_due']))
        available=max(Decimal('0.00'),_m(dp['amount'])-_m(dp['allocated_amount']))
        if amount<=0: raise ValueError('Jumlah alokasi harus lebih dari nol.')
        if available<=0: raise ValueError('Saldo DP sudah habis.')
        if due<=0: raise ValueError('Invoice sudah lunas.')
        if amount>available or amount>due:raise ValueError('Nilai alokasi melebihi saldo DP atau sisa tagihan.')
        no=_seq(tx,'ALC' if customer else 'ALS',alloc_date);cur=tx.execute("INSERT INTO downpayment_allocations(allocation_no,allocation_date,allocation_type,downpayment_id,invoice_id,amount,status,user_id,created_at) VALUES(?,?,?,?,?,?,\'POSTED\',?,?)",(no,alloc_date,'CUSTOMER' if customer else 'SUPPLIER',dpid,invoice,str(amount),actor['id'],now))
        tx.execute(f'UPDATE {table} SET allocated_amount=ROUND(allocated_amount+?,2) WHERE id=?',(str(amount),dpid));
        if not opening_partner_id: tx.execute(f'UPDATE {invtable} SET paid_amount=ROUND(paid_amount+?,2),balance_due=MAX(0,ROUND(balance_due-?,2)),updated_at=? WHERE id=?',(str(amount),str(amount),now,invoice))
        bp=tx.execute('SELECT receivable_account_id,payable_account_id FROM business_partners WHERE id=?',(dp[partner],)).fetchone(); lines=[{'account_code':'2200','debit':amount,'partner_id':dp[partner]},{'account_id':int(bp['receivable_account_id']) if bp and bp['receivable_account_id'] else accounting_service.account_id(tx,'1100'),'credit':amount,'partner_id':dp[partner]}] if customer else [{'account_id':int(bp['payable_account_id']) if bp and bp['payable_account_id'] else accounting_service.account_id(tx,'2000'),'debit':amount,'partner_id':dp[partner]},{'account_code':'1250','credit':amount,'partner_id':dp[partner]}]
        j=accounting_service.post_journal(tx,journal_date=alloc_date,description=f'Alokasi DP {no}',source_type='CUSTOMER_DP_ALLOCATION' if customer else 'SUPPLIER_DP_ALLOCATION',source_id=cur.lastrowid,reference_no=no,lines=lines,user_id=actor['id']);tx.execute('UPDATE downpayment_allocations SET journal_id=? WHERE id=?',(j['id'],cur.lastrowid));return {'id':cur.lastrowid,'allocation_no':no,'remaining_dp':float(available-amount),'remaining_invoice':float(due-amount)}

def list_allocations(kind):
    c=connect();typ='CUSTOMER' if kind=='customer' else 'SUPPLIER';dp='customer_downpayments' if kind=='customer' else 'supplier_downpayments';inv='sales' if kind=='customer' else 'purchases';ino='invoice_no' if kind=='customer' else 'purchase_no'
    try:
        rows=c.execute(f'''SELECT a.*,d.dp_no,CASE WHEN a.invoice_id<0 THEN 'SALDO AWAL-'||COALESCE(bp.code,'') ELSE i.{ino} END invoice_no FROM downpayment_allocations a JOIN {dp} d ON d.id=a.downpayment_id LEFT JOIN {inv} i ON i.id=a.invoice_id LEFT JOIN business_partners bp ON bp.id=-a.invoice_id WHERE a.allocation_type=? AND a.status='POSTED' ORDER BY a.allocation_date DESC,a.id DESC''',(typ,)).fetchall();return [{**dict(r),'amount':float(r['amount'])} for r in rows]
    finally:c.close()


def _void_journal(tx,journal_id):
    if journal_id:
        tx.execute("UPDATE journal_entries SET status='VOID',updated_at=? WHERE id=? AND status='POSTED'",(utc_now(),int(journal_id)))

def delete_dp(actor,kind,dp_id,ip):
    customer=kind=='customer';table='customer_downpayments' if customer else 'supplier_downpayments'
    with write_transaction() as tx:
        row=tx.execute(f"SELECT * FROM {table} WHERE id=? AND status='POSTED'",(int(dp_id),)).fetchone()
        if not row: raise ValueError('DP tidak ditemukan atau sudah dibatalkan.')
        if _m(row['allocated_amount'])>0: raise ValueError('DP sudah dialokasikan. Hapus alokasi DP terlebih dahulu.')
        _void_journal(tx,row['journal_id'])
        opposite='OUT' if customer else 'IN'
        cash_service.post(tx,account_id=row['cash_account_id'],transaction_date=date.today().isoformat(),transaction_type=opposite,amount=_m(row['amount']),description=f"Pembalikan {row['dp_no']}",reference_no=f"VOID-{row['dp_no']}",user_id=actor['id'],allow_negative=True)
        tx.execute(f"UPDATE {table} SET status='VOID' WHERE id=?",(int(dp_id),))
        return {'id':int(dp_id),'dp_no':row['dp_no']}

def update_dp(actor,kind,dp_id,d,ip):
    customer=kind=='customer';table='customer_downpayments' if customer else 'supplier_downpayments'
    c=connect()
    try: old=c.execute(f"SELECT * FROM {table} WHERE id=?",(int(dp_id),)).fetchone()
    finally: c.close()
    if not old: raise ValueError('DP tidak ditemukan.')
    if _m(old['allocated_amount'])>0: raise ValueError('DP sudah dialokasikan. Hapus alokasi terlebih dahulu sebelum edit.')
    delete_dp(actor,kind,dp_id,ip)
    payload=dict(d)
    if customer: payload.setdefault('customer_id',old['customer_id'])
    else: payload.setdefault('supplier_id',old['supplier_id'])
    payload.setdefault('cash_account_id',old['cash_account_id'])
    payload.setdefault('order_id',old['sales_order_id'] if customer else old['purchase_order_id'])
    payload.setdefault('dp_date',old['dp_date']);payload.setdefault('amount',old['amount']);payload.setdefault('notes',old['notes'])
    return create_dp(actor,payload,ip,kind)

def delete_allocation(actor,kind,allocation_id,ip):
    customer=kind=='customer';typ='CUSTOMER' if customer else 'SUPPLIER';table='customer_downpayments' if customer else 'supplier_downpayments';inv='sales' if customer else 'purchases'
    with write_transaction() as tx:
        row=tx.execute("SELECT * FROM downpayment_allocations WHERE id=? AND allocation_type=? AND status='POSTED'",(int(allocation_id),typ)).fetchone()
        if not row: raise ValueError('Alokasi DP tidak ditemukan atau sudah dibatalkan.')
        amount=_m(row['amount']);now=utc_now()
        _void_journal(tx,row['journal_id'])
        tx.execute(f"UPDATE {table} SET allocated_amount=MAX(0,ROUND(allocated_amount-?,2)) WHERE id=?",(str(amount),row['downpayment_id']))
        if int(row['invoice_id'])>0: tx.execute(f"UPDATE {inv} SET paid_amount=MAX(0,paid_amount-?),balance_due=balance_due+?,updated_at=? WHERE id=?",(str(amount),str(amount),now,row['invoice_id']))
        tx.execute("UPDATE downpayment_allocations SET status='VOID' WHERE id=?",(int(allocation_id),))
        return {'id':int(allocation_id),'allocation_no':row['allocation_no']}

def update_allocation(actor,kind,allocation_id,d,ip):
    c=connect()
    try: old=c.execute("SELECT * FROM downpayment_allocations WHERE id=?",(int(allocation_id),)).fetchone()
    finally: c.close()
    if not old: raise ValueError('Alokasi DP tidak ditemukan.')
    delete_allocation(actor,kind,allocation_id,ip)
    payload=dict(d);payload.setdefault('allocation_date',old['allocation_date']);payload.setdefault('downpayment_id',old['downpayment_id']);payload.setdefault('invoice_id',('OPENING:'+str(-int(old['invoice_id']))) if int(old['invoice_id'])<0 else old['invoice_id']);payload.setdefault('amount',old['amount'])
    return allocate_dp(actor,payload,ip,kind)

def validate_order_fulfillment(tx,kind,order_id,items):
    if not order_id:return None
    sale=kind=='sales';ot='sales_orders' if sale else 'purchase_orders';oit='sales_order_items' if sale else 'purchase_order_items';doc='sales' if sale else 'purchases';dit='sales_items' if sale else 'purchase_items';fk='sales_order_id' if sale else 'purchase_order_id'
    order=tx.execute(f"SELECT id,status FROM {ot} WHERE id=?",(int(order_id),)).fetchone()
    if not order:raise ValueError('Pesanan sumber tidak ditemukan.')
    if order['status'] in ('CANCELLED','COMPLETED'):raise ValueError('Pesanan sudah ditutup atau dibatalkan.')
    requested={}
    for pid,qty in items: requested[int(pid)]=requested.get(int(pid),Decimal('0'))+Decimal(str(qty))
    ordered={int(r['product_id']):Decimal(str(r['qty'])) for r in tx.execute(f"SELECT product_id,SUM(qty*COALESCE(conversion_ratio,1)) qty FROM {oit} WHERE order_id=? GROUP BY product_id",(int(order_id),))}
    used={int(r['product_id']):Decimal(str(r['qty'])) for r in tx.execute(f"SELECT i.product_id,SUM(i.qty) qty FROM {dit} i JOIN {doc} d ON d.id=i.{ 'sale_id' if sale else 'purchase_id'} WHERE d.{fk}=? AND d.status='POSTED' GROUP BY i.product_id",(int(order_id),))}
    for pid,qty in requested.items():
        remaining=ordered.get(pid,Decimal('0'))-used.get(pid,Decimal('0'))
        if qty>remaining:raise ValueError(f'Qty invoice melebihi sisa pesanan. Sisa produk ID {pid}: {remaining}.')
    return int(order_id)

def close_order_if_fulfilled(tx,kind,order_id):
    if not order_id:return
    sale=kind=='sales';ot='sales_orders' if sale else 'purchase_orders';oit='sales_order_items' if sale else 'purchase_order_items';doc='sales' if sale else 'purchases';dit='sales_items' if sale else 'purchase_items';fk='sales_order_id' if sale else 'purchase_order_id';idcol='sale_id' if sale else 'purchase_id'
    rows=tx.execute(f"SELECT oi.product_id,SUM(oi.qty*COALESCE(oi.conversion_ratio,1)) ordered,COALESCE((SELECT SUM(di.qty) FROM {dit} di JOIN {doc} d ON d.id=di.{idcol} WHERE d.{fk}=oi.order_id AND d.status='POSTED' AND di.product_id=oi.product_id),0) used FROM {oit} oi WHERE oi.order_id=? GROUP BY oi.product_id",(int(order_id),)).fetchall()
    status='COMPLETED' if rows and all(Decimal(str(r['used']))>=Decimal(str(r['ordered'])) for r in rows) else 'OPEN'
    tx.execute(f"UPDATE {ot} SET status=?,updated_at=? WHERE id=?",(status,utc_now(),int(order_id)))
