STOKLEDGER PRO SERVER CORE v1.2.3 - UI & TEST HOTFIX
====================================================

PERBAIKAN
- Menyamakan versi /api/health, log server, dan smoke test.
- Tester tidak lagi menunggu versi 1.2.0 saat server sudah 1.2.x.
- Judul TEST_SERVER diperbarui.
- Modern Sidebar UI v1.2.1 tetap dipertahankan.
- Tidak ada perubahan database atau logika transaksi.

CARA MIGRASI
1. Tutup server versi sebelumnya.
2. Backup data\stokledger_pro.db.
3. Salin database lama ke folder data versi ini.
4. Jalankan TEST_SERVER.bat.
5. Jalankan START_SERVER.bat.
6. Tekan Ctrl+F5 di browser.
