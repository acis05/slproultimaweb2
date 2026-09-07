StokLedger v1.15.3

- Hapus transaksi Kas Masuk/Keluar hasil Smart Import memakai posted_transaction_id.
- Saldo kas dibalik langsung dari nilai database, bukan dari teks tampilan.
- bank_import_rows menjadi VOID dan jurnal BANK_IMPORT ikut dibatalkan.
- Transaksi asli dan reversal internal hilang dari daftar aktif.
- Buku Besar Semua Akun tidak lagi menampilkan sections: [object Object].
- Ringkasan laporan PSAK dirender pada layout laporan, bukan panel summary generik.
