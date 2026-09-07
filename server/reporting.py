import io
import json
import html
from datetime import date, timedelta
from .database import connect
from . import repository as repo

REPORT_NAMES={
 "sales_product":"Penjualan per Barang",
 "sales_service":"Penjualan per Jasa",
 "sales_customer":"Penjualan per Pelanggan",
 "sales_salesperson":"Penjualan per Salesman",
 "sales_category":"Penjualan per Kategori",
 "sales_brand":"Penjualan per Merk",
 "sales_detail":"Rincian Penjualan",
 "sales_order_history":"History Pesanan Penjualan",
 "sales_dp":"DP Penjualan",
 "sales_dp_allocation":"Alokasi DP Penjualan",
 "purchase_product":"Pembelian per Barang",
 "purchase_supplier":"Pembelian per Pemasok",
 "purchase_category":"Pembelian per Kategori",
 "purchase_brand":"Pembelian per Merk",
 "purchase_detail":"Rincian Pembelian",
 "purchase_order_history":"History Pesanan Pembelian",
 "purchase_dp":"DP Pembelian",
 "purchase_dp_allocation":"Alokasi DP Pembelian",
 "stock_list":"Daftar Stok Barang",
 "stock_fast":"Stok Fast Moving",
 "stock_dead":"Dead Stock",
 "stock_warehouse":"Qty Barang per Gudang",
 "stock_mutation":"Mutasi Barang per Gudang",
 "stock_adjustment":"Penyesuaian Barang",
 "stock_valuation_summary":"Ringkasan Valuasi Persediaan",
 "stock_valuation_detail":"Rincian Valuasi Persediaan",
 "stock_assembly":"Laporan Assembly",
 "stock_assembly_finish":"Laporan Finishing Assembly",
 "finance_journals":"All Jurnal Transaksi",
 "finance_ledger":"Buku Besar",
 "finance_trial":"Neraca Saldo",
 "finance_balance":"Neraca",
 "finance_income":"Laporan Laba Rugi",
 "finance_cashflow":"Laporan Arus Kas (Metode Langsung)",
 "finance_receivables":"Laporan Piutang Pelanggan",
 "finance_payables":"Laporan Hutang Pemasok",
 "cash_book":"Buku Kas/Bank (Mutasi Kas/Bank)",
 "cash_out":"Laporan Pengeluaran Kas/Bank",
 "cash_in":"Laporan Penerimaan Kas/Bank",
 "project_income":"Laba Rugi per Proyek",
 "project_summary":"Rekap Semua Proyek",
 "project_purchases":"Pembelian per Proyek",
 "project_materials":"Pengeluaran Material per Proyek",
 "project_cost_detail":"Rincian Biaya per Proyek",
}

def _id(v):
    try:return int(v) if v not in (None,"") else None
    except:return None

def _period(filters):
    start=str(filters.get("date_from") or "")[:10] or None
    end=str(filters.get("date_to") or "")[:10] or None
    return start,end

def _filters_sql(filters,aliases):
    clauses=[];params=[]
    mapping=[
      ("product_id",aliases.get("product")),
      ("category_id",aliases.get("category")),
      ("brand_id",aliases.get("brand")),
      ("customer_id",aliases.get("customer")),
      ("supplier_id",aliases.get("supplier")),
      ("salesperson_id",aliases.get("salesperson")),
      ("warehouse_id",aliases.get("warehouse")),
      ("inventory_account_id",aliases.get("inventory_account")),
    ]
    for key,column in mapping:
        value=_id(filters.get(key))
        if value and column:
            clauses.append(f"{column}=?");params.append(value)
    return clauses,params

def _table(title,columns,rows,summary=None):
    return {"title":title,"columns":columns,"rows":rows,"summary":summary or {}}

COST_SENSITIVE_KEYS={
    "average_cost","average_cost_before","average_cost_after","stock_value","nilai_stok","nilai_awal","nilai_akhir","nilai_masuk","nilai_keluar","hpp_keluar","hpp_jurnal_referensi","hpp_expected_referensi","selisih_hpp_referensi",
    "purchase_price","purchase_price_snapshot","unit_cost","harga_rata","harga_satuan",
    "nilai_bahan","biaya_tambahan","total_assembly","material_cost","additional_cost",
    "total_cost","allocated_cost","cost_per_unit","hpp","laba_kotor","item_hpp","item_gross_profit"
}

def redact_cost_data(data):
    if not isinstance(data,dict): return data
    out=dict(data)
    cols=out.get("columns")
    if isinstance(cols,list):
        hidden={k for k,_ in cols if k in COST_SENSITIVE_KEYS}
        out["columns"]=[c for c in cols if c[0] not in hidden]
        if isinstance(out.get("rows"),list):
            out["rows"]=[{k:v for k,v in r.items() if k not in hidden} if isinstance(r,dict) else r for r in out["rows"]]
    if isinstance(out.get("available_columns"),list):
        out["available_columns"]=[c for c in out["available_columns"] if c[0] not in COST_SENSITIVE_KEYS]
    if isinstance(out.get("summary"),dict):
        out["summary"]={k:v for k,v in out["summary"].items() if k not in COST_SENSITIVE_KEYS and not k.startswith("total_hpp") and not k.startswith("total_laba_kotor")}
    if isinstance(out.get("projects"),list):
        out["projects"]=[redact_cost_data(x) if isinstance(x,dict) else x for x in out["projects"]]
    return out

def _sales_report(kind,filters):
    group_map={
      "sales_product":("p.id","p.sku kode,p.name nama","Barang"),
      "sales_service":("p.id","COALESCE(sv.service_code,p.sku) kode,p.name nama","Jasa"),
      "sales_customer":("COALESCE(bp.id,0)","COALESCE(bp.code,'UMUM') kode,COALESCE(bp.name,'Pelanggan Umum') nama","Pelanggan"),
      "sales_salesperson":("COALESCE(sp.id,0)","COALESCE(sp.code,'-') kode,COALESCE(sp.name,'Tanpa Salesman') nama","Salesman"),
      "sales_category":("COALESCE(c.id,0)","COALESCE(c.code,'-') kode,COALESCE(c.name,'Tanpa Kategori') nama","Kategori"),
      "sales_brand":("COALESCE(b.id,0)","COALESCE(b.code,'-') kode,COALESCE(b.name,'Tanpa Merk') nama","Merk"),
    }
    group,select_group,label=group_map[kind]
    start,end=_period(filters)
    where=["s.status='POSTED'"];params=[]
    if kind=="sales_product":where.append("p.product_type='STOCK'")
    if kind=="sales_service":where.append("p.product_type='SERVICE'")
    if start:where.append("s.sale_date>=?");params.append(start)
    if end:where.append("s.sale_date<=?");params.append(end)
    extra,p2=_filters_sql(filters,{
      "product":"p.id","category":"p.category_id","brand":"p.brand_id",
      "customer":"s.customer_id","salesperson":"s.salesperson_id"})
    where+=extra;params+=p2
    sql=f"""SELECT {select_group},
      COUNT(DISTINCT s.id) transaksi,SUM(si.qty) qty,
      SUM(si.line_total) penjualan,
      SUM(CASE WHEN s.salesperson_id IS NOT NULL AND COALESCE(sp.commission_percent,0)>0
        THEN (CASE WHEN CAST(s.subtotal AS REAL)>0
          THEN (CAST(si.line_total AS REAL)/CAST(s.subtotal AS REAL))*MAX(0,CAST(s.subtotal AS REAL)-CAST(COALESCE(s.discount_amount,0) AS REAL))*CAST(sp.commission_percent AS REAL)/100.0
          ELSE 0 END) ELSE 0 END) nilai_komisi,
      SUM((CASE WHEN COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)>0 THEN (COALESCE((SELECT SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL))
      FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
      JOIN chart_of_accounts ja ON ja.id=jl.account_id
      WHERE je.status='POSTED' AND je.source_type='SALE' AND je.source_id=s.id
        AND ja.account_subtype='HPP'),0))*((CAST(si.qty AS REAL)*(CASE WHEN p.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it.quantity_change AS REAL))*CAST(it.unit_cost AS REAL))/SUM(ABS(CAST(it.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it
        WHERE it.reference_type='SALE' AND it.reference_no=s.invoice_no AND it.product_id=si.product_id
      ),CAST(si.purchase_price_snapshot AS REAL),0) ELSE 0 END)))/(COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)) ELSE 0 END)) hpp,
      SUM(CAST(si.line_total AS REAL)-((CASE WHEN COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)>0 THEN (COALESCE((SELECT SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL))
      FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
      JOIN chart_of_accounts ja ON ja.id=jl.account_id
      WHERE je.status='POSTED' AND je.source_type='SALE' AND je.source_id=s.id
        AND ja.account_subtype='HPP'),0))*((CAST(si.qty AS REAL)*(CASE WHEN p.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it.quantity_change AS REAL))*CAST(it.unit_cost AS REAL))/SUM(ABS(CAST(it.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it
        WHERE it.reference_type='SALE' AND it.reference_no=s.invoice_no AND it.product_id=si.product_id
      ),CAST(si.purchase_price_snapshot AS REAL),0) ELSE 0 END)))/(COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)) ELSE 0 END))) laba_kotor
      FROM sales_items si JOIN sales s ON s.id=si.sale_id
      JOIN products p ON p.id=si.product_id
      LEFT JOIN business_partners bp ON bp.id=s.customer_id
      LEFT JOIN salespersons sp ON sp.id=s.salesperson_id
      LEFT JOIN item_categories c ON c.id=p.category_id
      LEFT JOIN brands b ON b.id=p.brand_id
      LEFT JOIN services sv ON sv.product_id=p.id
      WHERE {' AND '.join(where)}
      GROUP BY {group} ORDER BY penjualan DESC"""
    c=connect()
    try: rows=[dict(x) for x in c.execute(sql,params)]
    finally:c.close()
    for r in rows:
        for k in ("qty","penjualan","nilai_komisi","hpp","laba_kotor"):r[k]=float(r[k] or 0)
    return _table(REPORT_NAMES[kind],
      [("kode","Kode"),("nama",label),("transaksi","Transaksi"),("qty","Qty"),
       ("penjualan","Penjualan")]+([("nilai_komisi","Nilai Komisi")] if kind=="sales_salesperson" else [])+[("hpp","HPP"),("laba_kotor","Laba Kotor")],rows,
      {"total_penjualan":sum(r["penjualan"] for r in rows),
       **({"total_komisi":sum(r["nilai_komisi"] for r in rows)} if kind=="sales_salesperson" else {}),
       "total_hpp":sum(r["hpp"] for r in rows),
       "total_laba_kotor":sum(r["laba_kotor"] for r in rows)})

def _purchase_report(kind,filters):
    group_map={
      "purchase_product":("pr.id","pr.sku kode,pr.name nama","Barang"),
      "purchase_supplier":("bp.id","bp.code kode,bp.name nama","Pemasok"),
      "purchase_category":("COALESCE(c.id,0)","COALESCE(c.code,'-') kode,COALESCE(c.name,'Tanpa Kategori') nama","Kategori"),
      "purchase_brand":("COALESCE(b.id,0)","COALESCE(b.code,'-') kode,COALESCE(b.name,'Tanpa Merk') nama","Merk"),
    }
    group,select_group,label=group_map[kind]
    start,end=_period(filters)
    where=["p.status='POSTED'"];params=[]
    if start:where.append("p.purchase_date>=?");params.append(start)
    if end:where.append("p.purchase_date<=?");params.append(end)
    extra,p2=_filters_sql(filters,{
      "product":"pr.id","category":"pr.category_id","brand":"pr.brand_id",
      "supplier":"p.supplier_id"})
    where+=extra;params+=p2
    sql=f"""SELECT {select_group},COUNT(DISTINCT p.id) transaksi,
      SUM(pi.qty) qty,SUM(pi.line_total) pembelian,
      CASE WHEN SUM(pi.qty)=0 THEN 0 ELSE SUM(pi.line_total)/SUM(pi.qty) END harga_rata
      FROM purchase_items pi JOIN purchases p ON p.id=pi.purchase_id
      JOIN products pr ON pr.id=pi.product_id
      JOIN business_partners bp ON bp.id=p.supplier_id
      LEFT JOIN item_categories c ON c.id=pr.category_id
      LEFT JOIN brands b ON b.id=pr.brand_id
      WHERE {' AND '.join(where)}
      GROUP BY {group} ORDER BY pembelian DESC"""
    c=connect()
    try:rows=[dict(x) for x in c.execute(sql,params)]
    finally:c.close()
    for r in rows:
        for k in ("qty","pembelian","harga_rata"):r[k]=float(r[k] or 0)
    return _table(REPORT_NAMES[kind],
      [("kode","Kode"),("nama",label),("transaksi","Transaksi"),("qty","Qty"),
       ("harga_rata","Harga Rata-rata"),("pembelian","Pembelian")],rows,
      {"total_pembelian":sum(r["pembelian"] for r in rows)})


def _inventory_effective_date_expr(alias="it"):
    return f"""CASE
      WHEN {alias}.reference_type='OPENING' THEN COALESCE(
        (SELECT p2.opening_balance_date FROM products p2 WHERE p2.id={alias}.product_id),
        substr({alias}.created_at,1,10))
      WHEN {alias}.reference_type='PURCHASE' THEN COALESCE(
        (SELECT p2.purchase_date FROM purchases p2 WHERE p2.purchase_no={alias}.reference_no LIMIT 1),
        substr({alias}.created_at,1,10))
      WHEN {alias}.reference_type='SALE' THEN COALESCE(
        (SELECT s2.sale_date FROM sales s2 WHERE s2.invoice_no={alias}.reference_no LIMIT 1),
        substr({alias}.created_at,1,10))
      WHEN {alias}.reference_type IN ('PURCHASE_RETURN','PURCHASE_RETURN_VOID') THEN COALESCE(
        (SELECT r2.return_date FROM purchase_returns r2 WHERE r2.return_no={alias}.reference_no LIMIT 1),
        substr({alias}.created_at,1,10))
      WHEN {alias}.reference_type IN ('SALES_RETURN','SALES_RETURN_VOID') THEN COALESCE(
        (SELECT r3.return_date FROM sales_returns r3 WHERE r3.return_no={alias}.reference_no LIMIT 1),
        substr({alias}.created_at,1,10))
      WHEN {alias}.reference_type='PROJECT_MATERIAL_ISSUE' THEN COALESCE(
        (SELECT pm.issue_date FROM project_material_issues pm WHERE pm.issue_no={alias}.reference_no LIMIT 1),
        substr({alias}.created_at,1,10))
      ELSE substr({alias}.created_at,1,10)
    END"""

def _inventory_valuation_detail(filters):
    start,end=_period(filters)
    effective_date=_inventory_effective_date_expr("it")
    where=["p.product_type='STOCK'"];params=[]
    if start:where.append(f"({effective_date})>=?");params.append(start)
    if end:where.append(f"({effective_date})<=?");params.append(end)
    extra,p2=_filters_sql(filters,{"product":"p.id","category":"p.category_id","brand":"p.brand_id",
      "inventory_account":"p.inventory_account_id","warehouse":"w.id"})
    where+=extra;params+=p2
    c=connect()
    try:
        raw=[dict(x) for x in c.execute(f"""SELECT it.id,it.created_at,{effective_date} tanggal,
          w.code kode_gudang,w.name gudang,p.id product_id,p.sku kode,p.name barang,
          it.movement_type jenis,it.reference_type tipe_referensi,it.reference_no referensi,it.reason keterangan,
          CAST(it.quantity_change AS REAL) perubahan,CAST(it.quantity_before AS REAL) qty_awal,
          CAST(it.quantity_after AS REAL) qty_akhir,CAST(it.unit_cost AS REAL) unit_cost,
          CAST(it.average_cost_before AS REAL) average_cost_before,CAST(it.average_cost_after AS REAL) average_cost_after,CAST(it.value_change AS REAL) value_change,CAST(it.value_before AS REAL) value_before,CAST(it.value_after AS REAL) value_after,
          ia.code||' - '||ia.name akun_persediaan,
          ha.code||' - '||ha.name akun_hpp,
          p.cogs_account_id
          FROM inventory_transactions it JOIN products p ON p.id=it.product_id
          JOIN warehouses w ON w.id=it.warehouse_id
          LEFT JOIN chart_of_accounts ia ON ia.id=p.inventory_account_id
          LEFT JOIN chart_of_accounts ha ON ha.id=p.cogs_account_id
          WHERE {' AND '.join(where)}
          ORDER BY it.created_at,it.id""",params).fetchall()]

        # Journal HPP and expected inventory HPP are reconciled at transaction reference/invoice level.
        refs=sorted({str(x.get("referensi") or "") for x in raw if str(x.get("tipe_referensi") or "").upper()=="SALE" and x.get("referensi")})
        hpp_by_ref={};expected_by_ref={}
        for ref in refs:
            row=c.execute("""SELECT COALESCE(SUM(jl.debit-jl.credit),0) v
              FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
              JOIN chart_of_accounts a ON a.id=jl.account_id
              WHERE je.status='POSTED' AND je.reference_no=? AND a.account_subtype='HPP'""",(ref,)).fetchone()
            hpp_by_ref[ref]=float(row["v"] or 0)
            row=c.execute("""SELECT COALESCE(SUM(ABS(quantity_change)*unit_cost),0) v
              FROM inventory_transactions WHERE reference_type='SALE' AND reference_no=?""",(ref,)).fetchone()
            expected_by_ref[ref]=float(row["v"] or 0)

        rows=[]
        for x in raw:
            ch=float(x["perubahan"] or 0);uc=float(x["unit_cost"] or 0)
            x["qty_masuk"]=ch if ch>0 else 0.0
            x["qty_keluar"]=abs(ch) if ch<0 else 0.0
            movement_value=round(float(x.get("value_change") or ch*uc),2)
            x["nilai_masuk"]=movement_value if ch>0 else 0.0
            x["nilai_keluar"]=abs(movement_value) if ch<0 else 0.0
            x["nilai_awal"]=round(float(x.get("value_before") or 0),2)
            x["nilai_akhir"]=round(float(x.get("value_after") or 0),2)
            is_sale=str(x.get("tipe_referensi") or "").upper()=="SALE"
            x["hpp_keluar"]=x["nilai_keluar"] if is_sale else 0.0
            ref=str(x.get("referensi") or "")
            x["hpp_expected_referensi"]=round(expected_by_ref.get(ref,0.0),2) if is_sale else 0.0
            x["hpp_jurnal_referensi"]=round(hpp_by_ref.get(ref,0.0),2) if is_sale else 0.0
            x["selisih_hpp_referensi"]=round(x["hpp_expected_referensi"]-x["hpp_jurnal_referensi"],2) if is_sale else 0.0
            x["status_rekonsiliasi"]="SESUAI" if (not is_sale or abs(x["selisih_hpp_referensi"])<0.01) else "SELISIH"
            rows.append(x)

        total_masuk=sum(x["nilai_masuk"] for x in rows)
        total_keluar=sum(x["nilai_keluar"] for x in rows)
        # Unique reference totals, not repeated per row.
        total_hpp_expected=sum(expected_by_ref.values())
        total_hpp_jurnal=sum(hpp_by_ref.values())
        summary={"jumlah_mutasi":len(rows),"total_nilai_masuk":round(total_masuk,2),"total_nilai_keluar":round(total_keluar,2),
          "total_hpp_keluar":round(total_hpp_expected,2),"total_hpp_jurnal":round(total_hpp_jurnal,2),
          "selisih_hpp":round(total_hpp_expected-total_hpp_jurnal,2),
          "status_hpp":"SESUAI" if abs(total_hpp_expected-total_hpp_jurnal)<0.01 else "ADA SELISIH"}
    finally:c.close()
    cols=[("tanggal","Tanggal"),("kode_gudang","Kode Gudang"),("gudang","Gudang"),("kode","SKU"),("barang","Barang"),
      ("jenis","Jenis Mutasi"),("tipe_referensi","Tipe Referensi"),("referensi","Referensi"),("keterangan","Keterangan"),
      ("qty_masuk","Qty Masuk"),("qty_keluar","Qty Keluar"),("unit_cost","Unit Cost"),
      ("nilai_masuk","Nilai Masuk"),("nilai_keluar","Nilai Keluar"),
      ("qty_awal","Qty Awal"),("nilai_awal","Nilai Awal"),("qty_akhir","Qty Akhir"),("nilai_akhir","Nilai Akhir"),
      ("akun_persediaan","Akun Persediaan"),("akun_hpp","Akun HPP"),
      ("hpp_keluar","HPP Keluar Baris"),("hpp_expected_referensi","HPP Expected Referensi"),
      ("hpp_jurnal_referensi","HPP Jurnal Referensi"),("selisih_hpp_referensi","Selisih HPP Referensi"),
      ("status_rekonsiliasi","Status Rekonsiliasi")]
    return _table(REPORT_NAMES["stock_valuation_detail"],cols,rows,summary)

def _inventory_valuation_summary(filters):
    start,end=_period(filters)
    c=connect()
    try:
        where=["p.product_type='STOCK'","p.is_active=1"];params=[]
        extra,p2=_filters_sql(filters,{"product":"p.id","category":"p.category_id","brand":"p.brand_id",
          "inventory_account":"p.inventory_account_id","warehouse":"w.id"})
        where+=extra;params+=p2
        pairs=[dict(x) for x in c.execute(f"""SELECT p.id product_id,p.sku kode,p.name barang,w.id warehouse_id,
          w.code kode_gudang,w.name gudang,p.inventory_account_id,
          ia.code||' - '||ia.name akun_persediaan,ha.code||' - '||ha.name akun_hpp
          FROM products p CROSS JOIN warehouses w
          LEFT JOIN chart_of_accounts ia ON ia.id=p.inventory_account_id
          LEFT JOIN chart_of_accounts ha ON ha.id=p.cogs_account_id
          WHERE {' AND '.join(where)}
          ORDER BY p.sku COLLATE NOCASE,w.code COLLATE NOCASE""",params).fetchall()]
        rows=[]
        date_expr=_inventory_effective_date_expr("it")
        for x in pairs:
            pid=x["product_id"];wid=x["warehouse_id"]
            # Saldo awal/akhir VALUASI berasal dari penjumlahan nilai mutasi:
            # qty_change × unit_cost. Ini sumber yang sama dengan jurnal persediaan/HPP.
            pre_where=["it.product_id=?","it.warehouse_id=?"];pre=[pid,wid]
            if start:pre_where.append(f"({date_expr})<?");pre.append(start)
            else:pre_where.append("1=0")
            opening=c.execute(f"""SELECT
              COALESCE(SUM(it.quantity_change),0) qty,
              COALESCE(SUM(COALESCE(it.value_change,it.quantity_change*it.unit_cost)),0) nilai
              FROM inventory_transactions it WHERE {' AND '.join(pre_where)}""",pre).fetchone()
            per_where=["it.product_id=?","it.warehouse_id=?"];pp=[pid,wid]
            if start:per_where.append(f"({date_expr})>=?");pp.append(start)
            if end:per_where.append(f"({date_expr})<=?");pp.append(end)
            agg=c.execute(f"""SELECT
              COALESCE(SUM(CASE WHEN it.quantity_change>0 THEN it.quantity_change ELSE 0 END),0) qty_masuk,
              COALESCE(SUM(CASE WHEN it.quantity_change>0 THEN COALESCE(it.value_change,it.quantity_change*it.unit_cost) ELSE 0 END),0) nilai_masuk,
              COALESCE(SUM(CASE WHEN it.quantity_change<0 THEN -it.quantity_change ELSE 0 END),0) qty_keluar,
              COALESCE(SUM(CASE WHEN it.quantity_change<0 THEN -COALESCE(it.value_change,it.quantity_change*it.unit_cost) ELSE 0 END),0) nilai_keluar,
              COUNT(*) jumlah_mutasi FROM inventory_transactions it WHERE {' AND '.join(per_where)}""",pp).fetchone()
            end_where=["it.product_id=?","it.warehouse_id=?"];ep=[pid,wid]
            if end:end_where.append(f"({date_expr})<=?");ep.append(end)
            ending=c.execute(f"""SELECT
              COALESCE(SUM(it.quantity_change),0) qty,
              COALESCE(SUM(COALESCE(it.value_change,it.quantity_change*it.unit_cost)),0) nilai
              FROM inventory_transactions it WHERE {' AND '.join(end_where)}""",ep).fetchone()
            oq=float(opening["qty"] or 0);ov=float(opening["nilai"] or 0)
            eq=float(ending["qty"] or 0);ev=float(ending["nilai"] or 0)
            if not agg["jumlah_mutasi"] and abs(oq)<1e-12 and abs(eq)<1e-12:continue
            oa=(ov/oq) if abs(oq)>1e-12 else 0.0
            ea=(ev/eq) if abs(eq)>1e-12 else 0.0
            x.update({"qty_awal":oq,"harga_rata_awal":round(oa,2),"nilai_awal":round(ov,2),
              "qty_masuk":float(agg["qty_masuk"] or 0),"nilai_masuk":round(float(agg["nilai_masuk"] or 0),2),
              "qty_keluar":float(agg["qty_keluar"] or 0),"nilai_keluar":round(float(agg["nilai_keluar"] or 0),2),
              "qty_akhir":eq,"harga_rata_akhir":round(ea,2),"nilai_akhir":round(ev,2),
              "jumlah_mutasi":int(agg["jumlah_mutasi"] or 0)})
            rows.append(x)

        nilai_awal=round(sum(x["nilai_awal"] for x in rows),2)
        nilai_masuk=round(sum(x["nilai_masuk"] for x in rows),2)
        nilai_keluar=round(sum(x["nilai_keluar"] for x in rows),2)
        nilai_akhir=round(sum(x["nilai_akhir"] for x in rows),2)

        # Untuk laporan total tanpa filter dimensional gudang/barang, tampilkan pembanding GL.
        dimension_filtered=any(filters.get(k) not in (None,"","0",0) for k in ("warehouse_id","warehouse","product_id","product","category_id","category","brand_id","brand"))
        gl_value=None;gl_diff=None
        if not dimension_filtered:
            account_ids=sorted({int(x["inventory_account_id"]) for x in rows if x.get("inventory_account_id")})
            if account_ids:
                qs=",".join("?" for _ in account_ids)
                jp=list(account_ids)
                date_clause=""
                if end:
                    date_clause=" AND je.journal_date<=?"
                    jp.append(end)
                glrow=c.execute(f"""SELECT COALESCE(SUM(jl.debit-jl.credit),0) v
                  FROM journal_lines jl JOIN journal_entries je ON je.id=jl.journal_id
                  WHERE je.status='POSTED' AND jl.account_id IN ({qs}) {date_clause}""",jp).fetchone()
                gl_value=round(float(glrow["v"] or 0),2)
                gl_diff=round(nilai_akhir-gl_value,2)

        summary={"jumlah_item_gudang":len(rows),"nilai_awal":nilai_awal,
          "nilai_masuk":nilai_masuk,"nilai_keluar":nilai_keluar,"nilai_akhir":nilai_akhir}
        if gl_value is not None:
            summary["persediaan_buku_besar"]=gl_value
            summary["selisih_dengan_buku_besar"]=gl_diff
            summary["status_rekonsiliasi"]="SESUAI" if abs(gl_diff)<0.01 else "SELISIH"
    finally:c.close()
    cols=[("kode","SKU"),("barang","Barang"),("kode_gudang","Kode Gudang"),("gudang","Gudang"),
      ("qty_awal","Qty Awal"),("harga_rata_awal","Avg Cost Awal"),("nilai_awal","Nilai Awal"),
      ("qty_masuk","Qty Masuk"),("nilai_masuk","Nilai Masuk"),("qty_keluar","Qty Keluar"),("nilai_keluar","Nilai Keluar"),
      ("qty_akhir","Qty Akhir"),("harga_rata_akhir","Avg Cost Akhir"),("nilai_akhir","Nilai Akhir"),
      ("jumlah_mutasi","Jumlah Mutasi"),("akun_persediaan","Akun Persediaan"),("akun_hpp","Akun HPP")]
    return _table(REPORT_NAMES["stock_valuation_summary"],cols,rows,summary)

def _stock_report(kind,filters):
    start,end=_period(filters)
    c=connect()
    try:
      if kind=="stock_valuation_summary":
        return _inventory_valuation_summary(filters)
      if kind=="stock_valuation_detail":
        return _inventory_valuation_detail(filters)
      if kind=="stock_list":
        where=["p.is_active=1","p.product_type='STOCK'"];params=[]
        extra,p2=_filters_sql(filters,{"category":"p.category_id","brand":"p.brand_id","inventory_account":"p.inventory_account_id"})
        where+=extra;params+=p2
        sql=f"""SELECT p.sku kode,p.name barang,COALESCE(ca.name,'-') kategori,
          COALESCE(br.name,'-') merk,COALESCE(SUM(ib.quantity),0) qty,
          COALESCE(SUM(ib.quantity*ib.average_cost),0) nilai_stok,
          coa.code||' - '||coa.name akun_persediaan
          FROM products p LEFT JOIN inventory_balances ib ON ib.product_id=p.id
          LEFT JOIN item_categories ca ON ca.id=p.category_id LEFT JOIN brands br ON br.id=p.brand_id
          LEFT JOIN chart_of_accounts coa ON coa.id=p.inventory_account_id
          WHERE {' AND '.join(where)} GROUP BY p.id,ca.name,br.name,coa.code,coa.name ORDER BY p.sku COLLATE NOCASE,p.name COLLATE NOCASE"""
        rows=[dict(x) for x in c.execute(sql,params)]
        cols=[("kode","SKU"),("barang","Barang"),("kategori","Kategori"),("merk","Merk"),
              ("qty","Qty Realtime"),("nilai_stok","Nilai Stok"),("akun_persediaan","Akun Persediaan")]
      elif kind in ("stock_fast","stock_dead"):
        cutoff=(date.today()-timedelta(days=90)).isoformat()
        where=["p.is_active=1","p.product_type='STOCK'"];params=[]
        extra,p2=_filters_sql(filters,{"category":"p.category_id","brand":"p.brand_id","inventory_account":"p.inventory_account_id"})
        where+=extra;params+=p2
        sql=f"""SELECT p.sku kode,p.name barang,COALESCE(c.name,'-') kategori,
          COALESCE(b.name,'-') merk,COALESCE(SUM(ib.quantity),0) qty_stok,
          COALESCE(SUM(CASE WHEN it.quantity_change<0 AND substr(it.created_at,1,10)>=?
            THEN -it.quantity_change ELSE 0 END),0) qty_keluar_90_hari,
          MAX(CASE WHEN it.quantity_change<0 THEN substr(it.created_at,1,10) END) terakhir_keluar
          FROM products p LEFT JOIN inventory_balances ib ON ib.product_id=p.id
          LEFT JOIN inventory_transactions it ON it.product_id=p.id
          LEFT JOIN item_categories c ON c.id=p.category_id LEFT JOIN brands b ON b.id=p.brand_id
          WHERE {' AND '.join(where)} GROUP BY p.id,c.name,b.name"""
        params=[cutoff]+params
        if kind=="stock_fast":sql+=" HAVING COALESCE(SUM(CASE WHEN it.quantity_change<0 AND substr(it.created_at,1,10)>=? THEN -it.quantity_change ELSE 0 END),0)>0 ORDER BY qty_keluar_90_hari DESC";params.append(cutoff)
        else:sql+=" HAVING COALESCE(SUM(ib.quantity),0)>0 AND (MAX(CASE WHEN it.quantity_change<0 THEN substr(it.created_at,1,10) END) IS NULL OR MAX(CASE WHEN it.quantity_change<0 THEN substr(it.created_at,1,10) END)<?) ORDER BY qty_stok DESC";params.append(cutoff)
        rows=[dict(x) for x in c.execute(sql,params)]
        cols=[("kode","SKU"),("barang","Barang"),("kategori","Kategori"),("merk","Merk"),
              ("qty_stok","Qty Stok"),("qty_keluar_90_hari","Qty Keluar 90 Hari"),("terakhir_keluar","Terakhir Keluar")]
      elif kind=="stock_warehouse":
        where=["p.is_active=1","p.product_type='STOCK'"];params=[]
        extra,p2=_filters_sql(filters,{"category":"p.category_id","brand":"p.brand_id","inventory_account":"p.inventory_account_id","warehouse":"w.id"})
        where+=extra;params+=p2
        sql=f"""SELECT w.code kode_gudang,w.name gudang,p.sku kode_barang,p.name barang,
          COALESCE(c.name,'-') kategori,COALESCE(b.name,'-') merk,
          COALESCE(ib.quantity,0) qty,COALESCE(ib.average_cost,0) harga_rata,
          COALESCE(ib.quantity*ib.average_cost,0) nilai_stok
          FROM warehouses w CROSS JOIN products p
          LEFT JOIN inventory_balances ib ON ib.warehouse_id=w.id AND ib.product_id=p.id
          LEFT JOIN item_categories c ON c.id=p.category_id LEFT JOIN brands b ON b.id=p.brand_id
          WHERE {' AND '.join(where)} ORDER BY w.code COLLATE NOCASE,p.sku COLLATE NOCASE"""
        rows=[dict(x) for x in c.execute(sql,params)]
        cols=[("kode_gudang","Kode Gudang"),("gudang","Gudang"),("kode_barang","SKU"),("barang","Barang"),
              ("kategori","Kategori"),("merk","Merk"),("qty","Qty"),("harga_rata","Harga Rata"),("nilai_stok","Nilai")]
      elif kind in ("stock_assembly","stock_assembly_finish"):
        where=["a.status<>'VOID'"];params=[]
        if start: where.append("a.assembly_date>=?");params.append(start)
        if end: where.append("a.assembly_date<=?");params.append(end)
        if kind=="stock_assembly":
          sql=f"""SELECT a.assembly_date tanggal,a.assembly_no nomor,w.name gudang,
            p.sku kode_barang,p.name bahan,SUM(CAST(m.qty AS REAL)) qty,
            CASE WHEN SUM(CAST(m.qty AS REAL))=0 THEN 0 ELSE SUM(CAST(m.total_cost AS REAL))/SUM(CAST(m.qty AS REAL)) END harga_satuan,
            SUM(CAST(m.total_cost AS REAL)) nilai_bahan,
            a.additional_cost biaya_tambahan,a.total_cost total_assembly,a.status,a.notes catatan
            FROM assembly_orders a JOIN warehouses w ON w.id=a.warehouse_id
            JOIN assembly_materials m ON m.assembly_id=a.id JOIN products p ON p.id=m.product_id
            WHERE {' AND '.join(where)}
            GROUP BY a.id,p.id,p.sku,p.name,a.assembly_date,a.assembly_no,w.name,a.additional_cost,a.total_cost,a.status,a.notes
            ORDER BY a.assembly_date DESC,a.id DESC,p.name"""
          rows=[dict(x) for x in c.execute(sql,params)]
          cols=[("tanggal","Tanggal"),("nomor","Nomor Assembly"),("gudang","Gudang"),("kode_barang","SKU"),("bahan","Bahan Baku"),("qty","Qty"),("harga_satuan","Harga Satuan"),("nilai_bahan","Nilai Bahan"),("biaya_tambahan","Biaya Tambahan"),("total_assembly","Total Cost"),("status","Status"),("catatan","Catatan")]
        else:
          where.append("a.status='FINISHED'")
          sql=f"""SELECT a.finished_at tanggal,a.assembly_no nomor,w.name gudang,
            p.sku kode_barang,p.name barang_jadi,o.qty,o.allocation_percent persen_cost,
            o.allocated_cost nilai_cost,o.unit_cost cost_per_unit,a.total_cost total_assembly
            FROM assembly_orders a JOIN warehouses w ON w.id=a.warehouse_id
            JOIN assembly_outputs o ON o.assembly_id=a.id JOIN products p ON p.id=o.product_id
            WHERE {' AND '.join(where)} ORDER BY a.finished_at DESC,a.id DESC,o.id"""
          rows=[dict(x) for x in c.execute(sql,params)]
          cols=[("tanggal","Tanggal Finishing"),("nomor","Nomor Assembly"),("gudang","Gudang"),("kode_barang","SKU"),("barang_jadi","Barang Jadi"),("qty","Qty"),("persen_cost","% Cost"),("nilai_cost","Cost Dialokasikan"),("cost_per_unit","Cost per Unit"),("total_assembly","Total Cost Assembly")]
      elif kind in ("stock_mutation","stock_adjustment"):
        where=["NOT EXISTS(SELECT 1 FROM transaction_voids v WHERE v.transaction_key=CAST(ct.id AS TEXT) AND v.transaction_kind IN ('cash','cash_reversal'))"];params=[]
        if kind=="stock_adjustment":where.append("it.reference_type='ADJUSTMENT'")
        if start:where.append("substr(it.created_at,1,10)>=?");params.append(start)
        if end:where.append("substr(it.created_at,1,10)<=?");params.append(end)
        extra,p2=_filters_sql(filters,{"product":"p.id","category":"p.category_id","brand":"p.brand_id","inventory_account":"p.inventory_account_id","warehouse":"w.id"})
        where+=extra;params+=p2
        sql=f"""SELECT substr(it.created_at,1,10) tanggal,w.name gudang,p.sku kode,
          p.name barang,it.movement_type jenis,it.quantity_change perubahan,
          it.quantity_before qty_awal,it.quantity_after qty_akhir,it.unit_cost harga,
          it.reference_no referensi,it.reason keterangan
          FROM inventory_transactions it JOIN products p ON p.id=it.product_id
          JOIN warehouses w ON w.id=it.warehouse_id
          WHERE {' AND '.join(where)} ORDER BY it.created_at DESC,it.id DESC"""
        rows=[dict(x) for x in c.execute(sql,params)]
        cols=[("tanggal","Tanggal"),("gudang","Gudang"),("kode","SKU"),("barang","Barang"),
              ("jenis","Jenis"),("perubahan","Perubahan"),("qty_awal","Qty Awal"),("qty_akhir","Qty Akhir"),
              ("harga","Harga"),("referensi","Referensi"),("keterangan","Keterangan")]
      else:raise ValueError("Jenis laporan stok tidak valid.")
    finally:c.close()
    for row in rows:
        for k,v in list(row.items()):
            if isinstance(v,(int,float)) and k!="id":row[k]=float(v)
    return _table(REPORT_NAMES[kind],cols,rows,{"jumlah_baris":len(rows)})

def _balance_group(account):
    subtype=str(account.get("account_subtype") or "").upper()
    code=str(account.get("code") or "")
    account_type=str(account.get("account_type") or "").upper()
    if account_type=="ASSET":
        if subtype in ("FIXED_ASSET","ACCUM_DEPRECIATION") or code.startswith("14"):
            return "Aset Tidak Lancar"
        if subtype in ("CASH_BANK","RECEIVABLE","ASSET"):
            return "Aset Lancar"
        return "Aset Tidak Lancar"
    if account_type=="LIABILITY":
        if subtype in ("PAYABLE","LIABILITY") or code.startswith("2"):
            return "Kewajiban Jangka Pendek"
        return "Kewajiban Jangka Panjang"
    return "Ekuitas"

def _balance_sheet(filters):
    start,end=_period(filters)
    tb=repo.trial_balance(start,end)
    c=connect()
    try:
        accounts={r["code"]:dict(r) for r in c.execute("""SELECT a.id,a.code,a.name,
          a.account_type,a.account_subtype,a.parent_id,p.code parent_code,p.name parent_name
          FROM chart_of_accounts a LEFT JOIN chart_of_accounts p ON p.id=a.parent_id""")}
    finally:c.close()
    rows=[]
    total_aset=total_kewajiban=total_ekuitas=0.0
    laba_rugi_tahun_ini=0.0
    for item in tb["items"]:
        account=accounts.get(item["code"],{})
        typ=str(account.get("account_type") or "").upper()
        raw=float(item["ending_debit"] or 0)-float(item["ending_credit"] or 0)

        # Akun nominal tidak ditampilkan satu per satu di Neraca. Saldo bersih
        # pendapatan dan beban disajikan sebagai Laba (Rugi) Tahun Ini pada ekuitas.
        if typ in ("REVENUE","EXPENSE"):
            laba_rugi_tahun_ini-=raw
            continue
        if typ not in ("ASSET","LIABILITY","EQUITY"):
            continue

        saldo=raw if typ=="ASSET" else -raw
        if abs(saldo)<0.005:continue
        sisi="ASET" if typ=="ASSET" else "KEWAJIBAN & EKUITAS"
        kelompok=_balance_group(account)
        induk=account.get("parent_name") or kelompok
        rows.append({"sisi":sisi,"kelompok":kelompok,"induk":induk,
          "kode":item["code"],"akun":item["name"],"saldo":round(saldo,2)})
        if typ=="ASSET":total_aset+=saldo
        elif typ=="LIABILITY":total_kewajiban+=saldo
        elif typ=="EQUITY":total_ekuitas+=saldo

    if abs(laba_rugi_tahun_ini)>=0.005:
        rows.append({"sisi":"KEWAJIBAN & EKUITAS","kelompok":"Ekuitas",
          "induk":"Ekuitas","kode":"3999","akun":"Laba (Rugi) Tahun Ini",
          "saldo":round(laba_rugi_tahun_ini,2)})
        total_ekuitas+=laba_rugi_tahun_ini

    group_order={"Aset Lancar":10,"Aset Tidak Lancar":20,"Kewajiban Jangka Pendek":30,"Kewajiban Jangka Panjang":40,"Ekuitas":50}
    rows.sort(key=lambda x:(0 if x["sisi"]=="ASET" else 1,group_order.get(x["kelompok"],99),x["induk"],x["kode"]))
    difference=total_aset-total_kewajiban-total_ekuitas
    return _table(REPORT_NAMES["finance_balance"],
      [("sisi","Sisi"),("kelompok","Kelompok"),("induk","Induk Akun"),
       ("kode","Kode"),("akun","Akun"),("saldo","Saldo")],rows,
      {"total_aset":round(total_aset,2),"total_kewajiban":round(total_kewajiban,2),
       "total_ekuitas":round(total_ekuitas,2),
       "total_kewajiban_ekuitas":round(total_kewajiban+total_ekuitas,2),
       "selisih_neraca":round(difference,2),"balance":abs(difference)<0.01})

def _finance_report(kind,filters):
    start,end=_period(filters)
    if kind=="finance_ledger":
        aid=_id(filters.get("account_id"))
        columns=[("kode_akun","Kode Akun"),("nama_akun","Nama Akun"),
          ("tanggal","Tanggal"),("nomor","No. Bukti"),("keterangan","Keterangan"),
          ("partner","Pelanggan / Pemasok"),("referensi","Referensi"),
          ("debit","Debit"),("kredit","Kredit"),("saldo","Saldo")]
        if aid:
            ledgers=[repo.general_ledger(aid,start,end,filters.get("partner_id"))]
        else:
            # Mode Semua Akun: partner tidak diterapkan karena setiap akun dapat memiliki tipe partner berbeda.
            c=connect()
            try:
                account_ids=[r["id"] for r in c.execute(
                  "SELECT id FROM chart_of_accounts WHERE is_active=1 ORDER BY code"
                ).fetchall()]
            finally:c.close()
            ledgers=[repo.general_ledger(account_id,start,end,None) for account_id in account_ids]
        rows=[];sections=[];grand_opening=grand_debit=grand_credit=grand_ending=0.0
        for d in ledgers:
            account=d["account"];partner=d.get("partner")
            section_rows=[]
            for x in d["items"]:
                row={"kode_akun":account.get("code"),"nama_akun":account.get("name"),
                  "tanggal":x["journal_date"],"nomor":x["journal_no"],
                  "keterangan":x["description"],"memo":x.get("memo") or "",
                  "partner":x.get("partner_name") or "-",
                  "referensi":x.get("reference_no") or "-",
                  "debit":float(x["debit"] or 0),"kredit":float(x["credit"] or 0),
                  "saldo":float(x["running_balance"] or 0)}
                rows.append(row);section_rows.append(row)
            section={"kode_akun":account.get("code"),"nama_akun":account.get("name"),
              "tipe_akun":account.get("account_subtype") or account.get("account_type"),
              "normal_balance":account.get("normal_balance"),
              "partner":partner.get("code")+" - "+partner.get("name") if partner else "Semua",
              "saldo_awal":float(d["opening_balance"] or 0),
              "total_debit":float(d["period_debit"] or 0),
              "total_kredit":float(d["period_credit"] or 0),
              "saldo_akhir":float(d["ending_balance"] or 0),"rows":section_rows}
            sections.append(section)
            grand_opening+=section["saldo_awal"];grand_debit+=section["total_debit"]
            grand_credit+=section["total_kredit"];grand_ending+=section["saldo_akhir"]
        if aid:
            summary=dict(sections[0]);summary.pop("rows",None);summary["all_accounts"]=False
        else:
            summary={"kode_akun":"SEMUA","nama_akun":"Semua Akun","tipe_akun":"Semua Tipe",
              "normal_balance":"-","partner":"Semua","saldo_awal":round(grand_opening,2),
              "total_debit":round(grand_debit,2),"total_kredit":round(grand_credit,2),
              "saldo_akhir":round(grand_ending,2),"all_accounts":True,
              "jumlah_akun":len(sections),"sections":sections}
        return _table(REPORT_NAMES[kind],columns,rows,summary)
    if kind=="finance_trial":
        d=repo.trial_balance(start,end)
        return _table(REPORT_NAMES[kind],
          [("code","Kode"),("name","Akun"),("opening_debit","Saldo Awal Debit"),("opening_credit","Saldo Awal Kredit"),
           ("period_debit","Mutasi Debit"),("period_credit","Mutasi Kredit"),
           ("ending_debit","Saldo Akhir Debit"),("ending_credit","Saldo Akhir Kredit")],d["items"],
          {"total_debit":d["total_ending_debit"],"total_kredit":d["total_ending_credit"]})
    if kind=="finance_income":
        d=repo.income_statement(start,end);rows=[]
        for group,key in (("Pendapatan","revenue_items"),("Harga Pokok Penjualan","hpp_items"),("Biaya Operasional","expense_items")):
            rows += [{"kelompok":group,"kode":x["code"],"akun":x["name"],"jumlah":x["amount"]} for x in d[key]]
        return _table(REPORT_NAMES[kind],
          [("kelompok","Kelompok"),("kode","Kode"),("akun","Akun"),("jumlah","Jumlah")],rows,
          {"pendapatan":d["revenue"],"hpp":d["hpp"],"laba_kotor":d["gross_profit"],
           "biaya_operasional":d["operating_expense"],"laba_usaha":d["net_profit"],
           "laba_bersih":d["net_profit"]})
    if kind=="finance_balance":return _balance_sheet(filters)
    c=connect()
    try:
      if kind=="finance_journals":
        where=["j.status='POSTED'"];params=[]
        if start:where.append("j.journal_date>=?");params.append(start)
        if end:where.append("j.journal_date<=?");params.append(end)
        sql=f"""SELECT j.journal_date tanggal,j.journal_no nomor,j.description keterangan,
          COALESCE(j.source_type,'MANUAL') sumber,COALESCE(j.reference_no,'-') referensi,
          a.code kode_akun,a.name akun,l.debit,l.credit,COALESCE(bp.name,'-') partner
          FROM journal_entries j JOIN journal_lines l ON l.journal_id=j.id
          JOIN chart_of_accounts a ON a.id=l.account_id
          LEFT JOIN business_partners bp ON bp.id=l.partner_id
          WHERE {' AND '.join(where)} ORDER BY j.journal_date,j.id,l.id"""
        rows=[dict(x) for x in c.execute(sql,params)]
        return _table(REPORT_NAMES[kind],
          [("tanggal","Tanggal"),("nomor","Nomor Jurnal"),("keterangan","Keterangan"),("sumber","Sumber"),
           ("referensi","Referensi"),("kode_akun","Kode Akun"),("akun","Akun"),
           ("partner","Partner"),("debit","Debit"),("credit","Kredit")],rows)
      if kind=="finance_cashflow":
        # Direct-method cash flow. Internal cash/bank transfers are excluded.
        where=["ct.transaction_type IN ('IN','OUT','TRANSFER_IN','TRANSFER_OUT')",
          "NOT EXISTS(SELECT 1 FROM transaction_voids v WHERE v.transaction_key=CAST(ct.id AS TEXT) AND v.transaction_kind IN ('cash','cash_reversal'))"];params=[]
        if start:where.append("ct.transaction_date>=?");params.append(start)
        if end:where.append("ct.transaction_date<=?");params.append(end)
        sql=f"""SELECT ct.id,ct.transaction_date tanggal,ct.transaction_no nomor,
          ca.code||' - '||ca.name akun_bank,ct.description keterangan,
          COALESCE(ct.reference_no,'-') referensi,ct.transaction_type,ct.amount,
          (SELECT coa.code FROM journal_entries j
             JOIN journal_lines jl ON jl.journal_id=j.id
             JOIN chart_of_accounts coa ON coa.id=jl.account_id
            WHERE j.source_type='CASH_TRANSACTION' AND j.source_id=ct.id
              AND j.status='POSTED'
              AND COALESCE(coa.account_subtype,'')<>'CASH_BANK'
            ORDER BY jl.id LIMIT 1) kode_lawan,
          (SELECT coa.name FROM journal_entries j
             JOIN journal_lines jl ON jl.journal_id=j.id
             JOIN chart_of_accounts coa ON coa.id=jl.account_id
            WHERE j.source_type='CASH_TRANSACTION' AND j.source_id=ct.id
              AND j.status='POSTED'
              AND COALESCE(coa.account_subtype,'')<>'CASH_BANK'
            ORDER BY jl.id LIMIT 1) akun_lawan,
          (SELECT coa.account_type FROM journal_entries j
             JOIN journal_lines jl ON jl.journal_id=j.id
             JOIN chart_of_accounts coa ON coa.id=jl.account_id
            WHERE j.source_type='CASH_TRANSACTION' AND j.source_id=ct.id
              AND j.status='POSTED'
              AND COALESCE(coa.account_subtype,'')<>'CASH_BANK'
            ORDER BY jl.id LIMIT 1) account_type,
          COALESCE((SELECT coa.account_subtype FROM journal_entries j
             JOIN journal_lines jl ON jl.journal_id=j.id
             JOIN chart_of_accounts coa ON coa.id=jl.account_id
            WHERE j.source_type='CASH_TRANSACTION' AND j.source_id=ct.id
              AND j.status='POSTED'
              AND COALESCE(coa.account_subtype,'')<>'CASH_BANK'
            ORDER BY jl.id LIMIT 1),'') account_subtype
          FROM cash_transactions ct
          JOIN cash_accounts ca ON ca.id=ct.account_id
          WHERE {' AND '.join(where)}
          ORDER BY ct.transaction_date,ct.id"""
        raw=[dict(x) for x in c.execute(sql,params)]

        def classify(row):
            if str(row.get('transaction_type') or '').startswith('TRANSFER_'):
                return 'Transfer Internal'
            typ=(row.get("account_type") or "").upper()
            subtype=(row.get("account_subtype") or "").upper()
            name=(row.get("akun_lawan") or "").upper()
            if typ in ("LIABILITY","EQUITY"):
                return "Aktivitas Pendanaan"
            if typ=="ASSET" and subtype not in ("RECEIVABLE","INVENTORY","CASH_BANK"):
                return "Aktivitas Investasi"
            if any(word in name for word in ("ASET TETAP","KENDARAAN","BANGUNAN","TANAH","PERALATAN")):
                return "Aktivitas Investasi"
            return "Aktivitas Operasi"

        rows=[]
        totals={"Aktivitas Operasi":0.0,"Aktivitas Investasi":0.0,
                "Aktivitas Pendanaan":0.0,"Transfer Internal":0.0}
        total_in=total_out=0.0
        for item in raw:
            amount=float(item.get("amount") or 0)
            incoming=item.get("transaction_type") in ("IN","TRANSFER_IN")
            value=amount if incoming else -amount
            group=classify(item)
            totals[group]+=value
            total_in+=amount if incoming else 0
            total_out+=amount if not incoming else 0
            rows.append({"aktivitas":group,"tanggal":item["tanggal"],"nomor":item["nomor"],
              "uraian":item.get("keterangan") or "-",
              "akun_lawan":((item.get("kode_lawan") or "")+" - "+
                            (item.get("akun_lawan") or "")).strip(" -") or "-",
              "referensi":item.get("referensi") or "-",
              "penerimaan":amount if incoming else 0,
              "pengeluaran":amount if not incoming else 0,
              "arus_bersih":value})

        opening=float(c.execute(
          "SELECT COALESCE(SUM(opening_balance),0) saldo FROM cash_accounts"
        ).fetchone()["saldo"] or 0)
        if start:
            movement=c.execute("""SELECT COALESCE(SUM(
              CASE WHEN transaction_type IN ('IN','TRANSFER_IN') THEN amount
                   WHEN transaction_type IN ('OUT','TRANSFER_OUT') THEN -amount
                   ELSE 0 END),0) saldo
              FROM cash_transactions ct WHERE transaction_date<?
                AND NOT EXISTS(SELECT 1 FROM transaction_voids v
                  WHERE v.transaction_key=CAST(ct.id AS TEXT)
                    AND v.transaction_kind IN ('cash','cash_reversal'))""",(start,)).fetchone()
            opening+=float(movement["saldo"] or 0)
        net=sum(totals.values())
        ending=opening+net
        return _table(REPORT_NAMES[kind],
          [("aktivitas","Aktivitas"),("tanggal","Tanggal"),("nomor","No. Bukti"),
           ("uraian","Uraian"),("akun_lawan","Akun Lawan"),("referensi","Referensi"),
           ("penerimaan","Penerimaan"),("pengeluaran","Pengeluaran"),
           ("arus_bersih","Arus Bersih")],rows,
          {"aktivitas_operasi":round(totals["Aktivitas Operasi"],2),
           "aktivitas_investasi":round(totals["Aktivitas Investasi"],2),
           "aktivitas_pendanaan":round(totals["Aktivitas Pendanaan"],2),
           "total_penerimaan":round(total_in,2),"total_pengeluaran":round(total_out,2),
           "saldo_awal_kas":round(opening,2),"kenaikan_penurunan_kas":round(net,2),
           "saldo_akhir_kas":round(ending,2)})
    finally:c.close()
    raise ValueError("Jenis laporan keuangan tidak valid.")


def _cash_bank_report(kind,filters):
    start,end=_period(filters)
    cash_account_id=_id(filters.get("cash_account_id"))
    # Sama seperti daftar Kas/Bank dan Arus Kas: transaksi lama yang sudah di-edit/VOID
    # serta reversal internal tidak boleh muncul sebagai transaksi operasional aktif.
    where=["NOT EXISTS(SELECT 1 FROM transaction_voids v WHERE v.transaction_key=CAST(ct.id AS TEXT) AND v.transaction_kind IN ('cash','cash_reversal'))"];params=[]
    if kind=="cash_in":where.append("ct.transaction_type IN ('IN','TRANSFER_IN')")
    elif kind=="cash_out":where.append("ct.transaction_type IN ('OUT','TRANSFER_OUT')")
    if start:where.append("ct.transaction_date>=?");params.append(start)
    if end:where.append("ct.transaction_date<=?");params.append(end)
    if cash_account_id:where.append("ct.account_id=?");params.append(cash_account_id)
    c=connect()
    try:
        rows=[dict(x) for x in c.execute(f"""SELECT ct.transaction_date tanggal,
          ct.transaction_no nomor,ca.code kode_akun,ca.name akun_kas_bank,
          CASE ct.transaction_type WHEN 'IN' THEN 'Kas/Bank Masuk'
          WHEN 'OUT' THEN 'Kas/Bank Keluar' WHEN 'TRANSFER_IN' THEN 'Transfer Masuk'
          WHEN 'TRANSFER_OUT' THEN 'Transfer Keluar' ELSE ct.transaction_type END jenis,
          ct.description keterangan,COALESCE(ct.reference_no,'-') referensi,
          CASE WHEN ct.transaction_type IN ('IN','TRANSFER_IN') THEN ct.amount ELSE 0 END penerimaan,
          CASE WHEN ct.transaction_type IN ('OUT','TRANSFER_OUT') THEN ct.amount ELSE 0 END pengeluaran,
          ct.balance_before saldo_awal,ct.balance_after saldo_akhir
          FROM cash_transactions ct JOIN cash_accounts ca ON ca.id=ct.account_id
          WHERE {' AND '.join(where)} ORDER BY ct.transaction_date,ct.id""",params)]
    finally:c.close()
    for row in rows:
        for key in ("penerimaan","pengeluaran","saldo_awal","saldo_akhir"):
            row[key]=float(row[key] or 0)
    return _table(REPORT_NAMES[kind],
      [("tanggal","Tanggal"),("nomor","Nomor"),("kode_akun","Kode"),
       ("akun_kas_bank","Kas/Bank"),("jenis","Jenis"),("keterangan","Keterangan"),
       ("referensi","Referensi"),("penerimaan","Penerimaan"),
       ("pengeluaran","Pengeluaran"),("saldo_awal","Saldo Sebelum"),
       ("saldo_akhir","Saldo Sesudah")],rows,{
       "total_penerimaan":sum(x["penerimaan"] for x in rows),
       "total_pengeluaran":sum(x["pengeluaran"] for x in rows),
       "arus_bersih":sum(x["penerimaan"]-x["pengeluaran"] for x in rows)})

def _ar_ap_report(kind,filters):
    is_ar=kind=="finance_receivables"
    start,end=_period(filters)
    as_of=end or date.today().isoformat()
    partner_key="customer_id" if is_ar else "supplier_id"
    partner_id=_id(filters.get(partner_key))
    table="sales" if is_ar else "purchases"
    invoice_no="invoice_no" if is_ar else "purchase_no"
    trx_date="sale_date" if is_ar else "purchase_date"
    party_col="customer_id" if is_ar else "supplier_id"
    pay_table="receivable_payments" if is_ar else "payable_payments"
    pay_fk="sale_id" if is_ar else "purchase_id"
    void_kind="receivable" if is_ar else "payable"
    alloc_type="CUSTOMER" if is_ar else "SUPPLIER"
    c=connect()
    try:
        where=[f"i.status='POSTED'",f"i.{trx_date}<=?"]
        params=[as_of]
        # Laporan piutang/hutang adalah posisi saldo per tanggal, bukan hanya faktur yang dibuat di periode filter.
        # Faktur lama yang masih outstanding tetap wajib muncul.
        if partner_id:
            where.append(f"i.{party_col}=?");params.append(partner_id)
        sql=f"""SELECT i.id,i.{invoice_no} nomor,i.{trx_date} tanggal,
          i.due_date jatuh_tempo,CAST(i.total_amount AS REAL) total_invoice,
          CAST(i.paid_amount AS REAL) paid_stored,CAST(i.balance_due AS REAL) current_balance,
          bp.id partner_id,bp.code partner_code,bp.name partner_name
          FROM {table} i JOIN business_partners bp ON bp.id=i.{party_col}
          WHERE {' AND '.join(where)} ORDER BY bp.name,i.{trx_date},i.id"""
        invoices=[dict(x) for x in c.execute(sql,params)]
        rows=[]
        buckets={'belum_jatuh_tempo':0.0,'umur_1_30':0.0,'umur_31_60':0.0,'umur_61_90':0.0,'umur_diatas_90':0.0}
        for inv in invoices:
            all_pay=float(c.execute(f"""SELECT COALESCE(SUM(CAST(p.amount AS REAL)),0) total FROM {pay_table} p
              WHERE p.{pay_fk}=? AND NOT EXISTS(SELECT 1 FROM transaction_voids v
              WHERE v.transaction_kind=? AND v.transaction_key=CAST(p.id AS TEXT))""",(inv['id'],void_kind)).fetchone()['total'] or 0)
            pay_to_date=float(c.execute(f"""SELECT COALESCE(SUM(CAST(p.amount AS REAL)),0) total FROM {pay_table} p
              WHERE p.{pay_fk}=? AND p.payment_date<=? AND NOT EXISTS(SELECT 1 FROM transaction_voids v
              WHERE v.transaction_kind=? AND v.transaction_key=CAST(p.id AS TEXT))""",(inv['id'],as_of,void_kind)).fetchone()['total'] or 0)
            all_alloc=float(c.execute("""SELECT COALESCE(SUM(CAST(amount AS REAL)),0) total FROM downpayment_allocations
              WHERE allocation_type=? AND invoice_id=? AND status='POSTED'""",(alloc_type,inv['id'])).fetchone()['total'] or 0)
            alloc_to_date=float(c.execute("""SELECT COALESCE(SUM(CAST(amount AS REAL)),0) total FROM downpayment_allocations
              WHERE allocation_type=? AND invoice_id=? AND status='POSTED' AND allocation_date<=?""",(alloc_type,inv['id'],as_of)).fetchone()['total'] or 0)
            initial_paid=max(0.0,float(inv['paid_stored'] or 0)-all_pay-all_alloc)
            paid_as_of=initial_paid+pay_to_date+alloc_to_date
            if is_ar:
                returned=float(c.execute("SELECT COALESCE(SUM(CAST(total_sales AS REAL)),0) v FROM sales_returns WHERE sale_id=? AND status='POSTED' AND return_date<=?",(inv['id'],as_of)).fetchone()['v'] or 0)
            else:
                returned=float(c.execute("SELECT COALESCE(SUM(CAST(total_payable AS REAL)),0) v FROM purchase_returns WHERE purchase_id=? AND status='POSTED' AND return_date<=?",(inv['id'],as_of)).fetchone()['v'] or 0)
            net_invoice=max(0.0,float(inv['total_invoice'] or 0)-returned);balance=max(0.0,net_invoice-paid_as_of)
            if balance<=0.005:continue
            due=inv['jatuh_tempo'] or inv['tanggal']
            try:days=(date.fromisoformat(as_of)-date.fromisoformat(str(due)[:10])).days
            except:days=0
            overdue=max(0,days)
            bucket='belum_jatuh_tempo' if days<=0 else 'umur_1_30' if days<=30 else 'umur_31_60' if days<=60 else 'umur_61_90' if days<=90 else 'umur_diatas_90'
            buckets[bucket]+=balance
            rows.append({'partner_code':inv['partner_code'],'partner_name':inv['partner_name'],'nomor':inv['nomor'],
              'tanggal':inv['tanggal'],'jatuh_tempo':inv['jatuh_tempo'] or '-', 'total_invoice':net_invoice,
              'terbayar':paid_as_of,'saldo':balance,'hari_terlambat':overdue,
              'kelompok_umur':'Belum Jatuh Tempo' if days<=0 else '1-30 Hari' if days<=30 else '31-60 Hari' if days<=60 else '61-90 Hari' if days<=90 else '> 90 Hari'})
        # Saldo awal partner adalah bagian subledger AR/AP dan harus ikut laporan agar sama dengan Neraca/GL.
        pwhere=["is_active=1","partner_type IN (?,'BOTH')","COALESCE(opening_balance,0)<>0"]
        pargs=["CUSTOMER" if is_ar else "SUPPLIER"]
        if partner_id:pwhere.append("id=?");pargs.append(partner_id)
        openings=[dict(x) for x in c.execute("SELECT id,code,name,opening_balance,opening_balance_date FROM business_partners WHERE "+' AND '.join(pwhere),pargs).fetchall()]
        for op in openings:
            od=str(op.get('opening_balance_date') or as_of)[:10];gross=float(op.get('opening_balance') or 0)
            if od>as_of or gross<=0:continue
            opening_pay_table='opening_receivable_payments' if is_ar else 'opening_payable_payments'
            opening_fk='customer_id' if is_ar else 'supplier_id'
            paid_opening=float(c.execute(f"SELECT COALESCE(SUM(CAST(amount AS REAL)),0) v FROM {opening_pay_table} WHERE {opening_fk}=? AND payment_date<=?",(op['id'],as_of)).fetchone()['v'] or 0)+float(c.execute("SELECT COALESCE(SUM(CAST(amount AS REAL)),0) v FROM downpayment_allocations WHERE allocation_type=? AND invoice_id=? AND status='POSTED' AND allocation_date<=?",('CUSTOMER' if is_ar else 'SUPPLIER',-int(op['id']),as_of)).fetchone()['v'] or 0)
            bal=max(0.0,gross-paid_opening)
            if bal<=0.005:continue
            try:days=(date.fromisoformat(as_of)-date.fromisoformat(od)).days
            except:days=0
            bucket='belum_jatuh_tempo' if days<=0 else 'umur_1_30' if days<=30 else 'umur_31_60' if days<=60 else 'umur_61_90' if days<=90 else 'umur_diatas_90';buckets[bucket]+=bal
            rows.append({'partner_code':op['code'],'partner_name':op['name'],'nomor':'SALDO AWAL','tanggal':od,'jatuh_tempo':'-', 'total_invoice':gross,'terbayar':paid_opening,'saldo':bal,'hari_terlambat':max(0,days),'kelompok_umur':'Saldo Awal'})
        summary={'tanggal_laporan':as_of,'jumlah_partner':len(set(r['partner_code'] for r in rows)),
          'jumlah_invoice':len(rows),'total_invoice':sum(r['total_invoice'] for r in rows),
          'total_terbayar':sum(r['terbayar'] for r in rows),'total_saldo':sum(r['saldo'] for r in rows),**buckets}
        label='Pelanggan' if is_ar else 'Pemasok'
        return _table(REPORT_NAMES[kind],[('partner_code','Kode'),('partner_name',label),('nomor','No. Faktur'),
          ('tanggal','Tanggal'),('jatuh_tempo','Jatuh Tempo'),('total_invoice','Nilai Faktur'),
          ('terbayar','Terbayar/Alokasi DP'),('saldo','Saldo'),('hari_terlambat','Hari Terlambat'),('kelompok_umur','Umur')],rows,summary)
    finally:c.close()

def _project_report(kind,filters):
    start,end=_period(filters)
    if kind=="project_income":
        raw_ids=str(filters.get("project_ids") or filters.get("project_id") or "")
        project_ids=[int(x) for x in raw_ids.split(",") if str(x).strip().isdigit()]
        if not project_ids:raise ValueError("Pilih minimal satu proyek untuk Laba Rugi Proyek.")
        def one_project(project_id):
            c=connect()
            try:
                project=c.execute("""SELECT p.*,bp.name customer_name FROM projects p
                  LEFT JOIN business_partners bp ON bp.id=p.customer_id WHERE p.id=?""",(project_id,)).fetchone()
                if not project:raise ValueError("Proyek tidak ditemukan.")
                where=["j.status='POSTED'","jl.project_id=?"];params=[project_id]
                if start:where.append("j.journal_date>=?");params.append(start)
                if end:where.append("j.journal_date<=?");params.append(end)
                raw=[dict(x) for x in c.execute(f"""SELECT coa.code,coa.name akun,coa.account_type,
                  COALESCE(coa.account_subtype,'') account_subtype,SUM(CAST(jl.debit AS REAL)) debit,
                  SUM(CAST(jl.credit AS REAL)) kredit FROM journal_lines jl
                  JOIN journal_entries j ON j.id=jl.journal_id JOIN chart_of_accounts coa ON coa.id=jl.account_id
                  WHERE {' AND '.join(where)} GROUP BY coa.id ORDER BY coa.code""",params)]
                rows=[];rev=hpp=exp=0.0
                for x in raw:
                    d=float(x['debit'] or 0);k=float(x['kredit'] or 0);typ=(x['account_type'] or '').upper();sub=(x['account_subtype'] or '').upper()
                    if typ=='REVENUE':group='Pendapatan';amount=k-d;rev+=amount
                    elif sub=='HPP':group='Harga Pokok Penjualan';amount=d-k;hpp+=amount
                    elif typ=='EXPENSE' and sub!='HPP':group='Biaya Operasional';amount=d-k;exp+=amount
                    else:continue
                    rows.append({'kelompok':group,'kode':x['code'],'akun':x['akun'],'debit':d,'kredit':k,'jumlah':amount})
                budget=c.execute("SELECT COALESCE(material_budget,0) mb,COALESCE(expense_budget,0) eb FROM project_budgets WHERE project_id=?",(project_id,)).fetchone()
                mb=float(budget['mb'] or 0) if budget else 0;eb=float(budget['eb'] or 0) if budget else 0
                mat=float(c.execute("SELECT COALESCE(SUM(total_cost),0) t FROM project_material_issues WHERE project_id=? AND status='POSTED'",(project_id,)).fetchone()['t'] or 0)
                cost=float(c.execute("""SELECT COALESCE(SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL)),0) t
                  FROM journal_lines jl JOIN journal_entries j ON j.id=jl.journal_id JOIN chart_of_accounts coa ON coa.id=jl.account_id
                  WHERE j.status='POSTED' AND jl.project_id=? AND COALESCE(j.source_type,'')<>'PROJECT_MATERIAL_ISSUE'
                  AND (coa.account_type='EXPENSE' OR coa.account_subtype='HPP')""",(project_id,)).fetchone()['t'] or 0)
                gross=rev-hpp;net=gross-exp;tb=mb+eb;real=mat+cost
                summary={'project_id':project_id,'project_code':project['code'],'project_name':project['name'],'customer_name':project['customer_name'] or '-',
                  'pendapatan':rev,'hpp':hpp,'laba_kotor':gross,'biaya_operasional':exp,'laba_bersih':net,
                  'margin_percent':round(net/rev*100,2) if rev else 0,'total_budget':tb,'total_realization':real,
                  'remaining_budget':tb-real,'budget_usage_percent':round(real/tb*100,2) if tb else 0}
                return {'summary':summary,'rows':rows}
            finally:c.close()
        projects=[one_project(pid) for pid in project_ids]
        if len(projects)==1:
            p=projects[0]
            return _table(REPORT_NAMES[kind],[('kelompok','Kelompok'),('kode','Kode'),('akun','Nama Akun'),('debit','Debit'),('kredit','Kredit'),('jumlah','Jumlah')],p['rows'],p['summary'])
        return {'title':'Laba Rugi Multi Proyek','projects':projects,'summary':{'project_count':len(projects),'pendapatan':sum(p['summary']['pendapatan'] for p in projects),'hpp':sum(p['summary']['hpp'] for p in projects),'biaya_operasional':sum(p['summary']['biaya_operasional'] for p in projects),'laba_bersih':sum(p['summary']['laba_bersih'] for p in projects)},'columns':[],'rows':[]}
    if kind=="project_purchases":
        project_id=_id(filters.get("project_id"))
        if not project_id:raise ValueError("Pilih proyek untuk laporan Pembelian per Proyek.")
        supplier_id=_id(filters.get("supplier_id"));product_id=_id(filters.get("product_id"))
        department_id=_id(filters.get("department_id"));start,end=_period(filters)
        c=connect()
        try:
            project=c.execute("""SELECT p.code,p.name,bp.name customer_name FROM projects p
              LEFT JOIN business_partners bp ON bp.id=p.customer_id WHERE p.id=?""",(project_id,)).fetchone()
            if not project:raise ValueError("Proyek tidak ditemukan.")
            where=["p.status='POSTED'","p.project_id=?"];params=[project_id]
            if start:where.append("p.purchase_date>=?");params.append(start)
            if end:where.append("p.purchase_date<=?");params.append(end)
            if supplier_id:where.append("p.supplier_id=?");params.append(supplier_id)
            if product_id:where.append("pi.product_id=?");params.append(product_id)
            if department_id:where.append("p.department_id=?");params.append(department_id)
            rows=[dict(x) for x in c.execute(f"""SELECT p.purchase_date tanggal,
              p.purchase_no nomor_pembelian,COALESCE(p.supplier_invoice_no,'-') invoice_pemasok,
              bp.code supplier_code,bp.name pemasok,pr.sku,pr.name barang,
              pi.qty,pi.unit_cost harga,pi.discount_amount diskon,pi.line_total subtotal,
              COALESCE(d.name,'Tanpa Departemen') departemen,w.name gudang
              FROM purchase_items pi JOIN purchases p ON p.id=pi.purchase_id
              JOIN business_partners bp ON bp.id=p.supplier_id JOIN products pr ON pr.id=pi.product_id
              JOIN warehouses w ON w.id=p.warehouse_id LEFT JOIN departments d ON d.id=p.department_id
              WHERE {' AND '.join(where)} ORDER BY p.purchase_date,p.id,pi.id""",params)]
            for row in rows:
                for key in ("qty","harga","diskon","subtotal"):row[key]=float(row[key] or 0)
            return _table(REPORT_NAMES[kind],[("tanggal","Tanggal"),("nomor_pembelian","No. Pembelian"),
              ("invoice_pemasok","Invoice/Referensi"),("supplier_code","Kode Pemasok"),
              ("pemasok","Pemasok"),("sku","SKU"),("barang","Barang"),("qty","Qty"),
              ("harga","Harga"),("diskon","Diskon"),("subtotal","Subtotal"),
              ("departemen","Departemen"),("gudang","Gudang")],rows,{
              "project_code":project["code"],"project_name":project["name"],
              "customer_name":project["customer_name"] or "-",
              "transaction_count":len(set(x["nomor_pembelian"] for x in rows)),
              "item_line_count":len(rows),"total_qty":sum(x["qty"] for x in rows),
              "total_purchase":sum(x["subtotal"] for x in rows)})
        finally:c.close()

    if kind=="project_materials":
        project_id=_id(filters.get("project_id"))
        if not project_id:raise ValueError("Pilih proyek untuk laporan Pengeluaran Material.")
        product_id=_id(filters.get("product_id"));department_id=_id(filters.get("department_id"))
        warehouse_id=_id(filters.get("warehouse_id"));start,end=_period(filters)
        c=connect()
        try:
            project=c.execute("""SELECT p.code,p.name,bp.name customer_name FROM projects p
              LEFT JOIN business_partners bp ON bp.id=p.customer_id WHERE p.id=?""",(project_id,)).fetchone()
            if not project:raise ValueError("Proyek tidak ditemukan.")
            where=["i.status='POSTED'","i.project_id=?"];params=[project_id]
            if start:where.append("i.issue_date>=?");params.append(start)
            if end:where.append("i.issue_date<=?");params.append(end)
            if product_id:where.append("mi.product_id=?");params.append(product_id)
            if department_id:where.append("i.department_id=?");params.append(department_id)
            if warehouse_id:where.append("i.warehouse_id=?");params.append(warehouse_id)
            rows=[dict(x) for x in c.execute(f"""SELECT i.issue_date tanggal,i.issue_no nomor,
              pr.sku,pr.name barang,mi.qty,mi.average_cost,mi.total_cost,w.name gudang,
              COALESCE(d.name,'Tanpa Departemen') departemen,coa.code account_code,
              coa.name akun_pengeluaran,COALESCE(i.notes,'-') keterangan
              FROM project_material_issue_items mi JOIN project_material_issues i ON i.id=mi.issue_id
              JOIN products pr ON pr.id=mi.product_id JOIN warehouses w ON w.id=i.warehouse_id
              JOIN chart_of_accounts coa ON coa.id=i.expense_account_id
              LEFT JOIN departments d ON d.id=i.department_id
              WHERE {' AND '.join(where)} ORDER BY i.issue_date,i.id,mi.id""",params)]
            for row in rows:
                for key in ("qty","average_cost","total_cost"):row[key]=float(row[key] or 0)
            return _table(REPORT_NAMES[kind],[("tanggal","Tanggal"),("nomor","No. PMI"),
              ("sku","SKU"),("barang","Barang"),("qty","Qty"),("average_cost","Average Cost"),
              ("total_cost","Total Cost"),("gudang","Gudang"),("departemen","Departemen"),
              ("account_code","Kode Akun"),("akun_pengeluaran","Akun Pengeluaran"),
              ("keterangan","Keterangan")],rows,{
              "project_code":project["code"],"project_name":project["name"],
              "customer_name":project["customer_name"] or "-",
              "transaction_count":len(set(x["nomor"] for x in rows)),
              "item_line_count":len(rows),"total_qty":sum(x["qty"] for x in rows),
              "total_material_cost":sum(x["total_cost"] for x in rows)})
        finally:c.close()

    if kind=="project_cost_detail":
        project_id=_id(filters.get("project_id"))
        if not project_id:raise ValueError("Pilih proyek untuk laporan Rincian Biaya per Proyek.")
        department_id=_id(filters.get("department_id"));account_id=_id(filters.get("account_id"));start,end=_period(filters)
        c=connect()
        try:
            project=c.execute("""SELECT p.code,p.name,bp.name customer_name FROM projects p
              LEFT JOIN business_partners bp ON bp.id=p.customer_id WHERE p.id=?""",(project_id,)).fetchone()
            if not project:raise ValueError("Proyek tidak ditemukan.")
            rows=[]
            mw=["i.status='POSTED'","i.project_id=?"];mp=[project_id]
            if start:mw.append("i.issue_date>=?");mp.append(start)
            if end:mw.append("i.issue_date<=?");mp.append(end)
            if department_id:mw.append("i.department_id=?");mp.append(department_id)
            if account_id:mw.append("i.expense_account_id=?");mp.append(account_id)
            for x in c.execute(f"""SELECT i.issue_date tanggal,i.issue_no nomor,'MATERIAL' kategori,
              coa.code account_code,coa.name akun,COALESCE(d.name,'Tanpa Departemen') departemen,
              pr.sku||' - '||pr.name uraian,mi.total_cost nilai,'PROJECT_MATERIAL_ISSUE' sumber
              FROM project_material_issue_items mi JOIN project_material_issues i ON i.id=mi.issue_id
              JOIN products pr ON pr.id=mi.product_id JOIN chart_of_accounts coa ON coa.id=i.expense_account_id
              LEFT JOIN departments d ON d.id=i.department_id WHERE {' AND '.join(mw)}
              ORDER BY i.issue_date,i.id,mi.id""",mp):rows.append(dict(x))
            jw=["j.status='POSTED'","jl.project_id=?","COALESCE(j.source_type,'')<>'PROJECT_MATERIAL_ISSUE'","(coa.account_type='EXPENSE' OR coa.account_subtype='HPP')"];jp=[project_id]
            if start:jw.append("j.journal_date>=?");jp.append(start)
            if end:jw.append("j.journal_date<=?");jp.append(end)
            if department_id:jw.append("COALESCE(jl.department_id,j.department_id)=?");jp.append(department_id)
            if account_id:jw.append("jl.account_id=?");jp.append(account_id)
            for x in c.execute(f"""SELECT j.journal_date tanggal,j.journal_no nomor,
              CASE WHEN coa.account_subtype='HPP' THEN 'HPP/BIAYA LANGSUNG' ELSE 'BIAYA OPERASIONAL' END kategori,
              coa.code account_code,coa.name akun,COALESCE(d.name,'Tanpa Departemen') departemen,
              COALESCE(NULLIF(jl.memo,''),j.description) uraian,
              (CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL)) nilai,COALESCE(j.source_type,'JURNAL') sumber
              FROM journal_lines jl JOIN journal_entries j ON j.id=jl.journal_id
              JOIN chart_of_accounts coa ON coa.id=jl.account_id
              LEFT JOIN departments d ON d.id=COALESCE(jl.department_id,j.department_id)
              WHERE {' AND '.join(jw)} ORDER BY j.journal_date,j.id,jl.id""",jp):
                r=dict(x)
                if abs(float(r['nilai'] or 0))>0.000001:rows.append(r)
            rows.sort(key=lambda r:(str(r.get('tanggal') or ''),str(r.get('nomor') or '')))
            for r in rows:r['nilai']=float(r['nilai'] or 0)
            by_cat={}
            for r in rows:by_cat[r['kategori']]=by_cat.get(r['kategori'],0)+r['nilai']
            return _table(REPORT_NAMES[kind],[('tanggal','Tanggal'),('nomor','No. Transaksi'),('kategori','Kategori Biaya'),
              ('account_code','Kode Akun'),('akun','Akun Biaya'),('departemen','Departemen'),('uraian','Uraian'),
              ('sumber','Sumber'),('nilai','Nilai Biaya')],rows,{'project_code':project['code'],'project_name':project['name'],
              'customer_name':project['customer_name'] or '-','transaction_lines':len(rows),'total_biaya':sum(r['nilai'] for r in rows),
              'material':by_cat.get('MATERIAL',0),'hpp_biaya_langsung':by_cat.get('HPP/BIAYA LANGSUNG',0),
              'biaya_operasional':by_cat.get('BIAYA OPERASIONAL',0)})
        finally:c.close()

    if kind=="project_summary":
        c=connect()
        try:
            status=str(filters.get('project_status') or '').upper();where='WHERE p.status=?' if status else '';params=[status] if status else []
            rows=[]
            for p in c.execute(f"""SELECT p.id,p.code,p.name,p.status,bp.name customer_name FROM projects p
              LEFT JOIN business_partners bp ON bp.id=p.customer_id {where} ORDER BY p.code""",params):
                budget=c.execute("SELECT COALESCE(material_budget,0) mb,COALESCE(expense_budget,0) eb FROM project_budgets WHERE project_id=?",(p['id'],)).fetchone();tb=(float(budget['mb'])+float(budget['eb'])) if budget else 0
                mat=float(c.execute("SELECT COALESCE(SUM(total_cost),0) t FROM project_material_issues WHERE project_id=? AND status='POSTED'",(p['id'],)).fetchone()['t'] or 0)
                fin=c.execute("""SELECT COALESCE(SUM(CASE WHEN coa.account_type='REVENUE' THEN CAST(jl.credit AS REAL)-CAST(jl.debit AS REAL) ELSE 0 END),0) rev,
                  COALESCE(SUM(CASE WHEN coa.account_subtype='HPP' THEN CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL) ELSE 0 END),0) hpp,
                  COALESCE(SUM(CASE WHEN coa.account_type='EXPENSE' AND COALESCE(coa.account_subtype,'')<>'HPP' THEN CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL) ELSE 0 END),0) exp
                  FROM journal_lines jl JOIN journal_entries j ON j.id=jl.journal_id JOIN chart_of_accounts coa ON coa.id=jl.account_id
                  WHERE j.status='POSTED' AND jl.project_id=?""",(p['id'],)).fetchone()
                cost=float(c.execute("""SELECT COALESCE(SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL)),0) t FROM journal_lines jl
                  JOIN journal_entries j ON j.id=jl.journal_id JOIN chart_of_accounts coa ON coa.id=jl.account_id
                  WHERE j.status='POSTED' AND jl.project_id=? AND COALESCE(j.source_type,'')<>'PROJECT_MATERIAL_ISSUE'
                  AND (coa.account_type='EXPENSE' OR coa.account_subtype='HPP')""",(p['id'],)).fetchone()['t'] or 0)
                rev=float(fin['rev']);hpp=float(fin['hpp']);exp=float(fin['exp']);real=mat+cost;net=rev-hpp-exp
                rows.append({'project_id':p['id'],'kode':p['code'],'proyek':p['name'],'pelanggan':p['customer_name'] or '-','status':p['status'],'total_budget':tb,'realisasi':real,'sisa_budget':tb-real,'pendapatan':rev,'hpp':hpp,'biaya':exp,'laba_bersih':net,'margin_percent':round(net/rev*100,2) if rev else 0,'budget_usage_percent':round(real/tb*100,2) if tb else 0})
            return _table(REPORT_NAMES[kind],[('kode','Kode'),('proyek','Proyek'),('pelanggan','Pelanggan'),('status','Status'),('total_budget','Total Budget'),('realisasi','Realisasi'),('sisa_budget','Sisa Budget'),('pendapatan','Pendapatan'),('hpp','HPP'),('biaya','Biaya'),('laba_bersih','Laba Bersih'),('margin_percent','Margin %'),('budget_usage_percent','Budget Terpakai %')],rows,{'project_count':len(rows),'total_budget':sum(x['total_budget'] for x in rows),'total_realization':sum(x['realisasi'] for x in rows),'remaining_budget':sum(x['sisa_budget'] for x in rows),'revenue':sum(x['pendapatan'] for x in rows),'net_profit':sum(x['laba_bersih'] for x in rows)})
        finally:c.close()
    raise ValueError("Jenis laporan proyek tidak valid.")

def _field_selected_table(data,filters):
    available=list(data.get("columns") or [])
    data["available_columns"]=available
    raw=str(filters.get("fields") or "").strip()
    if raw:
        wanted={x.strip() for x in raw.split(",") if x.strip()}
        data["columns"]=[c for c in available if c[0] in wanted]
        if not data["columns"]:raise ValueError("Pilih minimal satu field/kolom laporan.")
    return data

def _sales_detail_report(filters):
    start,end=_period(filters);where=["s.status='POSTED'"];params=[]
    if start:where.append("s.sale_date>=?");params.append(start)
    if end:where.append("s.sale_date<=?");params.append(end)
    extra,p2=_filters_sql(filters,{"product":"si.product_id","customer":"s.customer_id","salesperson":"s.salesperson_id","warehouse":"s.warehouse_id"});where+=extra;params+=p2
    c=connect()
    try:
        rows=[dict(x) for x in c.execute(f"""SELECT s.invoice_no,s.delivery_no,s.sale_date,
          COALESCE(bp.code,'') customer_code,COALESCE(bp.name,'Pelanggan Umum') customer_name,
          COALESCE(sp.code,'') salesperson_code,COALESCE(sp.name,'') salesperson_name,
          COALESCE(w.code,'') warehouse_code,COALESCE(w.name,'') warehouse_name,
          COALESCE(d.code,'') department_code,COALESCE(d.name,'') department_name,
          COALESCE(prj.code,'') project_code,COALESCE(prj.name,'') project_name,
          s.payment_type,COALESCE(s.payment_method,'') payment_method,COALESCE(ca.code,'') cash_account_code,COALESCE(ca.name,'') cash_account_name,
          s.due_date,s.tax_percent,s.tax_amount,s.subtotal invoice_subtotal,s.discount_amount invoice_discount,s.total_amount invoice_total,
          s.paid_amount,s.balance_due,COALESCE(s.notes,'') invoice_notes,s.status,COALESCE(so.order_no,'') sales_order_no,
          COALESCE(u.username,'') created_by,s.created_at,
          si.sku,si.product_name,si.product_type,COALESCE(si.unit_code,'') unit_code,COALESCE(si.entered_qty,si.qty) entered_qty,
          si.qty base_qty,COALESCE(si.conversion_ratio,1) conversion_ratio,si.unit_price,COALESCE(si.discount_percent,0) item_discount_percent,
          si.discount_amount item_discount,(CAST(si.discount_amount AS REAL)+CASE WHEN CAST(s.subtotal AS REAL)>0 THEN CAST(s.discount_amount AS REAL)*(CAST(si.line_total AS REAL)/CAST(s.subtotal AS REAL)) ELSE 0 END) total_discount,si.line_total item_total,
          (CASE WHEN CAST(si.qty AS REAL)<>0 THEN ((CASE WHEN COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)>0 THEN (COALESCE((SELECT SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL))
      FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
      JOIN chart_of_accounts ja ON ja.id=jl.account_id
      WHERE je.status='POSTED' AND je.source_type='SALE' AND je.source_id=s.id
        AND ja.account_subtype='HPP'),0))*((CAST(si.qty AS REAL)*(CASE WHEN p.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it.quantity_change AS REAL))*CAST(it.unit_cost AS REAL))/SUM(ABS(CAST(it.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it
        WHERE it.reference_type='SALE' AND it.reference_no=s.invoice_no AND it.product_id=si.product_id
      ),CAST(si.purchase_price_snapshot AS REAL),0) ELSE 0 END)))/(COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)) ELSE 0 END))/CAST(si.qty AS REAL) ELSE 0 END) unit_cost,
          ((CASE WHEN COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)>0 THEN (COALESCE((SELECT SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL))
      FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
      JOIN chart_of_accounts ja ON ja.id=jl.account_id
      WHERE je.status='POSTED' AND je.source_type='SALE' AND je.source_id=s.id
        AND ja.account_subtype='HPP'),0))*((CAST(si.qty AS REAL)*(CASE WHEN p.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it.quantity_change AS REAL))*CAST(it.unit_cost AS REAL))/SUM(ABS(CAST(it.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it
        WHERE it.reference_type='SALE' AND it.reference_no=s.invoice_no AND it.product_id=si.product_id
      ),CAST(si.purchase_price_snapshot AS REAL),0) ELSE 0 END)))/(COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)) ELSE 0 END)) item_hpp,
          (CAST(si.line_total AS REAL)-((CASE WHEN COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)>0 THEN (COALESCE((SELECT SUM(CAST(jl.debit AS REAL)-CAST(jl.credit AS REAL))
      FROM journal_entries je JOIN journal_lines jl ON jl.journal_id=je.id
      JOIN chart_of_accounts ja ON ja.id=jl.account_id
      WHERE je.status='POSTED' AND je.source_type='SALE' AND je.source_id=s.id
        AND ja.account_subtype='HPP'),0))*((CAST(si.qty AS REAL)*(CASE WHEN p.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it.quantity_change AS REAL))*CAST(it.unit_cost AS REAL))/SUM(ABS(CAST(it.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it
        WHERE it.reference_type='SALE' AND it.reference_no=s.invoice_no AND it.product_id=si.product_id
      ),CAST(si.purchase_price_snapshot AS REAL),0) ELSE 0 END)))/(COALESCE((SELECT SUM(CAST(si2.qty AS REAL)*(CASE WHEN p2.product_type='STOCK' THEN COALESCE((
        SELECT CASE WHEN SUM(ABS(CAST(it2.quantity_change AS REAL)))>0
          THEN SUM(ABS(CAST(it2.quantity_change AS REAL))*CAST(it2.unit_cost AS REAL))/SUM(ABS(CAST(it2.quantity_change AS REAL))) ELSE 0 END
        FROM inventory_transactions it2
        WHERE it2.reference_type='SALE' AND it2.reference_no=s.invoice_no AND it2.product_id=si2.product_id
      ),CAST(si2.purchase_price_snapshot AS REAL),0) ELSE 0 END))
      FROM sales_items si2 JOIN products p2 ON p2.id=si2.product_id WHERE si2.sale_id=s.id),0)) ELSE 0 END))) item_gross_profit
          FROM sales_items si JOIN sales s ON s.id=si.sale_id JOIN products p ON p.id=si.product_id
          LEFT JOIN business_partners bp ON bp.id=s.customer_id LEFT JOIN salespersons sp ON sp.id=s.salesperson_id
          LEFT JOIN warehouses w ON w.id=s.warehouse_id LEFT JOIN departments d ON d.id=s.department_id LEFT JOIN projects prj ON prj.id=s.project_id
          LEFT JOIN cash_accounts ca ON ca.id=s.cash_account_id LEFT JOIN users u ON u.id=s.user_id LEFT JOIN sales_orders so ON so.id=s.sales_order_id
          WHERE {' AND '.join(where)} ORDER BY s.sale_date,s.id,si.id""",params)]
    finally:c.close()
    numeric=['tax_percent','tax_amount','invoice_subtotal','invoice_discount','invoice_total','paid_amount','balance_due','entered_qty','base_qty','conversion_ratio','unit_price','item_discount_percent','item_discount','total_discount','item_total','unit_cost','item_hpp','item_gross_profit']
    for r in rows:
        for k in numeric:r[k]=float(r[k] or 0)
    cols=[('invoice_no','No. Invoice'),('delivery_no','No. Surat Jalan'),('sale_date','Tanggal'),('customer_code','Kode Pelanggan'),('customer_name','Pelanggan'),('salesperson_code','Kode Sales'),('salesperson_name','Salesman'),('warehouse_code','Kode Gudang'),('warehouse_name','Gudang'),('department_code','Kode Departemen'),('department_name','Departemen'),('project_code','Kode Proyek'),('project_name','Proyek'),('payment_type','Tipe Pembayaran'),('payment_method','Metode Pembayaran'),('cash_account_code','Kode Kas/Bank'),('cash_account_name','Kas/Bank'),('due_date','Jatuh Tempo'),('tax_percent','PPN %'),('tax_amount','PPN'),('invoice_subtotal','Subtotal Invoice'),('invoice_discount','Diskon Invoice'),('invoice_total','Total Invoice'),('paid_amount','Terbayar'),('balance_due','Sisa Piutang'),('invoice_notes','Catatan Invoice'),('status','Status'),('sales_order_no','No. Pesanan Penjualan'),('created_by','Dibuat Oleh'),('created_at','Waktu Input'),('sku','SKU'),('product_name','Barang/Jasa'),('product_type','Jenis Item'),('unit_code','Satuan'),('entered_qty','Qty Input'),('base_qty','Qty Dasar'),('conversion_ratio','Konversi'),('unit_price','Harga Jual'),('item_discount_percent','Diskon Item %'),('item_discount','Diskon Item'),('total_discount','Total Diskon'),('item_total','Subtotal Item'),('unit_cost','Cost/Unit'),('item_hpp','HPP Item'),('item_gross_profit','Laba Kotor Item')]
    return _field_selected_table(_table(REPORT_NAMES['sales_detail'],cols,rows,{'jumlah_invoice':len(set(r['invoice_no'] for r in rows)),'jumlah_baris':len(rows),'total_penjualan':sum(r['item_total'] for r in rows),'total_diskon':sum(r.get('total_discount',0) for r in rows),'total_hpp':sum(r['item_hpp'] for r in rows),'total_laba_kotor':sum(r['item_gross_profit'] for r in rows)}),filters)

def _purchase_detail_report(filters):
    start,end=_period(filters);where=["p.status='POSTED'"];params=[]
    if start:where.append("p.purchase_date>=?");params.append(start)
    if end:where.append("p.purchase_date<=?");params.append(end)
    extra,p2=_filters_sql(filters,{"product":"pi.product_id","supplier":"p.supplier_id","warehouse":"p.warehouse_id"});where+=extra;params+=p2
    c=connect()
    try:
        rows=[dict(x) for x in c.execute(f"""SELECT p.purchase_no,p.supplier_invoice_no,p.goods_receipt_no,p.purchase_date,
          bp.code supplier_code,bp.name supplier_name,w.code warehouse_code,w.name warehouse_name,
          COALESCE(d.code,'') department_code,COALESCE(d.name,'') department_name,COALESCE(prj.code,'') project_code,COALESCE(prj.name,'') project_name,
          p.payment_type,COALESCE(p.payment_method,'') payment_method,COALESCE(ca.code,'') cash_account_code,COALESCE(ca.name,'') cash_account_name,
          p.due_date,p.tax_percent,p.tax_amount,p.subtotal purchase_subtotal,p.discount_amount purchase_discount,p.total_amount purchase_total,
          p.paid_amount,p.balance_due,COALESCE(p.notes,'') purchase_notes,p.status,COALESCE(po.order_no,'') purchase_order_no,
          COALESCE(u.username,'') created_by,p.created_at,
          pi.sku,pi.product_name,pi.product_type,COALESCE(pi.unit_code,'') unit_code,COALESCE(pi.entered_qty,pi.qty) entered_qty,
          pi.qty base_qty,COALESCE(pi.conversion_ratio,1) conversion_ratio,pi.unit_cost,COALESCE(pi.discount_percent,0) item_discount_percent,
          pi.discount_amount item_discount,pi.line_total item_total
          FROM purchase_items pi JOIN purchases p ON p.id=pi.purchase_id JOIN business_partners bp ON bp.id=p.supplier_id
          JOIN warehouses w ON w.id=p.warehouse_id LEFT JOIN departments d ON d.id=p.department_id LEFT JOIN projects prj ON prj.id=p.project_id
          LEFT JOIN cash_accounts ca ON ca.id=p.cash_account_id LEFT JOIN users u ON u.id=p.user_id LEFT JOIN purchase_orders po ON po.id=p.purchase_order_id
          WHERE {' AND '.join(where)} ORDER BY p.purchase_date,p.id,pi.id""",params)]
    finally:c.close()
    numeric=['tax_percent','tax_amount','purchase_subtotal','purchase_discount','purchase_total','paid_amount','balance_due','entered_qty','base_qty','conversion_ratio','unit_cost','item_discount_percent','item_discount','item_total']
    for r in rows:
        for k in numeric:r[k]=float(r[k] or 0)
    cols=[('purchase_no','No. Pembelian'),('supplier_invoice_no','Invoice Pemasok'),('goods_receipt_no','No. Good Receive'),('purchase_date','Tanggal'),('supplier_code','Kode Pemasok'),('supplier_name','Pemasok'),('warehouse_code','Kode Gudang'),('warehouse_name','Gudang'),('department_code','Kode Departemen'),('department_name','Departemen'),('project_code','Kode Proyek'),('project_name','Proyek'),('payment_type','Tipe Pembayaran'),('payment_method','Metode Pembayaran'),('cash_account_code','Kode Kas/Bank'),('cash_account_name','Kas/Bank'),('due_date','Jatuh Tempo'),('tax_percent','PPN %'),('tax_amount','PPN'),('purchase_subtotal','Subtotal Pembelian'),('purchase_discount','Diskon Pembelian'),('purchase_total','Total Pembelian'),('paid_amount','Terbayar'),('balance_due','Sisa Hutang'),('purchase_notes','Catatan'),('status','Status'),('purchase_order_no','No. Pesanan Pembelian'),('created_by','Dibuat Oleh'),('created_at','Waktu Input'),('sku','SKU'),('product_name','Barang/Jasa'),('product_type','Jenis Item'),('unit_code','Satuan'),('entered_qty','Qty Input'),('base_qty','Qty Dasar'),('conversion_ratio','Konversi'),('unit_cost','Harga Beli'),('item_discount_percent','Diskon Item %'),('item_discount','Diskon Item'),('item_total','Subtotal Item')]
    return _field_selected_table(_table(REPORT_NAMES['purchase_detail'],cols,rows,{'jumlah_pembelian':len(set(r['purchase_no'] for r in rows)),'jumlah_baris':len(rows),'total_pembelian':sum(r['item_total'] for r in rows)}),filters)

def _order_history_report(kind,filters):
    sale=kind=='sales_order_history';start,end=_period(filters);c=connect()
    try:
        if sale:
            where=['1=1'];params=[]
            if start:where.append('o.order_date>=?');params.append(start)
            if end:where.append('o.order_date<=?');params.append(end)
            rows=[dict(x) for x in c.execute(f"""SELECT o.order_no,o.order_date,o.expected_date,bp.code partner_code,bp.name partner_name,
              COALESCE(d.code,'') department_code,COALESCE(d.name,'') department_name,COALESCE(prj.code,'') project_code,COALESCE(prj.name,'') project_name,
              o.subtotal,o.discount_amount,o.tax_percent,o.tax_amount,o.total_amount,COALESCE(o.notes,'') notes,o.status,
              COALESCE((SELECT SUM(amount) FROM customer_downpayments dp WHERE dp.sales_order_id=o.id AND dp.status='POSTED'),0) dp_total,
              COALESCE((SELECT COUNT(*) FROM sales s WHERE s.sales_order_id=o.id AND s.status='POSTED'),0) invoice_count,
              oi.description item_description,p.sku,p.name product_name,oi.qty,oi.unit_price unit_value,oi.discount_amount item_discount,oi.line_total item_total
              FROM sales_orders o JOIN business_partners bp ON bp.id=o.customer_id LEFT JOIN departments d ON d.id=o.department_id LEFT JOIN projects prj ON prj.id=o.project_id
              JOIN sales_order_items oi ON oi.order_id=o.id JOIN products p ON p.id=oi.product_id WHERE {' AND '.join(where)} ORDER BY o.order_date,o.id,oi.id""",params)]
            title=REPORT_NAMES[kind]
        else:
            where=['1=1'];params=[]
            if start:where.append('o.order_date>=?');params.append(start)
            if end:where.append('o.order_date<=?');params.append(end)
            rows=[dict(x) for x in c.execute(f"""SELECT o.order_no,o.order_date,o.expected_date,bp.code partner_code,bp.name partner_name,w.code warehouse_code,w.name warehouse_name,
              COALESCE(d.code,'') department_code,COALESCE(d.name,'') department_name,COALESCE(prj.code,'') project_code,COALESCE(prj.name,'') project_name,
              o.subtotal,o.discount_amount,o.tax_percent,o.tax_amount,o.total_amount,COALESCE(o.notes,'') notes,o.status,
              COALESCE((SELECT SUM(amount) FROM supplier_downpayments dp WHERE dp.purchase_order_id=o.id AND dp.status='POSTED'),0) dp_total,
              COALESCE((SELECT COUNT(*) FROM purchases p2 WHERE p2.purchase_order_id=o.id AND p2.status='POSTED'),0) invoice_count,
              oi.description item_description,p.sku,p.name product_name,oi.qty,oi.unit_cost unit_value,oi.discount_amount item_discount,oi.line_total item_total
              FROM purchase_orders o JOIN business_partners bp ON bp.id=o.supplier_id JOIN warehouses w ON w.id=o.warehouse_id LEFT JOIN departments d ON d.id=o.department_id LEFT JOIN projects prj ON prj.id=o.project_id
              JOIN purchase_order_items oi ON oi.order_id=o.id JOIN products p ON p.id=oi.product_id WHERE {' AND '.join(where)} ORDER BY o.order_date,o.id,oi.id""",params)]
            title=REPORT_NAMES[kind]
    finally:c.close()
    for r in rows:
        for k in ('subtotal','discount_amount','tax_percent','tax_amount','total_amount','dp_total','qty','unit_value','item_discount','item_total','invoice_count'):r[k]=float(r[k] or 0)
    cols=[('order_no','No. Pesanan'),('order_date','Tanggal Pesanan'),('expected_date','Tanggal Rencana'),('partner_code','Kode Partner'),('partner_name','Pelanggan' if sale else 'Pemasok')]
    if not sale:cols += [('warehouse_code','Kode Gudang'),('warehouse_name','Gudang')]
    cols += [('department_code','Kode Departemen'),('department_name','Departemen'),('project_code','Kode Proyek'),('project_name','Proyek'),('status','Status'),('subtotal','Subtotal'),('discount_amount','Diskon'),('tax_percent','PPN %'),('tax_amount','PPN'),('total_amount','Total Pesanan'),('dp_total','Total DP'),('invoice_count','Jumlah Realisasi Invoice'),('notes','Catatan'),('sku','SKU'),('product_name','Barang/Jasa'),('item_description','Deskripsi'),('qty','Qty'),('unit_value','Harga'),('item_discount','Diskon Item'),('item_total','Subtotal Item')]
    return _table(title,cols,rows,{'jumlah_pesanan':len(set(r['order_no'] for r in rows)),'jumlah_baris':len(rows),'total_nilai':sum(r['item_total'] for r in rows),'total_dp':sum({r['order_no']:r['dp_total'] for r in rows}.values())})

def _dp_report(kind,filters):
    start,end=_period(filters);customer=kind in ('sales_dp','sales_dp_allocation');alloc=kind.endswith('_allocation');c=connect()
    try:
        if not alloc:
            table='customer_downpayments' if customer else 'supplier_downpayments';partner_col='customer_id' if customer else 'supplier_id';order_table='sales_orders' if customer else 'purchase_orders';order_col='sales_order_id' if customer else 'purchase_order_id'
            where=["dp.status='POSTED'"];params=[]
            if start:where.append('dp.dp_date>=?');params.append(start)
            if end:where.append('dp.dp_date<=?');params.append(end)
            rows=[dict(x) for x in c.execute(f"""SELECT dp.dp_no,dp.dp_date,bp.code partner_code,bp.name partner_name,COALESCE(o.order_no,'') order_no,
              ca.code cash_code,ca.name cash_name,dp.amount,dp.allocated_amount,(CAST(dp.amount AS REAL)-CAST(dp.allocated_amount AS REAL)) available_amount,
              COALESCE(dp.notes,'') notes,dp.status,dp.created_at FROM {table} dp JOIN business_partners bp ON bp.id=dp.{partner_col}
              LEFT JOIN {order_table} o ON o.id=dp.{order_col} JOIN cash_accounts ca ON ca.id=dp.cash_account_id WHERE {' AND '.join(where)} ORDER BY dp.dp_date,dp.id""",params)]
            cols=[('dp_no','No. DP'),('dp_date','Tanggal'),('partner_code','Kode Partner'),('partner_name','Pelanggan' if customer else 'Pemasok'),('order_no','No. Pesanan'),('cash_code','Kode Kas/Bank'),('cash_name','Kas/Bank'),('amount','Nilai DP'),('allocated_amount','Sudah Dialokasikan'),('available_amount','Sisa DP'),('notes','Catatan'),('status','Status'),('created_at','Waktu Input')]
        else:
            atype='CUSTOMER' if customer else 'SUPPLIER';dp_table='customer_downpayments' if customer else 'supplier_downpayments';doc_table='sales' if customer else 'purchases';doc_no='invoice_no' if customer else 'purchase_no';partner_col='customer_id' if customer else 'supplier_id'
            where=["a.status='POSTED'","a.allocation_type=?"];params=[atype]
            if start:where.append('a.allocation_date>=?');params.append(start)
            if end:where.append('a.allocation_date<=?');params.append(end)
            rows=[dict(x) for x in c.execute(f"""SELECT a.allocation_no,a.allocation_date,dp.dp_no,bp.code partner_code,bp.name partner_name,doc.{doc_no} document_no,
              a.amount,dp.amount dp_amount,dp.allocated_amount dp_allocated_total,(CAST(dp.amount AS REAL)-CAST(dp.allocated_amount AS REAL)) dp_remaining,
              doc.total_amount document_total,doc.balance_due document_balance,a.status,a.created_at
              FROM downpayment_allocations a JOIN {dp_table} dp ON dp.id=a.downpayment_id JOIN business_partners bp ON bp.id=dp.{partner_col}
              JOIN {doc_table} doc ON doc.id=a.invoice_id WHERE {' AND '.join(where)} ORDER BY a.allocation_date,a.id""",params)]
            cols=[('allocation_no','No. Alokasi'),('allocation_date','Tanggal'),('dp_no','No. DP'),('partner_code','Kode Partner'),('partner_name','Pelanggan' if customer else 'Pemasok'),('document_no','No. Invoice' if customer else 'No. Pembelian'),('amount','Nilai Alokasi'),('dp_amount','Nilai DP'),('dp_allocated_total','Total Alokasi DP'),('dp_remaining','Sisa DP'),('document_total','Nilai Dokumen'),('document_balance','Sisa Tagihan'),('status','Status'),('created_at','Waktu Input')]
    finally:c.close()
    for r in rows:
        for k,v in list(r.items()):
            if k in ('amount','allocated_amount','available_amount','dp_amount','dp_allocated_total','dp_remaining','document_total','document_balance'):r[k]=float(v or 0)
    return _table(REPORT_NAMES[kind],cols,rows,{'jumlah_baris':len(rows),'total':sum(float(r.get('amount') or 0) for r in rows)})

def report_data(kind,filters):
    if kind not in REPORT_NAMES:raise ValueError("Jenis laporan tidak dikenal.")
    if kind=="sales_detail":return _sales_detail_report(filters)
    if kind=="purchase_detail":return _purchase_detail_report(filters)
    if kind in ("sales_order_history","purchase_order_history"):return _order_history_report(kind,filters)
    if kind in ("sales_dp","sales_dp_allocation","purchase_dp","purchase_dp_allocation"):return _dp_report(kind,filters)
    if kind.startswith("sales_"):return _sales_report(kind,filters)
    if kind.startswith("purchase_"):return _purchase_report(kind,filters)
    if kind.startswith("stock_"):return _stock_report(kind,filters)
    if kind.startswith("cash_"):return _cash_bank_report(kind,filters)
    if kind.startswith("project_"):return _project_report(kind,filters)
    if kind in ("finance_receivables","finance_payables"):return _ar_ap_report(kind,filters)
    return _finance_report(kind,filters)

def _export_scalar(value):
    """Return a value that Excel/PDF writers can safely serialize."""
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    # Defensive fallback for report payloads containing nested metadata.
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        return str(value)

def _export_summary_items(summary):
    """Only export scalar summary values; nested report structures already exist in rows."""
    result=[]
    for key,value in (summary or {}).items():
        if isinstance(value, (dict, list, tuple, set)):
            # E.g. finance_ledger.summary.sections. Writing a list/dict directly is
            # rejected by openpyxl and was the cause of Buku Besar Excel errors.
            continue
        result.append((key,value))
    return result

def _safe_filename(title, ext):
    name=str(title or "Laporan").strip() or "Laporan"
    for ch in '<>:"/\\|?*':
        name=name.replace(ch,'-')
    return f"{name}.{ext}"


def _ledger_export_sections(data):
    """Return the exact account blocks used by the on-screen Buku Besar view."""
    summary=data.get("summary") or {}
    if summary.get("all_accounts"):
        return list(summary.get("sections") or [])
    section=dict(summary)
    section["rows"]=list(data.get("rows") or [])
    return [section]

def _ledger_money(value):
    try:return float(value or 0)
    except (TypeError,ValueError):return 0.0

def _export_finance_ledger_xlsx(data):
    from openpyxl import Workbook
    from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
    from openpyxl.utils import get_column_letter
    wb=Workbook();ws=wb.active;ws.title="Buku Besar"
    dark="173F73";pale="E7F3F5";green="DDF2E7";border="B8C8D2"
    thin=Side(style="thin",color=border)
    ws.merge_cells("A1:H1");ws["A1"]="BUKU BESAR";ws["A1"].font=Font(size=16,bold=True,color=dark);ws["A1"].alignment=Alignment(horizontal="center")
    period=data.get("period") or {}
    period_text=""
    if period.get("from") or period.get("to"):
        period_text=f"Periode {period.get('from') or '-'} s.d. {period.get('to') or '-'}"
    ws.merge_cells("A2:H2");ws["A2"]=period_text;ws["A2"].alignment=Alignment(horizontal="center");ws["A2"].font=Font(color="667788")
    row=4
    sections=_ledger_export_sections(data)
    for sec_i,section in enumerate(sections):
        if sec_i: row+=2
        # Four information cards, matching the browser view.
        info=[("Kode Akun",section.get("kode_akun") or "-"),("Nama Akun",section.get("nama_akun") or "-"),
              ("Tipe Akun",section.get("tipe_akun") or "-"),("Pelanggan / Pemasok",section.get("partner") or "Semua")]
        for i,(label,val) in enumerate(info):
            r=row+(i//2);c=1+(i%2)*4
            ws.merge_cells(start_row=r,start_column=c,end_row=r,end_column=c+1)
            ws.cell(r,c,label);ws.cell(r,c).font=Font(color="607D8B")
            ws.merge_cells(start_row=r,start_column=c+2,end_row=r,end_column=c+3)
            ws.cell(r,c+2,_export_scalar(val));ws.cell(r,c+2).font=Font(bold=True);ws.cell(r,c+2).alignment=Alignment(horizontal="right")
            for cc in range(c,c+4):
                ws.cell(r,cc).fill=PatternFill("solid",fgColor="F3F7F8");ws.cell(r,cc).border=Border(top=thin,bottom=thin)
        row+=3
        ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=7);ws.cell(row,1,"Saldo Awal");ws.cell(row,1).font=Font(bold=True)
        ws.cell(row,8,_ledger_money(section.get("saldo_awal")));ws.cell(row,8).font=Font(bold=True);ws.cell(row,8).number_format='#,##0;[Red]-#,##0'
        for c in range(1,9):ws.cell(row,c).fill=PatternFill("solid",fgColor=pale)
        row+=1
        headers=["Tanggal","No. Bukti","Keterangan","Partner","Referensi","Debit","Kredit","Saldo"]
        for c,h in enumerate(headers,1):
            cell=ws.cell(row,c,h);cell.font=Font(bold=True,color="FFFFFF");cell.fill=PatternFill("solid",fgColor=dark);cell.alignment=Alignment(horizontal="center",vertical="center")
        row+=1
        rows=list(section.get("rows") or [])
        if rows:
            for item in rows:
                vals=[item.get("tanggal"),item.get("nomor"),item.get("keterangan"),item.get("partner"),item.get("referensi"),
                      _ledger_money(item.get("debit")) if item.get("debit") else None,
                      _ledger_money(item.get("kredit")) if item.get("kredit") else None,_ledger_money(item.get("saldo"))]
                for c,v in enumerate(vals,1):
                    cell=ws.cell(row,c,_export_scalar(v));cell.alignment=Alignment(vertical="top",wrap_text=True)
                    if c>=6:cell.number_format='#,##0;[Red]-#,##0';cell.alignment=Alignment(horizontal="right",vertical="top")
                row+=1
        else:
            ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=8);ws.cell(row,1,"Tidak ada mutasi pada periode ini.");row+=1
        row+=1
        for label,key in [("Total Debit","total_debit"),("Total Kredit","total_kredit"),("Saldo Akhir","saldo_akhir")]:
            ws.merge_cells(start_row=row,start_column=6,end_row=row,end_column=7);ws.cell(row,6,label)
            ws.cell(row,8,_ledger_money(section.get(key)));ws.cell(row,8).font=Font(bold=True);ws.cell(row,8).number_format='#,##0;[Red]-#,##0'
            if key=="saldo_akhir":
                for c in range(6,9):ws.cell(row,c).fill=PatternFill("solid",fgColor=green)
            row+=1
    widths=[13,20,32,22,20,15,15,16]
    for i,w in enumerate(widths,1):ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes="A4"
    bio=io.BytesIO();wb.save(bio)
    return bio.getvalue(),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",_safe_filename(data.get("title"),"xlsx")

def _export_finance_ledger_pdf(data):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4,landscape
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,KeepTogether
    bio=io.BytesIO();page=landscape(A4);left=22;right=22
    doc=SimpleDocTemplate(bio,pagesize=page,leftMargin=left,rightMargin=right,topMargin=22,bottomMargin=22)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("LedgerTitle",parent=styles["Title"],fontSize=15,leading=18,textColor=colors.HexColor("#173F73"),alignment=1,spaceAfter=2)
    sub=ParagraphStyle("LedgerSub",parent=styles["BodyText"],fontSize=8,textColor=colors.HexColor("#667788"),alignment=1,spaceAfter=8)
    cell=ParagraphStyle("LedgerCell",parent=styles["BodyText"],fontSize=6.5,leading=8,spaceAfter=0,spaceBefore=0)
    head=ParagraphStyle("LedgerHead",parent=cell,fontName="Helvetica-Bold",textColor=colors.white,alignment=1)
    bold=ParagraphStyle("LedgerBold",parent=cell,fontName="Helvetica-Bold")
    def p(v,style=cell):return Paragraph(html.escape(str(_export_scalar(v))).replace("\n","<br/>"),style)
    period=data.get("period") or {}
    story=[Paragraph("BUKU BESAR",title),Paragraph(f"Periode {period.get('from') or '-'} s.d. {period.get('to') or '-'}",sub)]
    available=page[0]-left-right
    widths=[available*x for x in (.10,.15,.22,.15,.14,.08,.08,.08)]
    for section in _ledger_export_sections(data):
        info=[[p("Kode Akun"),p(section.get("kode_akun") or "-",bold),p("Nama Akun"),p(section.get("nama_akun") or "-",bold)],
              [p("Tipe Akun"),p(section.get("tipe_akun") or "-",bold),p("Pelanggan / Pemasok"),p(section.get("partner") or "Semua",bold)]]
        it=Table(info,colWidths=[available*.13,available*.17,available*.20,available*.50])
        it.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F3F7F8")),("BOX",(0,0),(-1,-1),.4,colors.HexColor("#C8D7DE")),
                                ("INNERGRID",(0,0),(-1,-1),.25,colors.HexColor("#D7E2E7")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(1,0),(1,-1),"RIGHT"),("ALIGN",(3,0),(3,-1),"RIGHT")]))
        opening=Table([[p("Saldo Awal",bold),p(f"{_ledger_money(section.get('saldo_awal')):,.0f}",bold)]],colWidths=[available*.85,available*.15])
        opening.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#E7F3F5")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("ALIGN",(1,0),(1,-1),"RIGHT")]))
        table=[[p(x,head) for x in ["Tanggal","No. Bukti","Keterangan","Partner","Referensi","Debit","Kredit","Saldo"]]]
        rows=list(section.get("rows") or [])
        if rows:
            for r in rows:
                table.append([p(r.get("tanggal")),p(r.get("nomor"),bold),p(r.get("keterangan")),p(r.get("partner")),p(r.get("referensi")),
                              p(f"{_ledger_money(r.get('debit')):,.0f}" if r.get("debit") else "-"),
                              p(f"{_ledger_money(r.get('kredit')):,.0f}" if r.get("kredit") else "-"),
                              p(f"{_ledger_money(r.get('saldo')):,.0f}",bold)])
        else:table.append([p("Tidak ada mutasi pada periode ini.")]+[p("") for _ in range(7)])
        t=Table(table,repeatRows=1,colWidths=widths)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#173F73")),("GRID",(0,0),(-1,-1),.3,colors.HexColor("#C8D7DE")),
                               ("VALIGN",(0,0),(-1,-1),"TOP"),("ALIGN",(5,1),(-1,-1),"RIGHT"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3)]))
        totals=[[p("Total Debit"),p(f"{_ledger_money(section.get('total_debit')):,.0f}",bold)],
                [p("Total Kredit"),p(f"{_ledger_money(section.get('total_kredit')):,.0f}",bold)],
                [p("Saldo Akhir"),p(f"{_ledger_money(section.get('saldo_akhir')):,.0f}",bold)]]
        tt=Table(totals,colWidths=[available*.22,available*.13],hAlign="RIGHT")
        tt.setStyle(TableStyle([("ALIGN",(1,0),(1,-1),"RIGHT"),("LINEBELOW",(0,0),(-1,-1),.3,colors.HexColor("#C8D7DE")),
                                ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#DDF2E7"))]))
        story.extend([it,Spacer(1,5),opening,Spacer(1,5),t,Spacer(1,6),tt,Spacer(1,14)])
    doc.build(story)
    return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")

def _pdf_money(value):
    try:value=float(value or 0)
    except Exception:value=0.0
    text=f"{abs(value):,.0f}".replace(",","X").replace(".",",").replace("X",".")
    return f"({text})" if value<0 else text

def _finance_income_pdf(data):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
    bio=io.BytesIO();doc=SimpleDocTemplate(bio,pagesize=A4,leftMargin=42,rightMargin=42,topMargin=34,bottomMargin=34)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("PsakTitle",parent=styles["Title"],fontSize=15,leading=18,alignment=1,textColor=colors.HexColor("#173F73"),spaceAfter=3)
    sub=ParagraphStyle("PsakSub",parent=styles["BodyText"],fontSize=8.5,alignment=1,textColor=colors.HexColor("#667788"),spaceAfter=14)
    section=ParagraphStyle("PsakSection",parent=styles["Heading3"],fontSize=9.5,leading=12,textColor=colors.HexColor("#173F73"),spaceBefore=9,spaceAfter=4)
    cell=ParagraphStyle("PsakCell",parent=styles["BodyText"],fontSize=8.5,leading=11)
    bold=ParagraphStyle("PsakBold",parent=cell,fontName="Helvetica-Bold")
    period=data.get("period") or {}; label=f"Periode {period.get('from') or '-'} s.d. {period.get('to') or '-'}"
    story=[Paragraph("LAPORAN LABA RUGI",title),Paragraph(label,sub)]
    rows=data.get("rows") or []; summary=data.get("summary") or {}
    groups=[("Pendapatan","PENDAPATAN","pendapatan",False),
            ("Harga Pokok Penjualan","HARGA POKOK PENJUALAN","hpp",True),
            ("Biaya Operasional","BEBAN OPERASIONAL","biaya_operasional",True)]
    available=A4[0]-84
    def add_group(key,heading,total_key,negative):
        story.append(Paragraph(heading,section))
        items=[x for x in rows if x.get("kelompok")==key]
        body=[]
        if items:
            for x in items:
                left=Paragraph(f"<font size='7'>{html.escape(str(x.get('kode') or ''))}</font>&nbsp;&nbsp;{html.escape(str(x.get('akun') or ''))}",cell)
                body.append([left,Paragraph(_pdf_money(x.get("jumlah")),cell)])
        else:body.append([Paragraph("Tidak ada saldo.",cell),Paragraph("-",cell)])
        t=Table(body,colWidths=[available*.76,available*.24])
        t.setStyle(TableStyle([("ALIGN",(1,0),(1,-1),"RIGHT"),("VALIGN",(0,0),(-1,-1),"TOP"),
                               ("BOTTOMPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),3)]))
        story.append(t)
        total=-(abs(float(summary.get(total_key) or 0))) if negative else float(summary.get(total_key) or 0)
        tt=Table([[Paragraph("Total "+heading,bold),Paragraph(_pdf_money(total),bold)]],colWidths=[available*.76,available*.24])
        tt.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),.5,colors.HexColor("#9FB4C1")),("ALIGN",(1,0),(1,0),"RIGHT"),
                                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F3F7F8")),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story.append(tt)
    add_group(*groups[0]);add_group(*groups[1])
    for label2,key in [("LABA KOTOR","laba_kotor")]:
        gt=Table([[Paragraph(label2,bold),Paragraph(_pdf_money(summary.get(key)),bold)]],colWidths=[available*.76,available*.24])
        gt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#E7F3F5")),("ALIGN",(1,0),(1,0),"RIGHT"),
                                ("BOX",(0,0),(-1,-1),.5,colors.HexColor("#A9C4CE")),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
        story.extend([Spacer(1,7),gt])
    add_group(*groups[2])
    gt=Table([[Paragraph("LABA BERSIH",bold),Paragraph(_pdf_money(summary.get("laba_bersih")),bold)]],colWidths=[available*.76,available*.24])
    gt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#DDF2E7")),("ALIGN",(1,0),(1,0),"RIGHT"),
                            ("BOX",(0,0),(-1,-1),.7,colors.HexColor("#7EAF93")),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    story.extend([Spacer(1,8),gt]);doc.build(story)
    return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")

def _finance_balance_pdf(data):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4,landscape
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
    bio=io.BytesIO();page=landscape(A4);doc=SimpleDocTemplate(bio,pagesize=page,leftMargin=28,rightMargin=28,topMargin=28,bottomMargin=28)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("BalTitle",parent=styles["Title"],fontSize=15,alignment=1,textColor=colors.HexColor("#173F73"),spaceAfter=3)
    sub=ParagraphStyle("BalSub",parent=styles["BodyText"],fontSize=8.5,alignment=1,textColor=colors.HexColor("#667788"),spaceAfter=12)
    small=ParagraphStyle("BalCell",parent=styles["BodyText"],fontSize=7.5,leading=9)
    bold=ParagraphStyle("BalBold",parent=small,fontName="Helvetica-Bold")
    rows=data.get("rows") or [];summary=data.get("summary") or {};period=data.get("period") or {}
    story=[Paragraph("NERACA",title),Paragraph(f"Per {period.get('to') or '-'}",sub)]
    assets=[x for x in rows if x.get("sisi")=="ASET"];rights=[x for x in rows if x.get("sisi")=="KEWAJIBAN & EKUITAS"]
    def column(title_text,items,total):
        content=[[Paragraph(title_text,bold),Paragraph("",bold)]]
        groups=[]
        for row in items:
            g=row.get("kelompok") or row.get("sisi") or "Lainnya"
            if g not in groups:groups.append(g)
        for g in groups:
            group_items=[x for x in items if (x.get("kelompok") or x.get("sisi") or "Lainnya")==g]
            content.append([Paragraph(g,bold),Paragraph("",bold)])
            for x in group_items:
                content.append([Paragraph(f"{html.escape(str(x.get('kode') or ''))}  {html.escape(str(x.get('akun') or ''))}",small),
                                Paragraph(_pdf_money(x.get("saldo")),small)])
            content.append([Paragraph("Jumlah "+g,bold),Paragraph(_pdf_money(sum(float(x.get("saldo") or 0) for x in group_items)),bold)])
        content.append([Paragraph("TOTAL "+title_text,bold),Paragraph(_pdf_money(total),bold)])
        t=Table(content,colWidths=[page[0]*.35,page[0]*.11])
        t.setStyle(TableStyle([("ALIGN",(1,0),(1,-1),"RIGHT"),("VALIGN",(0,0),(-1,-1),"TOP"),
                               ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DCEFF1")),
                               ("LINEBELOW",(0,-1),(-1,-1),.8,colors.HexColor("#173F73")),
                               ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        return t
    left=column("ASET",assets,summary.get("total_aset"))
    right=column("KEWAJIBAN & EKUITAS",rights,summary.get("total_kewajiban_ekuitas"))
    main=Table([[left,right]],colWidths=[(page[0]-56)*.5,(page[0]-56)*.5])
    main.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
    story.append(main);story.append(Spacer(1,10))
    balanced=bool(summary.get("balance"));status="NERACA SEIMBANG" if balanced else "NERACA TIDAK SEIMBANG"
    st=Table([[Paragraph(status,bold),Paragraph("Selisih "+_pdf_money(summary.get("selisih_neraca")),bold)]],colWidths=[(page[0]-56)*.7,(page[0]-56)*.3])
    st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#DDF2E7") if balanced else colors.HexColor("#FBE4E4")),
                            ("ALIGN",(1,0),(1,0),"RIGHT"),("BOX",(0,0),(-1,-1),.6,colors.HexColor("#7EAF93") if balanced else colors.HexColor("#C77A7A")),
                            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story.append(st);doc.build(story)
    return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")

def _finance_cashflow_pdf(data):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
    bio=io.BytesIO();doc=SimpleDocTemplate(bio,pagesize=A4,leftMargin=38,rightMargin=38,topMargin=32,bottomMargin=32)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("CfTitle",parent=styles["Title"],fontSize=15,alignment=1,textColor=colors.HexColor("#173F73"),spaceAfter=3)
    sub=ParagraphStyle("CfSub",parent=styles["BodyText"],fontSize=8.5,alignment=1,textColor=colors.HexColor("#667788"),spaceAfter=12)
    cell=ParagraphStyle("CfCell",parent=styles["BodyText"],fontSize=8,leading=10)
    bold=ParagraphStyle("CfBold",parent=cell,fontName="Helvetica-Bold")
    period=data.get("period") or {};rows=data.get("rows") or [];s=data.get("summary") or {};available=A4[0]-76
    story=[Paragraph("LAPORAN ARUS KAS",title),Paragraph(f"Metode Langsung - Periode {period.get('from') or '-'} s.d. {period.get('to') or '-'}",sub)]
    mapping=[("AKTIVITAS OPERASI","Aktivitas Operasi","aktivitas_operasi"),("AKTIVITAS INVESTASI","Aktivitas Investasi","aktivitas_investasi"),("AKTIVITAS PENDANAAN","Aktivitas Pendanaan","aktivitas_pendanaan")]
    for heading,key,total_key in mapping:
        story.append(Paragraph(heading,bold))
        items=[x for x in rows if x.get("aktivitas")==key]
        body=[]
        if items:
            for x in items:
                detail=f"{html.escape(str(x.get('uraian') or '-'))}<br/><font size='6'>{html.escape(str(x.get('tanggal') or ''))} - {html.escape(str(x.get('nomor') or ''))} - {html.escape(str(x.get('akun_lawan') or '-'))}</font>"
                body.append([Paragraph(detail,cell),Paragraph(_pdf_money(x.get("arus_bersih")),cell)])
        else:body.append([Paragraph("Tidak ada arus kas.",cell),Paragraph("-",cell)])
        t=Table(body,colWidths=[available*.77,available*.23]);t.setStyle(TableStyle([("ALIGN",(1,0),(1,-1),"RIGHT"),("VALIGN",(0,0),(-1,-1),"TOP")]))
        story.append(t)
        tt=Table([[Paragraph("Kas Bersih "+heading,bold),Paragraph(_pdf_money(s.get(total_key)),bold)]],colWidths=[available*.77,available*.23])
        tt.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),.5,colors.HexColor("#A7BAC4")),("ALIGN",(1,0),(1,0),"RIGHT"),("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F3F7F8"))]))
        story.extend([tt,Spacer(1,9)])
    rec=[("Saldo Awal Kas dan Setara Kas","saldo_awal_kas"),("Kenaikan / (Penurunan) Bersih Kas","kenaikan_penurunan_kas"),("Saldo Akhir Kas dan Setara Kas","saldo_akhir_kas")]
    rt=Table([[Paragraph(lbl,bold),Paragraph(_pdf_money(s.get(k)),bold)] for lbl,k in rec],colWidths=[available*.72,available*.28])
    rt.setStyle(TableStyle([("ALIGN",(1,0),(1,-1),"RIGHT"),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#C8D7DE")),
                            ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#DDF2E7")),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story.append(rt);doc.build(story)
    return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")



def _finance_table_pdf(data):
    """Clean preview-like PDF for tabular financial reports."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4,landscape
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
    page=landscape(A4);bio=io.BytesIO()
    doc=SimpleDocTemplate(bio,pagesize=page,leftMargin=24,rightMargin=24,topMargin=28,bottomMargin=28)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("FinTblTitle",parent=styles["Title"],fontSize=14,alignment=1,textColor=colors.HexColor("#173F73"),spaceAfter=3)
    sub=ParagraphStyle("FinTblSub",parent=styles["BodyText"],fontSize=8,alignment=1,textColor=colors.HexColor("#667788"),spaceAfter=12)
    cell=ParagraphStyle("FinTblCell",parent=styles["BodyText"],fontSize=7,leading=8.5)
    head=ParagraphStyle("FinTblHead",parent=cell,fontName="Helvetica-Bold",textColor=colors.white)
    story=[Paragraph(html.escape(str(data.get("title") or "Laporan Keuangan")),title)]
    period=data.get("period") or {}
    if period.get("from") or period.get("to"):
        story.append(Paragraph(f"Periode {period.get('from') or '-'} s.d. {period.get('to') or '-'}",sub))
    cols=list(data.get("columns") or [])
    keys=[x[0] for x in cols]
    labels=[x[1] for x in cols]
    rows=list(data.get("rows") or [])
    if not cols:
        story.append(Paragraph("Tidak ada kolom laporan.",cell))
    else:
        weights=[]
        for key,label in cols:
            k=str(key).lower()
            if any(x in k for x in ("keterangan","uraian","partner","pelanggan","pemasok","akun")):weights.append(2.0)
            elif any(x in k for x in ("debit","credit","kredit","saldo","jumlah","total","penerimaan","pengeluaran","amount")):weights.append(1.15)
            elif "tanggal" in k or "date" in k:weights.append(1.05)
            else:weights.append(1.0)
        avail=page[0]-48;scale=avail/sum(weights);widths=[x*scale for x in weights]
        table_data=[[Paragraph(html.escape(str(x)),head) for x in labels]]
        for row in rows:
            cells=[]
            for key in keys:
                val=row.get(key,"")
                if isinstance(val,(int,float)) and any(x in str(key).lower() for x in ("debit","credit","kredit","saldo","jumlah","total","penerimaan","pengeluaran","amount")):
                    txt=_pdf_money(val)
                else:txt=html.escape(str(val if val not in (None,"") else "-"))
                cells.append(Paragraph(txt,cell))
            table_data.append(cells)
        t=Table(table_data,colWidths=widths,repeatRows=1)
        numeric_cols=[i for i,k in enumerate(keys) if any(x in str(k).lower() for x in ("debit","credit","kredit","saldo","jumlah","total","penerimaan","pengeluaran","amount"))]
        style=[("BACKGROUND",(0,0),(-1,0),colors.HexColor("#184A82")),("VALIGN",(0,0),(-1,-1),"TOP"),
               ("GRID",(0,0),(-1,-1),.25,colors.HexColor("#C8D5DF")),
               ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
               ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F7FAFC")])]
        for ci in numeric_cols:style.append(("ALIGN",(ci,1),(ci,-1),"RIGHT"))
        t.setStyle(TableStyle(style));story.append(t)
    summary=_export_summary_items(data.get("summary"))
    if summary:
        story.append(Spacer(1,10))
        body=[[Paragraph(str(k).replace("_"," ").title(),cell),Paragraph(_pdf_money(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else html.escape(str(v)),cell)] for k,v in summary]
        st=Table(body,colWidths=[(page[0]-48)*.75,(page[0]-48)*.25])
        st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#EFF5F7")),("GRID",(0,0),(-1,-1),.25,colors.HexColor("#C7D7DF")),
                                ("ALIGN",(1,0),(1,-1),"RIGHT"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        story.append(st)
    doc.build(story)
    return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")


def export_report(kind,fmt,filters,include_cost=True):
    data=report_data(kind,filters)
    if kind in ("finance_income","finance_balance","finance_ledger","finance_cashflow"):
        data=dict(data)
        data["period"]={"from":str(filters.get("date_from") or "")[:10] or None,
                        "to":str(filters.get("date_to") or "")[:10] or None}
    if not include_cost:
        data=redact_cost_data(data)
    fmt=str(fmt or '').lower().strip()
    if kind=="finance_ledger":
        if fmt=="xlsx":return _export_finance_ledger_xlsx(data)
        if fmt=="pdf":return _export_finance_ledger_pdf(data)
    if fmt=="pdf" and kind=="finance_income":return _finance_income_pdf(data)
    if fmt=="pdf" and kind=="finance_balance":return _finance_balance_pdf(data)
    if fmt=="pdf" and kind=="finance_cashflow":return _finance_cashflow_pdf(data)
    if fmt=="pdf" and kind in ("finance_journal","finance_trial","finance_receivables","finance_payables"):
        return _finance_table_pdf(data)
    if fmt=="xlsx":
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font,PatternFill,Alignment
        except ImportError as exc:raise ValueError("Ekspor Excel membutuhkan openpyxl.") from exc
        wb=Workbook();ws=wb.active;ws.title="Laporan"
        ws.append([str(data.get("title") or "Laporan")]);ws["A1"].font=Font(size=16,bold=True)
        ws.append([])
        columns=list(data.get("columns") or [])
        headers=[label for _,label in columns];keys=[key for key,_ in columns]
        ws.append(headers)
        for cell in ws[3]:
            cell.font=Font(bold=True);cell.fill=PatternFill("solid",fgColor="DCEFF1");cell.alignment=Alignment(vertical="top",wrap_text=True)
        for row in (data.get("rows") or []):
            ws.append([_export_scalar(row.get(k,"")) for k in keys])
        summary_items=_export_summary_items(data.get("summary"))
        if summary_items:
            ws.append([]);ws.append(["RINGKASAN"]);ws.cell(ws.max_row,1).font=Font(bold=True)
            for k,v in summary_items:
                ws.append([str(k).replace("_"," ").title(),_export_scalar(v)])
        # Keep wide/long reports usable and prevent pathological content from
        # creating excessively wide Excel columns.
        for col in ws.columns:
            letter=col[0].column_letter
            max_len=0
            for c in col:
                text=str(c.value or "")
                if len(text)>120:text=text[:120]
                max_len=max(max_len,max((len(line) for line in text.splitlines()),default=0))
                c.alignment=Alignment(vertical="top",wrap_text=True)
            ws.column_dimensions[letter].width=min(45,max(10,max_len+2))
        if headers:
            ws.freeze_panes="A4";ws.auto_filter.ref=f"A3:{ws.cell(3,len(headers)).coordinate}"
        bio=io.BytesIO();wb.save(bio)
        return bio.getvalue(),"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",_safe_filename(data.get("title"),"xlsx")
    if fmt=="pdf":
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4,landscape
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
        except ImportError as exc:raise ValueError("Ekspor PDF membutuhkan reportlab.") from exc
        bio=io.BytesIO();page=landscape(A4);left=18;right=18
        doc=SimpleDocTemplate(bio,pagesize=page,leftMargin=left,rightMargin=right,topMargin=18,bottomMargin=18)
        styles=getSampleStyleSheet();story=[Paragraph(html.escape(str(data.get("title") or "Laporan")),styles["Title"]),Spacer(1,10)]
        columns=list(data.get("columns") or []);keys=[k for k,_ in columns]
        col_count=max(1,len(columns));font_size=5 if col_count>12 else (6 if col_count>8 else 7)
        cell_style=ParagraphStyle("ReportCell",parent=styles["BodyText"],fontSize=font_size,leading=font_size+1,spaceAfter=0,spaceBefore=0)
        head_style=ParagraphStyle("ReportHead",parent=cell_style,fontName="Helvetica-Bold")
        def para(value,style=cell_style):
            text=str(_export_scalar(value))
            text=html.escape(text).replace("\n","<br/>")
            return Paragraph(text,style)
        table=[[para(label,head_style) for _,label in columns]] if columns else [[para("Data",head_style)]]
        if columns:
            for r in (data.get("rows") or []):table.append([para(r.get(k,"")) for k in keys])
        elif not (data.get("rows") or []):
            table.append([para("Tidak ada data")])
        available=page[0]-left-right
        col_widths=[available/col_count]*col_count
        t=Table(table,repeatRows=1,colWidths=col_widths,hAlign="LEFT")
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DCEFF1")),
          ("GRID",(0,0),(-1,-1),0.35,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),
          ("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2),
          ("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2)]))
        story.append(t)
        summary_items=_export_summary_items(data.get("summary"))
        if summary_items:
            story.append(Spacer(1,10));story.append(Paragraph("Ringkasan",styles["Heading2"]))
            summary=[[para(str(k).replace("_"," ").title()),para(v)] for k,v in summary_items]
            st=Table(summary,colWidths=[available*0.35,available*0.65],hAlign="LEFT")
            st.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.35,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP")]))
            story.append(st)
        doc.build(story)
        return bio.getvalue(),"application/pdf",_safe_filename(data.get("title"),"pdf")
    raise ValueError("Format ekspor harus xlsx atau pdf.")

