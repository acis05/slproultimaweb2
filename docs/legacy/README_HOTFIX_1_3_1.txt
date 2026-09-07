STOKLEDGER PRO v1.3.1 - DASHBOARD VISIBILITY HOTFIX

Perbaikan:
- Seluruh blok Analitik Bulan Ini, grafik, reminder jatuh tempo, stok minimum, dan dead stock berada di dalam halaman Dashboard.
- Saat membuka menu lain, seluruh elemen Dashboard ikut disembunyikan.
- Tidak ada perubahan database atau logika transaksi.
- Smoke test memiliki pemeriksaan struktur UI agar bug ini tidak berulang.

Cara update:
1. Backup data\stokledger_pro.db.
2. Ekstrak paket ke folder baru.
3. Salin database lama ke folder data.
4. Jalankan TEST_SERVER.bat lalu START_SERVER.bat.
5. Tekan Ctrl+F5 di browser.
