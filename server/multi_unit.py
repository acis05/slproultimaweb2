from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

QTY=Decimal("0.0001")
MONEY=Decimal("0.01")

def _dec(value,label="Nilai"):
    try: result=Decimal(str(value if value not in (None,"") else 0))
    except (InvalidOperation,ValueError,TypeError): raise ValueError(f"{label} tidak valid.")
    if not result.is_finite(): raise ValueError(f"{label} tidak valid.")
    return result

def product_units(conn,product_id,base_unit_id=None,base_purchase=0,base_sell=0):
    rows=[dict(x) for x in conn.execute("""SELECT pu.*,u.code unit_code,u.name unit_name,u.decimals
      FROM product_units pu JOIN units u ON u.id=pu.unit_id
      WHERE pu.product_id=? AND pu.is_active=1 ORDER BY pu.is_base DESC,u.name""",(int(product_id),)).fetchall()]
    if rows:return rows
    if base_unit_id:
        u=conn.execute("SELECT code,name,decimals FROM units WHERE id=?",(int(base_unit_id),)).fetchone()
        if u:return [{"product_id":int(product_id),"unit_id":int(base_unit_id),"unit_code":u["code"],"unit_name":u["name"],"decimals":u["decimals"],"conversion_ratio":1.0,"purchase_price":float(base_purchase or 0),"selling_price":float(base_sell or 0),"is_base":True,"is_active":True}]
    return []

def save_product_units(tx,product_id,base_unit_id,rows,base_purchase=0,base_sell=0):
    tx.execute("DELETE FROM product_units WHERE product_id=?",(int(product_id),))
    cleaned=[]; seen=set()
    for raw in (rows or []):
        try: uid=int(raw.get("unit_id"))
        except Exception: continue
        if uid in seen: continue
        seen.add(uid)
        ratio=_dec(raw.get("conversion_ratio",1),"Rasio konversi")
        if ratio<=0: raise ValueError("Rasio konversi harus lebih dari nol.")
        buy=_dec(raw.get('purchase_price',0),'Harga beli satuan')
        sell=_dec(raw.get('selling_price',0),'Harga jual satuan')
        if buy<=0: buy=(_dec(base_purchase)*ratio).quantize(MONEY,rounding=ROUND_HALF_UP)
        if sell<=0: sell=(_dec(base_sell)*ratio).quantize(MONEY,rounding=ROUND_HALF_UP)
        cleaned.append((uid,ratio,buy,sell))
    if int(base_unit_id) not in seen: cleaned.insert(0,(int(base_unit_id),Decimal("1"),_dec(base_purchase),_dec(base_sell)))
    for uid,ratio,buy,sell in cleaned:
        if not tx.execute("SELECT 1 FROM units WHERE id=? AND is_active=1",(uid,)).fetchone():raise ValueError("Satuan alternatif tidak ditemukan atau nonaktif.")
        is_base=1 if uid==int(base_unit_id) else 0
        if is_base: ratio=Decimal("1"); buy=_dec(base_purchase); sell=_dec(base_sell)
        tx.execute("""INSERT INTO product_units(product_id,unit_id,conversion_ratio,purchase_price,selling_price,is_base,is_active) VALUES(?,?,?,?,?,?,1)""",(int(product_id),uid,str(ratio),str(buy),str(sell),is_base))

def resolve(tx,product,unit_id,entered_qty,entered_price,price_kind):
    uid=int(unit_id or product["unit_id"]); qty=_dec(entered_qty,"Qty")
    if qty<=0: raise ValueError("Qty harus lebih dari nol.")
    row=tx.execute("""SELECT pu.*,u.code unit_code FROM product_units pu JOIN units u ON u.id=pu.unit_id WHERE pu.product_id=? AND pu.unit_id=? AND pu.is_active=1""",(int(product["id"]),uid)).fetchone()
    if row:
        ratio=_dec(row["conversion_ratio"],"Rasio konversi"); default_price=row["selling_price"] if price_kind=="SELL" else row["purchase_price"]; code=row["unit_code"]
    elif uid==int(product["unit_id"]):
        ratio=Decimal("1"); default_price=product["selling_price"] if price_kind=="SELL" else product["purchase_price"]; u=tx.execute("SELECT code FROM units WHERE id=?",(uid,)).fetchone(); code=u["code"] if u else ""
    else:
        # Legacy databases may have an empty product_units map after upgrades.
        # If so, normalize the transaction to the product base unit instead of blocking save.
        mapped=tx.execute("SELECT 1 FROM product_units WHERE product_id=? AND is_active=1 LIMIT 1",(int(product["id"]),)).fetchone()
        if not mapped:
            uid=int(product["unit_id"]);ratio=Decimal("1")
            default_price=product["selling_price"] if price_kind=="SELL" else product["purchase_price"]
            u=tx.execute("SELECT code FROM units WHERE id=?",(uid,)).fetchone();code=u["code"] if u else ""
        else:
            raise ValueError("Satuan tidak tersedia untuk barang ini. Pilih satuan yang terdaftar pada master barang.")
    price=_dec(entered_price if entered_price not in (None,"") else default_price,"Harga satuan")
    return {"unit_id":uid,"unit_code":code,"ratio":ratio,"entered_qty":qty,"base_qty":(qty*ratio).quantize(QTY,rounding=ROUND_HALF_UP),"price":price}
