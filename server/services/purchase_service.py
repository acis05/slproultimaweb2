from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from ..security import utc_now
from . import inventory_service, cash_service, accounting_service
from .. import multi_unit
from datetime import date, timedelta

QTY = Decimal("0.0001")
MONEY = Decimal("0.01")

def _decimal_text(value):
    if value in (None, ""): return "0"
    if isinstance(value, (int, float, Decimal)): return str(value)
    text=str(value).strip().replace("Rp","").replace("rp","").replace(" ","")
    neg=text.startswith("(") and text.endswith(")"); text=text.strip("()")
    if "," in text and "." in text:
        text=text.replace(".","").replace(",",".") if text.rfind(",")>text.rfind(".") else text.replace(",","")
    elif "," in text:
        parts=text.split(","); text=parts[0].replace(".","")+"."+parts[1] if len(parts)==2 and len(parts[1])<=4 else "".join(parts)
    elif text.count(".")>1 or (text.count(".")==1 and len(text.rsplit(".",1)[1])==3): text=text.replace(".","")
    return ("-" if neg else "")+text

def _dec(value, label, allow_negative=False):
    try:
        result = Decimal(_decimal_text(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} tidak valid.")
    if not result.is_finite():
        raise ValueError(f"{label} tidak valid.")
    if not allow_negative and result < 0:
        raise ValueError(f"{label} tidak boleh negatif.")
    return result

def _qty(value, label="Jumlah"):
    value = _dec(value, label)
    return value.quantize(QTY, rounding=ROUND_HALF_UP)

def next_goods_receipt_no(tx,purchase_date):
    prefix=f"GR-{str(purchase_date)[:7].replace('-','')}"
    row=tx.execute("SELECT goods_receipt_no FROM purchases WHERE goods_receipt_no LIKE ? ORDER BY id DESC LIMIT 1",(prefix+'-%',)).fetchone()
    seq=int(row["goods_receipt_no"].rsplit('-',1)[-1])+1 if row and row["goods_receipt_no"] else 1
    return f"{prefix}-{seq:06d}"

def _money(value, label="Nilai"):
    value = _dec(value, label)
    return value.quantize(MONEY, rounding=ROUND_HALF_UP)

def next_purchase_no(tx, purchase_date):
    period = str(purchase_date)[:7].replace("-", "")
    key = f"PURCHASE-{period}"
    row = tx.execute(
        "SELECT current_value FROM document_sequences WHERE sequence_key=?",
        (key,),
    ).fetchone()
    next_value = int(row["current_value"]) + 1 if row else 1
    tx.execute(
        """INSERT INTO document_sequences(sequence_key,current_value,updated_at)
           VALUES(?,?,?)
           ON CONFLICT(sequence_key) DO UPDATE SET
             current_value=excluded.current_value,
             updated_at=excluded.updated_at""",
        (key, next_value, utc_now()),
    )
    return f"PB-{period}-{next_value:06d}"

def create_purchase(tx, *, actor, data, client_ip, audit_callback):
    department_id=data.get("department_id") or None
    project_id=data.get("project_id") or None
    if department_id is not None:
        try:department_id=int(department_id)
        except Exception:raise ValueError("Departemen tidak valid.")
        if not tx.execute("SELECT 1 FROM departments WHERE id=? AND is_active=1",(department_id,)).fetchone():
            raise ValueError("Departemen tidak ditemukan atau nonaktif.")
    if project_id is not None:
        try:project_id=int(project_id)
        except Exception:raise ValueError("Proyek tidak valid.")
        if not tx.execute("SELECT 1 FROM projects WHERE id=? AND is_active=1",(project_id,)).fetchone():
            raise ValueError("Proyek tidak ditemukan atau nonaktif.")
    purchase_date = str(data.get("purchase_date") or "")[:10]
    if len(purchase_date) != 10:
        raise ValueError("Tanggal pembelian wajib diisi.")

    try:
        supplier_id = int(data.get("supplier_id"))
        warehouse_id = int(data.get("warehouse_id"))
    except Exception:
        raise ValueError("Supplier dan gudang tujuan wajib dipilih.")

    supplier = tx.execute(
        """SELECT * FROM business_partners
           WHERE id=? AND is_active=1
             AND partner_type IN ('SUPPLIER','BOTH')""",
        (supplier_id,),
    ).fetchone()
    if not supplier:
        raise ValueError("Supplier tidak ditemukan atau nonaktif.")

    warehouse = tx.execute(
        "SELECT id,name FROM warehouses WHERE id=? AND is_active=1",
        (warehouse_id,),
    ).fetchone()
    if not warehouse:
        raise ValueError("Gudang tujuan tidak ditemukan atau nonaktif.")

    payment_method = str(data.get("payment_method", data.get("payment_type", "CASH"))).upper()
    if payment_method not in ("CASH", "TRANSFER", "CREDIT"):
        raise ValueError("Metode pembayaran harus Tunai, Transfer, atau Kredit.")
    payment_type = "CREDIT" if payment_method == "CREDIT" else "CASH"

    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Minimal satu item pembelian wajib diisi.")

    normalized = []
    subtotal = Decimal("0.00")
    for index, item in enumerate(items, start=1):
        try:
            product_id = int(item.get("product_id"))
        except Exception:
            raise ValueError(f"Barang pada baris {index} tidak valid.")
        product = tx.execute(
            "SELECT * FROM products WHERE id=? AND is_active=1",
            (product_id,),
        ).fetchone()
        if not product:
            raise ValueError(f"Barang pada baris {index} tidak ditemukan.")

        unit=multi_unit.resolve(tx,product,item.get("unit_id"),item.get("qty"),item.get("unit_cost"),"BUY")
        entered_quantity=unit["entered_qty"]
        quantity=unit["base_qty"]
        unit_cost=_money(unit["price"], f"Harga beli baris {index}")
        discount_mode = str(item.get("discount_mode", "AMOUNT")).upper()
        discount_value = _money(item.get("discount_value", item.get("discount_amount", 0)), f"Diskon baris {index}")
        if quantity <= 0:
            raise ValueError(f"Jumlah baris {index} harus lebih dari nol.")

        gross = (entered_quantity * unit_cost).quantize(MONEY, rounding=ROUND_HALF_UP)
        if discount_mode == "PERCENT":
            if discount_value > 100: raise ValueError(f"Diskon persen baris {index} tidak boleh lebih dari 100%.")
            discount_percent = discount_value
            discount = (gross * discount_value / Decimal("100")).quantize(MONEY, rounding=ROUND_HALF_UP)
        else:
            discount = discount_value
            if discount > gross: raise ValueError(f"Diskon baris {index} melebihi nilai barang.")
            discount_percent = (discount/gross*Decimal("100")).quantize(MONEY, rounding=ROUND_HALF_UP) if gross else Decimal("0")
        line_total = (gross - discount).quantize(MONEY, rounding=ROUND_HALF_UP)
        normalized.append((product, quantity, unit_cost, discount_percent, discount, line_total, unit))
        subtotal += line_total

    header_mode = str(data.get("discount_mode", "AMOUNT")).upper()
    header_value = _money(data.get("discount_value", data.get("discount_amount", 0)), "Diskon transaksi")
    if header_mode == "PERCENT":
        if header_value > 100: raise ValueError("Diskon transaksi persen tidak boleh lebih dari 100%.")
        header_discount = (subtotal * header_value / Decimal("100")).quantize(MONEY, rounding=ROUND_HALF_UP)
    else: header_discount = header_value
    if header_discount > subtotal: raise ValueError("Diskon transaksi melebihi subtotal.")
    taxable = subtotal - header_discount
    tax_percent = _money(data.get("tax_percent",0), "PPN")
    if tax_percent > 100: raise ValueError("PPN tidak boleh lebih dari 100%.")
    tax_amount = (taxable * tax_percent / Decimal("100")).quantize(MONEY, rounding=ROUND_HALF_UP)
    total = (taxable + tax_amount).quantize(MONEY, rounding=ROUND_HALF_UP)

    paid_requested = _money(data.get("paid_amount", 0), "Jumlah bayar")
    cash_account_id = data.get("cash_account_id") or None
    if payment_method in ("CASH","TRANSFER"):
        if not cash_account_id: raise ValueError("Akun kas/bank wajib dipilih.")
        if paid_requested < total: raise ValueError("Pembelian tunai/transfer harus dibayar penuh.")
        paid = total; balance = Decimal("0.00"); due_date = None
    else:
        if paid_requested > total:
            raise ValueError("Pembayaran awal tidak boleh melebihi total pembelian.")
        paid = paid_requested
        balance = (total - paid).quantize(MONEY, rounding=ROUND_HALF_UP)
        raw_term = data.get("payment_term_days")
        if raw_term in (None, ""):
            raw_term = supplier["payment_term_days"] or 0
        try:
            term = int(str(raw_term).strip())
        except (TypeError, ValueError):
            raise ValueError("Termin pembayaran harus berupa jumlah hari, misalnya 0, 14, atau 30.")
        if term < 0 or term > 3650:
            raise ValueError("Termin pembayaran harus antara 0 sampai 3650 hari.")
        due_date = str(data.get("due_date") or (date.fromisoformat(purchase_date)+timedelta(days=term)).isoformat())[:10]
        if paid > 0 and not cash_account_id: raise ValueError("Akun kas/bank wajib dipilih untuk pembayaran awal.")

    from .. import order_dp
    purchase_order_id=data.get("purchase_order_id") or None
    order_dp.validate_order_fulfillment(tx,"purchase",purchase_order_id,[(x[0]["id"],x[1]) for x in normalized])
    now = utc_now()
    purchase_no = str(data.get("purchase_no") or "").strip() or next_purchase_no(tx, purchase_date)
    supplier_invoice_no=str(data.get("supplier_invoice_no") or "").strip() or None
    goods_receipt_no=str(data.get("goods_receipt_no") or "").strip() or next_goods_receipt_no(tx,purchase_date)
    if goods_receipt_no and tx.execute("SELECT 1 FROM purchases WHERE goods_receipt_no=? COLLATE NOCASE",(goods_receipt_no,)).fetchone():
        raise ValueError("Nomor Good Receive sudah digunakan.")
    notes = str(data.get("notes", "")).strip() or None

    cur = tx.execute(
        """INSERT INTO purchases(
             purchase_no,supplier_invoice_no,goods_receipt_no,purchase_date,supplier_id,warehouse_id,department_id,project_id,payment_type,payment_method,cash_account_id,due_date,tax_percent,tax_amount,
             subtotal,discount_amount,total_amount,paid_amount,balance_due,notes,status,user_id,created_at,updated_at
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'POSTED',?,?,?)""",
        (purchase_no,supplier_invoice_no,goods_receipt_no,purchase_date,supplier_id,warehouse_id,department_id,project_id,payment_type,payment_method,cash_account_id,due_date,str(tax_percent),str(tax_amount),
         str(subtotal),str(header_discount),str(total),str(paid),str(balance),notes,actor["id"],now,now),
    )
    purchase_id = cur.lastrowid
    if purchase_order_id: tx.execute("UPDATE purchases SET purchase_order_id=? WHERE id=?",(int(purchase_order_id),purchase_id))

    inventory_amount=Decimal("0.00");expense_amount=Decimal("0.00")
    inventory_groups={};expense_groups={}
    allocated=Decimal("0.00")
    for line_index,(product, quantity, unit_cost, discount_percent, discount, line_total, unit) in enumerate(normalized):
        if subtotal>0:
            if line_index==len(normalized)-1:
                net_line=taxable-allocated
            else:
                net_line=(line_total*taxable/subtotal).quantize(MONEY,rounding=ROUND_HALF_UP)
                allocated+=net_line
        else: net_line=Decimal("0.00")
        tx.execute(
            """INSERT INTO purchase_items(
                 purchase_id,product_id,sku,product_name,product_type,
                 qty,entered_qty,unit_id,unit_code,conversion_ratio,unit_cost,discount_percent,discount_amount,line_total
               ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (purchase_id,product["id"],product["sku"],product["name"],product["product_type"],str(quantity),str(unit["entered_qty"]),unit["unit_id"],unit["unit_code"],str(unit["ratio"]),str(unit_cost),str(discount_percent),str(discount),str(line_total)),
        )
        if product["product_type"] == "STOCK":
            inventory_amount += net_line
            inventory_aid=product["inventory_account_id"]
            if not inventory_aid: raise ValueError(f"Akun persediaan {product['sku']} belum diatur.")
            inventory_groups[inventory_aid]=inventory_groups.get(inventory_aid,Decimal("0.00"))+net_line
            effective_cost = (
                net_line / quantity
            ).quantize(MONEY, rounding=ROUND_HALF_UP)
            inventory_service.stock_in(
                tx,
                product_id=product["id"],
                warehouse_id=warehouse_id,
                quantity=quantity,
                unit_cost=effective_cost,
                reference_type="PURCHASE",
                reference_no=purchase_no,
                reason="Pembelian",
                user_id=actor["id"],
                created_at=now,
            )
            tx.execute(
                "UPDATE products SET purchase_price=?,updated_at=? WHERE id=?",
                (str(effective_cost), now, product["id"]),
            )
        else:
            expense_amount += net_line
            expense_id=product["cogs_account_id"] or accounting_service.account_id(tx,"5100")
            expense_groups[int(expense_id)]=expense_groups.get(int(expense_id),Decimal("0.00"))+net_line

    if paid > 0:
        cash_service.post(tx,account_id=int(cash_account_id),transaction_date=purchase_date,transaction_type="OUT",amount=paid,description=f"Pembayaran pembelian {purchase_no}",reference_no=purchase_no,user_id=actor["id"],department_id=department_id,project_id=project_id,allow_negative=True)

    accounting_service.post_purchase(tx,purchase_id=purchase_id,purchase_no=purchase_no,
        purchase_date=purchase_date,inventory_amount=inventory_amount,expense_amount=expense_amount,
        tax_amount=tax_amount,paid_amount=paid,balance_due=balance,cash_account_id=cash_account_id,
        supplier_id=supplier_id,user_id=actor["id"],
        inventory_lines=[{"account_id":aid,"amount":amount} for aid,amount in inventory_groups.items() if amount>0],
        expense_lines=[{"account_id":aid,"amount":amount} for aid,amount in expense_groups.items() if amount>0],
        department_id=department_id,project_id=project_id,payable_account_id=(supplier["payable_account_id"] if supplier else None))

    audit_callback(
        actor["id"],
        "PURCHASE_CREATED",
        "purchase",
        purchase_id,
        {
            "purchase_no": purchase_no,
            "supplier_id": supplier_id,
            "warehouse_id": warehouse_id,
            "total": float(total),
            "payment_type": payment_type,"payment_method": payment_method,"tax_amount": float(tax_amount),
        },
        client_ip,
        tx,
    )

    order_dp.close_order_if_fulfilled(tx,"purchase",purchase_order_id)
    return {
        "id": purchase_id,
        "purchase_no": purchase_no,
        "supplier_invoice_no": supplier_invoice_no,
        "goods_receipt_no": goods_receipt_no,
        "subtotal": float(subtotal),
        "discount_amount": float(header_discount),"tax_amount": float(tax_amount),
        "total_amount": float(total),
        "paid_amount": float(paid),
        "change_amount": float(max(Decimal("0"), paid_requested - total)),
        "balance_due": float(balance),
        "warehouse_id": warehouse_id,"due_date": due_date,
    }
