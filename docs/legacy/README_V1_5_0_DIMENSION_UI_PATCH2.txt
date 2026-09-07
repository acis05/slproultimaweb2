STOKLEDGER PRO v1.5.0 — DEPARTEMEN & PROYEK UI PATCH 2
========================================================

FIELD BARU PADA FORM
- Penjualan: Departemen dan Proyek.
- Pembelian: Departemen dan Proyek.
- Kas Masuk/Keluar: Departemen dan Proyek.
- Penyesuaian Stok: Departemen dan Proyek.
- Jurnal Manual: Departemen dan Proyek per baris jurnal.

PERILAKU
- Dropdown hanya mengambil Master Departemen/Proyek yang aktif.
- Semua pilihan bersifat opsional.
- Penjualan, Pembelian, Kas, dan Adjustment mengirim department_id
  dan project_id ke backend.
- Pilihan dimensi direset setelah transaksi berhasil.
- Jurnal Manual sudah membawa department_id/project_id di payload
  masing-masing baris, tetapi penyimpanan ke journal_lines baru
  diaktifkan pada Patch 3.

TIDAK DIUBAH
- Posting dimensi ke baris jurnal.
- Filter laporan.
- Dashboard.
- Routing dan menu inti.
- Perhitungan transaksi.