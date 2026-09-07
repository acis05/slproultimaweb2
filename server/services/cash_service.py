from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from ..security import utc_now

MONEY = Decimal("0.01")


def _normalize_decimal_text(value):
    """Normalize angka dari transaksi lama, Excel, dan rekening koran PDF."""
    if value in (None, ""):
        return "0"
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (int, float)):
        return str(value)

    import re
    text=str(value).strip()
    negative=text.startswith("-") or (text.startswith("(") and text.endswith(")"))
    text=text.replace("Rp", "").replace("rp", "")
    # Sisakan angka dan separator saja; membuang DB/CR, pipa, dan teks PDF.
    text=re.sub(r"[^0-9.,]", "", text)
    if not text:
        raise ValueError("Angka kosong")

    if "," in text and "." in text:
        # Separator terakhir adalah desimal, separator sebelumnya ribuan.
        if text.rfind(",") > text.rfind("."):
            text=text.replace(".", "").replace(",", ".")
        else:
            text=text.replace(",", "")
    elif "," in text:
        parts=text.split(",")
        if len(parts)==2 and len(parts[-1]) in (1,2):
            text=parts[0]+"."+parts[1]
        else:
            text="".join(parts)
    elif "." in text:
        parts=text.split(".")
        if len(parts)>2:
            # 1.234.567 atau 1.234.567, yang seluruhnya separator ribuan.
            text="".join(parts)
        elif len(parts)==2 and len(parts[-1])==3:
            # Format Indonesia ribuan, contoh 60.000.
            text="".join(parts)
    if negative and text != "0":
        text="-"+text
    return text

def money(value, label="Nilai", allow_negative=False):
    """Parse nilai uang. Nominal transaksi tetap >= 0, saldo akun boleh negatif."""
    try:
        result = Decimal(_normalize_decimal_text(value)).quantize(
            MONEY, rounding=ROUND_HALF_UP
        )
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} tidak valid.")
    if not result.is_finite() or (result < 0 and not allow_negative):
        raise ValueError(f"{label} tidak valid.")
    return result


def next_number(tx, transaction_date, prefix):
    period = str(transaction_date)[:7].replace("-", "")
    key = f"CASH-{prefix}-{period}"
    row = tx.execute(
        "SELECT current_value FROM document_sequences WHERE sequence_key=?", (key,)
    ).fetchone()
    value = int(row["current_value"]) + 1 if row else 1
    tx.execute(
        """INSERT INTO document_sequences(sequence_key,current_value,updated_at)
           VALUES(?,?,?)
           ON CONFLICT(sequence_key) DO UPDATE SET
             current_value=excluded.current_value,
             updated_at=excluded.updated_at""",
        (key, value, utc_now()),
    )
    return f"{prefix}-{period}-{value:06d}"


def post(
    tx, *, account_id, transaction_date, transaction_type, amount,
    description, reference_no, user_id, transfer_group=None,
    transaction_no=None, allow_negative=True, department_id=None, project_id=None
):
    if transaction_type not in ("IN", "OUT", "TRANSFER_IN", "TRANSFER_OUT"):
        raise ValueError("Jenis transaksi kas tidak valid.")
    amount = money(amount, "Jumlah")
    if amount <= 0:
        raise ValueError("Jumlah harus lebih dari nol.")

    account = tx.execute(
        "SELECT * FROM cash_accounts WHERE id=? AND is_active=1", (int(account_id),)
    ).fetchone()
    if not account:
        raise ValueError("Akun kas/bank tidak ditemukan atau nonaktif.")

    before = money(account["current_balance"], "Saldo akun", allow_negative=True)
    delta = amount if transaction_type in ("IN", "TRANSFER_IN") else -amount
    after = (before + delta).quantize(MONEY, rounding=ROUND_HALF_UP)
    if after < 0 and not allow_negative:
        raise ValueError(
            f"Saldo {account['name']} tidak cukup. Saldo tersedia {before}."
        )

    if not transaction_no:
        prefix = "KM" if transaction_type == "IN" else "KK"
        transaction_no = next_number(tx, transaction_date, prefix)

    now = utc_now()
    tx.execute(
        "UPDATE cash_accounts SET current_balance=?,updated_at=? WHERE id=?",
        (str(after), now, account_id),
    )
    cursor = tx.execute(
        """INSERT INTO cash_transactions(
             transaction_no,transaction_date,account_id,transaction_type,
             amount,balance_before,balance_after,description,reference_no,
             transfer_group,department_id,project_id,user_id,created_at
           ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            transaction_no, str(transaction_date)[:10], account_id,
            transaction_type, str(amount), str(before), str(after), description,
            reference_no, transfer_group, department_id, project_id, user_id, now,
        ),
    )
    return {
        "id": cursor.lastrowid,
        "transaction_no": transaction_no,
        "amount": float(amount),
        "balance_before": float(before),
        "balance_after": float(after),
    }


def transfer(
    tx, *, source_account_id, target_account_id, transaction_date,
    amount, description, reference_no, user_id
):
    if int(source_account_id) == int(target_account_id):
        raise ValueError("Akun asal dan tujuan tidak boleh sama.")
    transfer_no = next_number(tx, transaction_date, "TR")
    source = post(
        tx, account_id=source_account_id, transaction_date=transaction_date,
        transaction_type="TRANSFER_OUT", amount=amount,
        description=description, reference_no=reference_no, user_id=user_id,
        transfer_group=transfer_no, transaction_no=f"{transfer_no}-OUT",
        allow_negative=True,
    )
    target = post(
        tx, account_id=target_account_id, transaction_date=transaction_date,
        transaction_type="TRANSFER_IN", amount=amount,
        description=description, reference_no=reference_no, user_id=user_id,
        transfer_group=transfer_no, transaction_no=f"{transfer_no}-IN",
    )
    return {"transfer_no": transfer_no, "source": source, "target": target}
