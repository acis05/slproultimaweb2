STOKLEDGER PRO SERVER CORE v1.1.3 - TRANSACTION MASTER BINDING HOTFIX
============================================================================

PERBAIKAN
- Dropdown akun kas/bank pada Penjualan, Pembelian, Terima Piutang, dan Bayar Hutang.
- Dropdown Barang/Jasa pada Pembelian dan Penjualan tidak lagi mengikuti filter Data Barang.
- Data transaksi selalu mengambil seluruh master aktif dari server.
- Pilihan dropdown dipertahankan saat Refresh.
- Pesan jelas bila akun kas/bank atau barang belum tersedia.
- Validasi transaksi tunai/transfer wajib memiliki akun kas/bank.
- Tidak ada perubahan struktur database.

CARA UPDATE
1. Tutup server versi lama.
2. Backup data\stokledger_pro.db.
3. Ekstrak v1.1.3 ke folder baru.
4. Salin database lama ke folder data.
5. Jalankan TEST_SERVER.bat.
6. Jalankan START_SERVER.bat.
7. Tekan Ctrl+F5 pada browser.
