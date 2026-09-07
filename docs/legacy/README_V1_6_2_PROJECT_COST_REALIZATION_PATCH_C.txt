STOKLEDGER PRO v1.6.2 — PROJECT COST REALIZATION PATCH C
==========================================================

REALISASI MATERIAL
- Tetap dihitung dari Pengeluaran Material Proyek.
- Menggunakan nilai average cost historis transaksi material.

REALISASI BIAYA PROYEK
- Dihitung dari journal_lines yang memiliki project_id.
- Akun yang dihitung: account_type EXPENSE atau subtype HPP.
- Sumber dapat berasal dari Kas Masuk/Keluar, Pembelian langsung ke
  akun biaya, Penjualan/HPP, dan Jurnal Manual.
- Nilai dihitung net Debit dikurangi Kredit.
- Jurnal source_type PROJECT_MATERIAL_ISSUE dikecualikan agar material
  tidak dihitung dua kali.

KONTROL BUDGET
- Budget Material vs Realisasi Material.
- Budget Biaya vs Realisasi Biaya.
- Sisa budget per komponen.
- Persentase pemakaian per komponen dan total.
- Rincian jurnal sumber Realisasi Biaya dapat dilihat dari halaman budget.

CATATAN
- Akun Aset Proyek tidak masuk Budget Biaya pada Patch C.
- Filter laporan dan ekspor laporan proyek belum ditambahkan.