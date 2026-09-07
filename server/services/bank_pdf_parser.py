import io
import re
from datetime import date

MONTHS={"JANUARI":1,"FEBRUARI":2,"MARET":3,"APRIL":4,"MEI":5,"JUNI":6,
"JULI":7,"AGUSTUS":8,"SEPTEMBER":9,"OKTOBER":10,"NOVEMBER":11,"DESEMBER":12}
START_RE=re.compile(r"^\d{2}/\d{2}\s+")
MONEY_RE=re.compile(r"\d{1,3}(?:,\d{3})+\.\d{2}")
DEBIT_RE=re.compile(r"(\d{1,3}(?:,\d{3})+\.\d{2})\s+DB\b")
IGNORE=("REKENING TAHAPAN","REKENING GIRO","KCP ","NO. REKENING","HALAMAN",
"PERIODE","MATA UANG","CATATAN:","Apabila nasabah","Rekening ini",
"telah menyetujui","BCA berhak","•","TANGGAL KETERANGAN",
"Bersambung ke halaman berikut","SALDO AWAL :","MUTASI CR :","MUTASI DB :","SALDO AKHIR :")

def amount(v):return float(v.replace(",",""))

def period(text):
    m=re.search(r"PERIODE\s*:\s*([A-Z]+)\s+(\d{4})",text.upper())
    if not m:raise ValueError("Periode rekening koran tidak ditemukan.")
    month=MONTHS.get(m.group(1))
    if not month:raise ValueError("Nama bulan rekening koran tidak dikenali.")
    return int(m.group(2)),month

def clean(text):
    out=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line:continue
        if any(line.startswith(x) for x in IGNORE):continue
        if re.fullmatch(r"\d+\s*/",line):continue
        out.append(line)
    return out

def parse_bca_statement_text(text):
    year,statement_month=period(text)
    blocks=[];current=[]
    for line in clean(text):
        if START_RE.match(line):
            if current:blocks.append(current)
            current=[line]
        elif current:current.append(line)
    if current:blocks.append(current)

    opening=None;items=[]
    for block in blocks:
        first=block[0];joined=" ".join(block)
        if "SALDO AWAL" in first:
            values=MONEY_RE.findall(joined)
            if values:opening=amount(values[-1])
            continue
        day,month=map(int,first[:5].split("/"))
        if month!=statement_month:continue
        debits=DEBIT_RE.findall(joined)
        values=MONEY_RE.findall(joined)
        if debits:
            direction="DEBIT";value=amount(debits[-1])
            bm=re.search(r"\d{1,3}(?:,\d{3})+\.\d{2}\s+DB(?:\s+(\d{1,3}(?:,\d{3})+\.\d{2}))?\s*$",joined)
            balance=amount(bm.group(1)) if bm and bm.group(1) else None
        else:
            if not values:continue
            direction="CREDIT"
            value=amount(values[-2] if len(values)>=2 else values[-1])
            balance=amount(values[-1]) if len(values)>=2 else None
        parts=list(block);parts[0]=parts[0][6:].strip()
        desc=" | ".join(x for x in parts if x)
        desc=re.sub(r"\s+\d{1,3}(?:,\d{3})+\.\d{2}\s+DB(?:\s+\d{1,3}(?:,\d{3})+\.\d{2})?\s*$","",desc)
        if direction=="CREDIT":
            desc=re.sub(r"\s+\d{1,3}(?:,\d{3})+\.\d{2}(?:\s+\d{1,3}(?:,\d{3})+\.\d{2})?\s*$","",desc)
        items.append({"transaction_date":date(year,month,day).isoformat(),
        "description":desc.strip(" |"),"direction":direction,
        "debit":value if direction=="DEBIT" else 0.0,
        "credit":value if direction=="CREDIT" else 0.0,
        "amount":value,"balance":balance})
    if not items:raise ValueError("Tidak ada transaksi yang berhasil dibaca.")
    return {"bank_name":"BCA","period_year":year,"period_month":statement_month,
    "opening_balance":opening,"row_count":len(items),
    "debit_count":sum(x["direction"]=="DEBIT" for x in items),
    "credit_count":sum(x["direction"]=="CREDIT" for x in items),
    "debit_total":sum(x["debit"] for x in items),
    "credit_total":sum(x["credit"] for x in items),"items":items}

def parse_bca_statement_pdf(pdf_bytes):
    try:from pypdf import PdfReader
    except ImportError as exc:raise RuntimeError("Jalankan INSTALL_PDF_SUPPORT.bat.") from exc
    text="\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(pdf_bytes)).pages)
    upper=text.upper()
    if "REKENING TAHAPAN" not in upper and "REKENING GIRO" not in upper:
        raise ValueError("Format PDF belum dikenali. Mendukung BCA Tahapan dan Giro.")
    return parse_bca_statement_text(text)

BANK_SIGNATURES=[
 ("BCA",("BCA","REKENING TAHAPAN","REKENING GIRO")),
 ("MANDIRI",("BANK MANDIRI","LIVIN'","LIVIN BY MANDIRI")),
 ("BRI",("BANK RAKYAT INDONESIA","BANK BRI","BRIMO")),
 ("BNI",("BANK NEGARA INDONESIA","BANK BNI","BNI MOBILE")),
 ("CIMB NIAGA",("CIMB NIAGA","CIMB")),
 ("PERMATA",("PERMATABANK","BANK PERMATA")),
 ("DANAMON",("BANK DANAMON","DANAMON")),
 ("OCBC",("OCBC","OCBC NISP")),
 ("BSI",("BANK SYARIAH INDONESIA","BSI")),
 ("MAYBANK",("MAYBANK","BANK MAYBANK")),
 ("PANIN",("PANIN BANK","BANK PANIN")),
]

GENERIC_DATE_RE=re.compile(r"(?<!\d)(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?(?!\d)")
GENERIC_MONEY_RE=re.compile(r"(?<!\d)(?:RP\s*)?[-+]?\d[\d.,]*\d(?:[.,]\d{2})?(?!\d)",re.I)

def detect_bank(text):
    upper=(text or "").upper()
    best=None;score=0
    for name,sigs in BANK_SIGNATURES:
        hits=sum(1 for sig in sigs if sig in upper)
        if hits>score:best=name;score=hits
    return best or "BANK LAIN"

def _generic_money(value):
    text=str(value or "").strip().upper().replace("RP","").replace("IDR","").replace(" ","")
    negative=text.endswith("DB") or text.startswith("-") or (text.startswith("(") and text.endswith(")"))
    text=text.replace("DB","").replace("CR","").strip("()")
    if not text:return 0.0
    if "," in text and "." in text:
        if text.rfind(",")>text.rfind("."):text=text.replace(".","").replace(",",".")
        else:text=text.replace(",","")
    elif "," in text:
        parts=text.split(",")
        text="".join(parts) if len(parts[-1])==3 else ".".join(parts)
    elif "." in text:
        parts=text.split(".")
        if len(parts)>2 or (len(parts)==2 and len(parts[-1])==3):text="".join(parts)
    try:value=float(re.sub(r"[^0-9.\-]","",text) or 0)
    except Exception:value=0.0
    return -abs(value) if negative else value

def _statement_year(text):
    years=[int(x) for x in re.findall(r"\b(20\d{2})\b",text or "")]
    return years[0] if years else date.today().year

def parse_generic_statement_text(text,bank_name=None):
    """Heuristic parser for common Indonesian bank PDF statements.
    Supports rows that expose date + description + debit/credit/balance in extracted text.
    """
    bank_name=bank_name or detect_bank(text)
    year=_statement_year(text)
    items=[];opening=None
    lines=[re.sub(r"\s+"," ",x.strip()) for x in (text or "").splitlines() if x.strip()]
    for line in lines:
        up=line.upper()
        if any(k in up for k in ("SALDO AWAL","OPENING BALANCE","BALANCE B/F")):
            nums=GENERIC_MONEY_RE.findall(line)
            if nums:opening=abs(_generic_money(nums[-1]))
            continue
        dm=GENERIC_DATE_RE.search(line)
        if not dm:continue
        day=int(dm.group(1));month=int(dm.group(2));row_year=int(dm.group(3)) if dm.group(3) else year
        if row_year<100:row_year+=2000
        try:tdate=date(row_year,month,day).isoformat()
        except Exception:continue
        tail=line[dm.end():].strip()
        tokens=GENERIC_MONEY_RE.findall(tail)
        nums=[abs(_generic_money(x)) for x in tokens if abs(_generic_money(x))>0]
        if not nums:continue
        # Remove date-like fragments accidentally captured.
        desc=tail
        for tok in tokens:desc=desc.replace(tok," ",1)
        desc=re.sub(r"\b(?:DB|CR|DEBIT|KREDIT|CREDIT)\b"," ",desc,flags=re.I)
        desc=re.sub(r"\s+"," ",desc).strip(" |-")
        direction=None;amount_value=None;balance=None
        # Explicit direction markers are the safest signal.
        if re.search(r"\b(DB|DEBIT)\b",tail,re.I):
            direction="DEBIT";amount_value=nums[0];balance=nums[-1] if len(nums)>=2 else None
        elif re.search(r"\b(CR|CREDIT|KREDIT)\b",tail,re.I):
            direction="CREDIT";amount_value=nums[0];balance=nums[-1] if len(nums)>=2 else None
        elif len(nums)>=3:
            # Common columns: Debit | Credit | Balance.
            debit,credit,balance=nums[-3],nums[-2],nums[-1]
            if debit>0 and credit==0:direction="DEBIT";amount_value=debit
            elif credit>0 and debit==0:direction="CREDIT";amount_value=credit
            elif debit>0 and credit>0:
                # Some extractors omit blank cells. Infer from keywords/description.
                if any(k in up for k in ("TRANSFER MASUK","SETOR","CREDIT","KREDIT","CR ")):
                    direction="CREDIT";amount_value=credit
                else:direction="DEBIT";amount_value=debit
        elif len(nums)==2:
            # Amount + balance. Infer from transaction semantics.
            amount_value,balance=nums
            credit_words=("TRANSFER MASUK","SETORAN","SETOR ","BUNGA","CREDIT","KREDIT","REVERSAL","REFUND","QRIS MASUK")
            debit_words=("TRANSFER KELUAR","TARIK","PEMBAYARAN","BIAYA","ADMIN","DEBIT","AUTODEBET","PURCHASE","QRIS BAYAR")
            if any(k in up for k in credit_words):direction="CREDIT"
            elif any(k in up for k in debit_words):direction="DEBIT"
        if not direction or not amount_value:continue
        items.append({"transaction_date":tdate,"description":desc or "Mutasi rekening",
          "direction":direction,"debit":amount_value if direction=="DEBIT" else 0.0,
          "credit":amount_value if direction=="CREDIT" else 0.0,
          "amount":amount_value,"balance":balance})
    # Deduplicate extraction repeats from PDF headers/layers.
    unique=[];seen=set()
    for x in items:
        key=(x["transaction_date"],x["description"],round(x["amount"],2),x["direction"],round(x["balance"] or 0,2))
        if key in seen:continue
        seen.add(key);unique.append(x)
    items=unique
    if not items:
        raise ValueError("Format rekening koran belum berhasil dibaca. Gunakan PDF teks (bukan scan) atau impor CSV/Excel bank.")
    months=[int(x["transaction_date"][5:7]) for x in items]
    years=[int(x["transaction_date"][:4]) for x in items]
    return {"bank_name":bank_name,"period_year":years[0] if years else year,
      "period_month":months[0] if months else date.today().month,
      "opening_balance":opening,"row_count":len(items),
      "debit_count":sum(x["direction"]=="DEBIT" for x in items),
      "credit_count":sum(x["direction"]=="CREDIT" for x in items),
      "debit_total":sum(x["debit"] for x in items),
      "credit_total":sum(x["credit"] for x in items),"items":items}

def parse_statement_pdf(pdf_bytes):
    try:from pypdf import PdfReader
    except ImportError as exc:raise RuntimeError("Jalankan INSTALL_PDF_SUPPORT.bat.") from exc
    text="\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(pdf_bytes)).pages)
    bank=detect_bank(text)
    upper=text.upper()
    if bank=="BCA" and ("REKENING TAHAPAN" in upper or "REKENING GIRO" in upper):
        return parse_bca_statement_text(text)
    return parse_generic_statement_text(text,bank)

