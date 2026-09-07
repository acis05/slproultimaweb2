STOKLEDGER PRO v1.2.3 - SMOKE TEST RESET HOTFIX
=================================================

PENYEBAB BUG
- Folder test_data dari pengujian sebelumnya tidak dibersihkan.
- Setiap pengujian menambahkan jurnal baru.
- Assertion mengharapkan satu jurnal Rp100.000 sehingga tes berikutnya gagal.

PERBAIKAN
- test_data dan test_logs dihapus otomatis sebelum smoke test.
- Port test tetap dipilih otomatis.
- Versi health check, tester, dan judul disamakan ke 1.2.3.
- Database produksi di folder data tidak pernah disentuh oleh tester.

CARA PAKAI
1. Ekstrak ke folder baru.
2. Salin data\stokledger_pro.db lama ke folder data bila diperlukan.
3. Jalankan TEST_SERVER.bat.
4. Setelah berhasil, jalankan START_SERVER.bat.
