STOKLEDGER PRO v1.5.1 — DEPARTEMEN & PROYEK JOURNAL LINES PATCH 3
===================================================================
- Penjualan, Pembelian, Kas Masuk/Keluar, dan Penyesuaian Stok
  menyimpan Departemen/Proyek pada setiap journal_lines.
- Jurnal Manual menyimpan dimensi per baris.
- Baris tanpa dimensi memakai dimensi header jika ada.
- Jika header dan baris kosong, nilai tetap NULL.
- Departemen/Proyek wajib aktif.
- Data lama tetap kompatibel.
- Filter laporan per dimensi belum ditambahkan.