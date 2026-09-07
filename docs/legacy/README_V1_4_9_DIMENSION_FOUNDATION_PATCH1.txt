STOKLEDGER PRO v1.4.9 — DEPARTEMEN & PROYEK FOUNDATION PATCH 1
================================================================

Patch ini hanya menambahkan fondasi database dan backend.

KOLOM BARU
- sales.department_id / project_id
- purchases.department_id / project_id
- cash_transactions.department_id / project_id
- inventory_transactions.department_id / project_id
- journal_entries.department_id / project_id
- journal_lines.department_id / project_id

MIGRASI
- Database v1.4.8 otomatis ditambah kolom saat server dijalankan.
- Semua kolom nullable sehingga data transaksi lama tetap kompatibel.

BACKEND
- API Penjualan, Pembelian, Kas Masuk/Keluar, Penyesuaian Stok,
  dan Jurnal Manual sudah menerima department_id dan project_id.
- Departemen dan proyek divalidasi harus aktif.
- Dimensi disimpan pada header transaksi dan journal_entries.
- Kolom journal_lines sudah tersedia untuk Patch 3 (posting per baris).

BELUM DIUBAH
- Form/UI transaksi.
- Filter laporan.
- Dashboard, routing, dan menu.
