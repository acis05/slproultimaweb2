StokLedger Pro Ultima v1.13.7 - DATABASE MANAGER REDESIGN

- Database Manager native selalu tampil sebelum server dijalankan.
- Tiga pilihan: Buat Database Baru, Buka Database, Gunakan Terakhir.
- Server berjalan sebagai child process dengan path database eksplisit.
- Server tidak boleh fallback diam-diam ke database default.
- Tombol Ganti Database menutup child server dan kembali ke Database Manager.
- Database terakhir hanya dipakai saat pengguna menekan Gunakan Terakhir.
