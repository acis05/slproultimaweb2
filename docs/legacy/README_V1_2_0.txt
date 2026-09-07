STOKLEDGER PRO SERVER CORE v1.2.0 - BUKU BESAR & NERACA SALDO
================================================================

FITUR BARU
- Buku Besar per akun
- Filter tanggal mulai dan tanggal akhir
- Saldo awal sebelum periode
- Mutasi debit dan kredit periode
- Saldo berjalan setiap baris jurnal
- Saldo akhir akun
- Neraca Saldo dengan saldo awal, mutasi, dan saldo akhir
- Indikator SEIMBANG / TIDAK SEIMBANG
- Tombol Refresh tanpa reload halaman
- API: /api/general-ledger dan /api/trial-balance

MIGRASI
1. Tutup server v1.1.3.
2. Backup data\stokledger_pro.db.
3. Salin database ke folder data versi ini.
4. Jalankan TEST_SERVER.bat.
5. Jalankan START_SERVER.bat.
6. Tekan Ctrl+F5 pada browser.

Tidak ada perubahan destruktif pada database.
