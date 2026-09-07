from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from ..security import utc_now
from .. import licensing

MONEY = Decimal("0.01")

def _normalize_decimal_text(value):
    """Normalize nominal database/PDF in Indonesian or international format.

    Examples: 600000, 600,000.00, 600.000,00 and Rp 600.000.
    """
    if value in (None, ""):
        return "0"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    text = str(value).strip().replace("Rp", "").replace("rp", "").replace(" ", "")
    negative = text.startswith("-")
    if negative:
        text = text[1:]
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        parts = text.split(",")
        text = (parts[0].replace(".", "") + "." + parts[1]) if len(parts) == 2 and len(parts[1]) in (1, 2) else "".join(parts)
    elif "." in text:
        parts = text.split(".")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
            text = "".join(parts)
    return ("-" if negative else "") + text

def money(value, label="Nilai"):
    try:
        v = Decimal(_normalize_decimal_text(value)).quantize(MONEY, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} tidak valid.")
    if not v.is_finite() or v < 0:
        raise ValueError(f"{label} tidak valid.")
    return v

def account_id(tx, code):
    r=tx.execute("SELECT id FROM chart_of_accounts WHERE code=? AND is_active=1",(code,)).fetchone()
    if not r: raise ValueError(f"Akun COA {code} tidak ditemukan atau nonaktif.")
    return int(r["id"])

def next_journal_no(tx, journal_date):
    period=str(journal_date)[:7].replace('-','')
    key=f"JOURNAL-{period}"
    r=tx.execute("SELECT current_value FROM document_sequences WHERE sequence_key=?",(key,)).fetchone()
    value=int(r['current_value'])+1 if r else 1
    tx.execute("""INSERT INTO document_sequences(sequence_key,current_value,updated_at)
                  VALUES(?,?,?) ON CONFLICT(sequence_key) DO UPDATE SET
                  current_value=excluded.current_value,updated_at=excluded.updated_at""",
               (key,value,utc_now()))
    return f"JU-{period}-{value:06d}"

def post_journal(tx, *, journal_date, description, source_type, source_id, reference_no,
                 lines, user_id, journal_no=None, department_id=None, project_id=None):
    if not lines or len(lines)<2: raise ValueError("Jurnal minimal memiliki dua baris.")
    if department_id is not None:
        try:department_id=int(department_id)
        except Exception:raise ValueError("Departemen jurnal tidak valid.")
        if not tx.execute("SELECT 1 FROM departments WHERE id=? AND is_active=1",(department_id,)).fetchone():
            raise ValueError("Departemen jurnal tidak ditemukan atau nonaktif.")
    if project_id is not None:
        try:project_id=int(project_id)
        except Exception:raise ValueError("Proyek jurnal tidak valid.")
        if not tx.execute("SELECT 1 FROM projects WHERE id=? AND is_active=1",(project_id,)).fetchone():
            raise ValueError("Proyek jurnal tidak ditemukan atau nonaktif.")
    normalized=[]; total_debit=Decimal('0.00'); total_credit=Decimal('0.00')
    for idx,line in enumerate(lines,1):
        aid=line.get('account_id')
        if not aid and line.get('account_code'): aid=account_id(tx,line['account_code'])
        try: aid=int(aid)
        except Exception: raise ValueError(f"Akun baris {idx} tidak valid.")
        acc=tx.execute("SELECT id,code,name,account_subtype FROM chart_of_accounts WHERE id=? AND is_active=1",(aid,)).fetchone()
        if not acc: raise ValueError(f"Akun baris {idx} tidak ditemukan atau nonaktif.")
        debit=money(line.get('debit',0),f"Debit baris {idx}")
        credit=money(line.get('credit',0),f"Kredit baris {idx}")
        if (debit>0 and credit>0) or (debit==0 and credit==0):
            raise ValueError(f"Baris {idx} harus berisi debit atau kredit saja.")
        total_debit += debit; total_credit += credit
        partner_id=line.get('partner_id') or None
        partner_type=None
        subtype=acc['account_subtype'] or ''
        if subtype in ('RECEIVABLE','PAYABLE'):
            if not partner_id: raise ValueError(f"Baris {idx}: akun {acc['name']} wajib memilih pelanggan/pemasok.")
            try: partner_id=int(partner_id)
            except Exception: raise ValueError(f"Baris {idx}: partner tidak valid.")
            required='CUSTOMER' if subtype=='RECEIVABLE' else 'SUPPLIER'
            partner=tx.execute("SELECT id,partner_type,name FROM business_partners WHERE id=? AND is_active=1",(partner_id,)).fetchone()
            if not partner or partner['partner_type'] not in (required,'BOTH'):
                raise ValueError(f"Baris {idx}: partner tidak sesuai tipe akun.")
            partner_type=required
        line_department_id=line.get("department_id")
        line_project_id=line.get("project_id")
        if line_department_id in (None,""):
            line_department_id=department_id
        else:
            try:line_department_id=int(line_department_id)
            except Exception:raise ValueError(f"Baris {idx}: departemen tidak valid.")
            if not tx.execute("SELECT 1 FROM departments WHERE id=? AND is_active=1",(line_department_id,)).fetchone():
                raise ValueError(f"Baris {idx}: departemen tidak ditemukan atau nonaktif.")
        if line_project_id in (None,""):
            line_project_id=project_id
        else:
            try:line_project_id=int(line_project_id)
            except Exception:raise ValueError(f"Baris {idx}: proyek tidak valid.")
            if not tx.execute("SELECT 1 FROM projects WHERE id=? AND is_active=1",(line_project_id,)).fetchone():
                raise ValueError(f"Baris {idx}: proyek tidak ditemukan atau nonaktif.")
        normalized.append((aid,debit,credit,str(line.get('memo','')).strip() or None,
                           partner_id,partner_type,line_department_id,line_project_id))
    total_debit=total_debit.quantize(MONEY); total_credit=total_credit.quantize(MONEY)
    if total_debit != total_credit: raise ValueError(f"Jurnal tidak seimbang. Debit {total_debit}, kredit {total_credit}.")
    if total_debit <= 0: raise ValueError("Nilai jurnal harus lebih dari nol.")
    if source_type and source_id is not None:
        existing=tx.execute("SELECT id,journal_no FROM journal_entries WHERE source_type=? AND source_id=? AND status='POSTED'",(source_type,str(source_id))).fetchone()
        if existing: return {'id':existing['id'],'journal_no':existing['journal_no'],'total_debit':float(total_debit),'total_credit':float(total_credit),'existing':True}
    journal_no=journal_no or next_journal_no(tx,journal_date)
    now=utc_now()
    licensing.enforce_transaction_capacity(tx, 1)
    cur=tx.execute("""INSERT INTO journal_entries(journal_no,journal_date,description,source_type,source_id,reference_no,department_id,project_id,status,total_debit,total_credit,user_id,created_at,updated_at)
                      VALUES(?,?,?,?,?,?,?,?,'POSTED',?,?,?,?,?)""",
                   (journal_no,str(journal_date)[:10],description,source_type,str(source_id) if source_id is not None else None,reference_no,department_id,project_id,str(total_debit),str(total_credit),user_id,now,now))
    jid=cur.lastrowid
    licensing.record_transaction_usage(tx,event_key=f'JOURNAL-{jid}',event_type=source_type or 'JOURNAL',
        reference_no=reference_no,source_table='journal_entries',source_id=jid,units=1)
    for aid,debit,credit,memo,partner_id,partner_type,line_department_id,line_project_id in normalized:
        tx.execute("""INSERT INTO journal_lines(
          journal_id,account_id,debit,credit,memo,partner_id,partner_type,
          department_id,project_id
        ) VALUES(?,?,?,?,?,?,?,?,?)""",(
          jid,aid,str(debit),str(credit),memo,partner_id,partner_type,
          line_department_id,line_project_id))
    return {'id':jid,'journal_no':journal_no,'total_debit':float(total_debit),'total_credit':float(total_credit),'existing':False}

def post_sale(tx, *, sale_id, invoice_no, sale_date, taxable_amount, tax_amount,
              paid_amount, balance_due, cash_account_id, cogs_amount, customer_id,
              user_id, revenue_lines=None, cogs_lines=None, department_id=None, project_id=None,
              discount_amount=0, commission_amount=0, receivable_account_id=None):
    lines=[]
    if money(paid_amount)>0:
        coa=tx.execute("SELECT coa_account_id FROM cash_accounts WHERE id=?",(cash_account_id,)).fetchone()
        lines.append({'account_id':coa['coa_account_id'] if coa and coa['coa_account_id'] else account_id(tx,'1000'),'debit':paid_amount})
    if money(balance_due)>0:
        lines.append({'account_id':int(receivable_account_id) if receivable_account_id else account_id(tx,'1100'),'debit':balance_due,'partner_id':customer_id})
    # Diskon dipisahkan sebagai beban agar tidak hilang karena pendapatan dinetokan.
    if money(discount_amount)>0:
        lines.append({'account_code':'5140','debit':discount_amount})
    if revenue_lines:
        for line in revenue_lines:
            lines.append({'account_id':line['account_id'],'credit':line['amount']})
    else:
        lines.append({'account_code':'4000','credit':taxable_amount})
    if money(tax_amount)>0:
        lines.append({'account_code':'2100','credit':tax_amount})
    # Komisi salesman diakui sebagai beban dan kewajiban sampai dibayarkan.
    if money(commission_amount)>0:
        lines.append({'account_code':'5150','debit':commission_amount})
        lines.append({'account_code':'2150','credit':commission_amount})
    if cogs_lines:
        for line in cogs_lines:
            lines.append({'account_id':line['cogs_account_id'],'debit':line['amount']})
            lines.append({'account_id':line['inventory_account_id'],'credit':line['amount']})
    elif money(cogs_amount)>0:
        lines += [{'account_code':'5000','debit':cogs_amount},{'account_code':'1200','credit':cogs_amount}]
    return post_journal(tx,journal_date=sale_date,description=f"Penjualan {invoice_no}",
        source_type='SALE',source_id=sale_id,reference_no=invoice_no,lines=lines,user_id=user_id,department_id=department_id,project_id=project_id)

def post_purchase(tx, *, purchase_id, purchase_no, purchase_date, inventory_amount,
                  expense_amount, tax_amount, paid_amount, balance_due, cash_account_id,
                  supplier_id, user_id, inventory_lines=None, expense_lines=None, department_id=None, project_id=None, payable_account_id=None):
    lines=[]
    if inventory_lines:
        for line in inventory_lines:
            lines.append({'account_id':line['account_id'],'debit':line['amount']})
    elif money(inventory_amount)>0:
        lines.append({'account_code':'1200','debit':inventory_amount})
    if expense_lines:
        for line in expense_lines:
            lines.append({'account_id':line['account_id'],'debit':line['amount']})
    elif money(expense_amount)>0:
        lines.append({'account_code':'5100','debit':expense_amount})
    if money(tax_amount)>0:
        lines.append({'account_code':'1300','debit':tax_amount})
    if money(paid_amount)>0:
        coa=tx.execute("SELECT coa_account_id FROM cash_accounts WHERE id=?",(cash_account_id,)).fetchone()
        lines.append({'account_id':coa['coa_account_id'] if coa and coa['coa_account_id'] else account_id(tx,'1000'),'credit':paid_amount})
    if money(balance_due)>0:
        lines.append({'account_id':int(payable_account_id) if payable_account_id else account_id(tx,'2000'),'credit':balance_due,'partner_id':supplier_id})
    return post_journal(tx,journal_date=purchase_date,description=f"Pembelian {purchase_no}",
        source_type='PURCHASE',source_id=purchase_id,reference_no=purchase_no,lines=lines,user_id=user_id,department_id=department_id,project_id=project_id)


def post_receivable_payment(tx,*,payment_id,payment_no,payment_date,amount,cash_account_id,customer_id,user_id,receivable_account_id=None):
    coa=tx.execute('SELECT coa_account_id FROM cash_accounts WHERE id=?',(cash_account_id,)).fetchone()
    cash_id=coa['coa_account_id'] if coa and coa['coa_account_id'] else account_id(tx,'1000')
    return post_journal(tx,journal_date=payment_date,description=f"Penerimaan piutang {payment_no}",source_type="RECEIVABLE_PAYMENT",source_id=payment_id,reference_no=payment_no,lines=[{"account_id":cash_id,"debit":amount,"credit":0},{"account_id":int(receivable_account_id) if receivable_account_id else account_id(tx,"1100"),"debit":0,"credit":amount,"partner_id":customer_id}],user_id=user_id)

def post_payable_payment(tx,*,payment_id,payment_no,payment_date,amount,cash_account_id,supplier_id,user_id,payable_account_id=None):
    coa=tx.execute('SELECT coa_account_id FROM cash_accounts WHERE id=?',(cash_account_id,)).fetchone()
    cash_id=coa['coa_account_id'] if coa and coa['coa_account_id'] else account_id(tx,'1000')
    return post_journal(tx,journal_date=payment_date,description=f"Pembayaran hutang {payment_no}",source_type="PAYABLE_PAYMENT",source_id=payment_id,reference_no=payment_no,lines=[{"account_id":int(payable_account_id) if payable_account_id else account_id(tx,"2000"),"debit":amount,"credit":0,"partner_id":supplier_id},{"account_id":cash_id,"debit":0,"credit":amount}],user_id=user_id)

def post_opening_balance(tx,*,entity_type,entity_id,reference_no,amount,user_id,opening_date=None,inventory_account_id=None,partner_account_id=None):
    amount=money(amount,"Saldo awal")
    if amount<=0:return None
    opening_date=opening_date or utc_now()[:10]
    if entity_type=="CUSTOMER":
        lines=[{"account_id":int(partner_account_id) if partner_account_id else account_id(tx,"1100"),"debit":amount,"partner_id":entity_id},{"account_code":"3200","credit":amount}]
    elif entity_type=="SUPPLIER":
        lines=[{"account_code":"3200","debit":amount},{"account_id":int(partner_account_id) if partner_account_id else account_id(tx,"2000"),"credit":amount,"partner_id":entity_id}]
    elif entity_type=="PRODUCT":
        lines=[{"account_id":inventory_account_id or account_id(tx,"1200"),"debit":amount},{"account_code":"3200","credit":amount}]
    else:raise ValueError("Jenis saldo awal tidak valid.")
    return post_journal(tx,journal_date=opening_date,description=f"Saldo awal {reference_no}",
        source_type=f"OPENING_{entity_type}",source_id=entity_id,reference_no=reference_no,lines=lines,user_id=user_id)
