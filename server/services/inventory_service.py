from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from ..security import utc_now

QTY = Decimal("0.0001")
MONEY = Decimal("0.01")
AVG_COST = Decimal("0.000001")

def dec(value, label="Nilai"):
    try:
        result = Decimal(str(value if value not in (None, "") else 0))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} tidak valid.")
    if not result.is_finite():
        raise ValueError(f"{label} tidak valid.")
    return result

def qty(value, label="Jumlah"):
    return dec(value, label).quantize(QTY, rounding=ROUND_HALF_UP)

def money(value, label="Nilai"):
    return dec(value, label).quantize(MONEY, rounding=ROUND_HALF_UP)

def avg_cost(value, label="Average cost"):
    return dec(value, label).quantize(AVG_COST, rounding=ROUND_HALF_UP)

def get_default_warehouse_id(tx):
    row = tx.execute("SELECT id FROM warehouses WHERE is_default=1 AND is_active=1 ORDER BY id LIMIT 1").fetchone()
    if not row:
        row = tx.execute("SELECT id FROM warehouses WHERE is_active=1 ORDER BY id LIMIT 1").fetchone()
    if not row:
        raise ValueError("Gudang aktif belum tersedia.")
    return int(row["id"])

def get_balance_state(tx, warehouse_id, product_id):
    row = tx.execute(
        """SELECT quantity, average_cost,COALESCE(book_value,quantity*average_cost) book_value
           FROM inventory_balances WHERE warehouse_id=? AND product_id=?""",
        (warehouse_id, product_id),
    ).fetchone()
    if row:
        return qty(row["quantity"]), avg_cost(row["average_cost"]), money(row["book_value"])
    return Decimal("0.0000"), Decimal("0.000000"), Decimal("0.00")

def get_balance(tx, warehouse_id, product_id):
    q,a,_=get_balance_state(tx,warehouse_id,product_id)
    return q,a

def _ensure_product(tx, product_id):
    row = tx.execute(
        "SELECT id, sku, name, product_type, is_active FROM products WHERE id=?",
        (product_id,),
    ).fetchone()
    if not row or not row["is_active"]:
        raise ValueError("Barang tidak ditemukan atau nonaktif.")
    if row["product_type"] != "STOCK":
        raise ValueError("Jasa tidak memiliki persediaan.")
    return row

def _ensure_warehouse(tx, warehouse_id):
    row = tx.execute(
        "SELECT id, code, name FROM warehouses WHERE id=? AND is_active=1",
        (warehouse_id,),
    ).fetchone()
    if not row:
        raise ValueError("Gudang tidak ditemukan atau nonaktif.")
    return row

def _sync_product_total(tx, product_id, now):
    total = tx.execute(
        "SELECT COALESCE(SUM(quantity),0) total FROM inventory_balances WHERE product_id=?",
        (product_id,),
    ).fetchone()["total"]
    tx.execute("UPDATE products SET stock_qty=?, updated_at=? WHERE id=?", (str(total), now, product_id))
    return qty(total)

def post_movement(
    tx, *, product_id, warehouse_id, movement_type, quantity_change,
    unit_cost=None, reference_type=None, reference_no=None, reason,
    user_id, created_at=None, department_id=None, project_id=None, allow_negative=False
):
    created_at = created_at or utc_now()
    product = _ensure_product(tx, int(product_id))
    warehouse = _ensure_warehouse(tx, int(warehouse_id))
    change = qty(quantity_change, "Perubahan stok")
    if change == 0:
        raise ValueError("Perubahan stok tidak boleh nol.")

    before, avg_before, value_before = get_balance_state(tx, int(warehouse_id), int(product_id))
    after = (before + change).quantize(QTY, rounding=ROUND_HALF_UP)
    if change < 0 and after < 0 and not allow_negative:
        raise ValueError(
            f"Stok {product['sku']} - {product['name']} di {warehouse['name']} tidak cukup. "
            f"Tersedia {before}."
        )

    cost = avg_cost(avg_before if unit_cost in (None, "") else unit_cost, "Harga pokok")
    # Monetary book value is canonical and uses the same 2-decimal movement amount as GL.
    value_change=money(change*cost)
    value_after=money(value_before+value_change)
    avg_after=avg_before
    if after>0:
        avg_after=avg_cost(value_after/after)
    elif after==0:
        avg_after=Decimal("0.000000")
    elif change>0 and before<=0:
        avg_after=cost

    tx.execute(
        """INSERT INTO inventory_balances(warehouse_id, product_id, quantity, average_cost,book_value, updated_at)
           VALUES(?,?,?,?,?,?)
           ON CONFLICT(warehouse_id,product_id) DO UPDATE SET
             quantity=excluded.quantity,average_cost=excluded.average_cost,
             book_value=excluded.book_value,updated_at=excluded.updated_at""",
        (warehouse_id, product_id, str(after), str(avg_after),str(value_after), created_at),
    )
    cur = tx.execute(
        """INSERT INTO inventory_transactions(
             product_id, warehouse_id, movement_type, quantity_change,
             quantity_before, quantity_after, unit_cost, average_cost_before,
             average_cost_after,value_change,value_before,value_after,
             reference_type, reference_no, reason, department_id, project_id, user_id, created_at
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            product_id, warehouse_id, movement_type, str(change), str(before), str(after),
            str(cost), str(avg_before), str(avg_after),str(value_change),str(value_before),str(value_after),
            reference_type, reference_no,reason, department_id, project_id, user_id, created_at,
        ),
    )

    # Legacy card remains filled for backward compatibility.
    tx.execute(
        """INSERT INTO stock_movements(product_id,movement_type,qty_change,qty_before,qty_after,
             reference_no,reason,user_id,created_at)
           VALUES(?,?,?,?,?,?,?,?,?)""",
        (product_id, movement_type, str(change), str(before), str(after),
         reference_no, reason, user_id, created_at),
    )
    total = _sync_product_total(tx, product_id, created_at)
    return {
        "transaction_id": cur.lastrowid,
        "warehouse_id": warehouse_id,
        "product_id": product_id,
        "quantity_before": float(before),
        "quantity_after": float(after),
        "total_quantity": float(total),
        "average_cost_before": float(avg_before),
        "average_cost_after": float(avg_after),
        "unit_cost": float(cost),
        "value_change": float(value_change),"value_before":float(value_before),"value_after":float(value_after),
    }

def stock_in(tx, *, product_id, warehouse_id, quantity, unit_cost,
             reference_type, reference_no, reason, user_id, created_at=None):
    amount = qty(quantity)
    if amount <= 0:
        raise ValueError("Jumlah stok masuk harus lebih dari nol.")
    return post_movement(
        tx, product_id=product_id, warehouse_id=warehouse_id, movement_type="IN",
        quantity_change=amount, unit_cost=unit_cost, reference_type=reference_type,
        reference_no=reference_no, reason=reason, user_id=user_id, created_at=created_at,
    )

def stock_out(tx, *, product_id, warehouse_id, quantity,
              reference_type, reference_no, reason, user_id, created_at=None, allow_negative=False):
    amount = qty(quantity)
    if amount <= 0:
        raise ValueError("Jumlah stok keluar harus lebih dari nol.")
    before, avg = get_balance(tx, warehouse_id, product_id)
    # Compatibility repair: older/imported stock can have quantity but average_cost=0.
    # Use the product purchase price as HPP fallback so sales still post COGS correctly.
    if avg <= 0 and before != 0:
        prow=tx.execute("SELECT purchase_price FROM products WHERE id=?",(int(product_id),)).fetchone()
        fallback=money(prow["purchase_price"] if prow else 0)
        if fallback > 0:
            avg=fallback
            tx.execute("UPDATE inventory_balances SET average_cost=?,updated_at=? WHERE warehouse_id=? AND product_id=?",(str(avg),created_at or utc_now(),int(warehouse_id),int(product_id)))
    result = post_movement(
        tx, product_id=product_id, warehouse_id=warehouse_id, movement_type="OUT",
        quantity_change=-amount, unit_cost=avg, reference_type=reference_type,
        reference_no=reference_no, reason=reason, user_id=user_id, created_at=created_at,
        allow_negative=allow_negative,
    )
    result["cost_of_goods"] = float(abs(Decimal(str(result["value_change"]))))
    return result

def adjust(tx, *, product_id, warehouse_id, quantity_change, reason,
           reference_no, user_id, created_at=None, department_id=None, project_id=None):
    change = qty(quantity_change)
    before, avg = get_balance(tx, warehouse_id, product_id)
    if avg <= 0:
        row=tx.execute("SELECT purchase_price FROM products WHERE id=?",(int(product_id),)).fetchone()
        fallback=money(row["purchase_price"] if row else 0)
        if fallback>0: avg=fallback
    return post_movement(
        tx, product_id=product_id, warehouse_id=warehouse_id, movement_type="ADJUSTMENT",
        quantity_change=change, unit_cost=avg, reference_type="ADJUSTMENT",
        reference_no=reference_no, reason=reason, user_id=user_id, created_at=created_at,
        department_id=department_id,project_id=project_id,
    )

def transfer(tx, *, product_id, source_warehouse_id, target_warehouse_id,
             quantity, reference_no, reason, user_id, created_at=None):
    if int(source_warehouse_id) == int(target_warehouse_id):
        raise ValueError("Gudang asal dan tujuan tidak boleh sama.")
    amount = qty(quantity)
    if amount <= 0:
        raise ValueError("Jumlah transfer harus lebih dari nol.")
    _, avg = get_balance(tx, int(source_warehouse_id), int(product_id))
    out_result = post_movement(
        tx, product_id=product_id, warehouse_id=source_warehouse_id,
        movement_type="TRANSFER_OUT", quantity_change=-amount, unit_cost=avg,
        reference_type="TRANSFER", reference_no=reference_no, reason=reason,
        user_id=user_id, created_at=created_at,
    )
    in_result = post_movement(
        tx, product_id=product_id, warehouse_id=target_warehouse_id,
        movement_type="TRANSFER_IN", quantity_change=amount, unit_cost=avg,
        reference_type="TRANSFER", reference_no=reference_no, reason=reason,
        user_id=user_id, created_at=created_at,
    )
    return {"source": out_result, "target": in_result}


def reassign_warehouse_balance(tx, *, product_id, source_warehouse_id, target_warehouse_id, reason, user_id, created_at=None):
    source_warehouse_id=int(source_warehouse_id);target_warehouse_id=int(target_warehouse_id)
    if source_warehouse_id==target_warehouse_id:return {"moved":0.0}
    amount,avg=get_balance(tx,source_warehouse_id,int(product_id))
    if amount==0:return {"moved":0.0}
    created_at=created_at or utc_now()
    if amount>0:
        result=transfer(tx,product_id=product_id,source_warehouse_id=source_warehouse_id,target_warehouse_id=target_warehouse_id,
          quantity=amount,reference_no=f"MASTER-WH-{product_id}",reason=reason,user_id=user_id,created_at=created_at)
        result["moved"]=float(amount);return result
    q=abs(amount)
    src=post_movement(tx,product_id=product_id,warehouse_id=source_warehouse_id,movement_type="WAREHOUSE_REASSIGN_OUT",
      quantity_change=q,unit_cost=avg,reference_type="WAREHOUSE_REASSIGN",reference_no=f"MASTER-WH-{product_id}",
      reason=reason,user_id=user_id,created_at=created_at,allow_negative=True)
    dst=post_movement(tx,product_id=product_id,warehouse_id=target_warehouse_id,movement_type="WAREHOUSE_REASSIGN_IN",
      quantity_change=-q,unit_cost=avg,reference_type="WAREHOUSE_REASSIGN",reference_no=f"MASTER-WH-{product_id}",
      reason=reason,user_id=user_id,created_at=created_at,allow_negative=True)
    return {"moved":float(amount),"source":src,"target":dst}
