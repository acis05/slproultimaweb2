StokLedger v1.17.4

- Master Data > Daftar Nama Gudang dengan CRUD, default, aktif/nonaktif.
- Gudang yang sudah dipakai transaksi dinonaktifkan, bukan dihapus permanen.
- Trial dibatasi maksimal 2 device/browser aktif.
- Device ID tersimpan di localStorage browser; tab dalam browser yang sama memakai satu slot.
- Logout membebaskan slot. Sesi trial tanpa aktivitas 30 menit dibersihkan.
