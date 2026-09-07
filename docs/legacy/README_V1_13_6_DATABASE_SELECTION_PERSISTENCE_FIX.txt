StokLedger Pro Ultima v1.13.6

PERBAIKAN DATABASE AKTIF
- database_selection.json menjadi fallback resmi pada server/config.py.
- Database pilihan tidak lagi kembali diam-diam ke database default.
- Prioritas DB: STOKLEDGER_DB_PATH -> database_selection.json -> database default.
- Dialog Buka/Ganti Database dipaksa tampil di depan browser.
- Penulisan database_selection.json diverifikasi setelah disimpan.
- Database aktif pada halaman login mengikuti DB_PATH server yang sebenarnya.
