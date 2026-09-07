StokLedger Pro Ultima v1.13.6 - DATABASE SELECTOR FINAL FIX

Perbaikan:
- Buat Database Baru langsung memakai file baru yang dipilih.
- Buka/Ganti Database tidak lagi kembali ke database default atau database lama.
- Perpindahan database merestart proses aplikasi secara bersih agar seluruh modul membaca DB_PATH baru.
- Lokasi database aktif disimpan secara atomik di database_selection.json khusus edisi StokLedger Pro Ultima.
- Aplikasi memvalidasi bahwa DB_PATH server sama persis dengan pilihan pengguna sebelum server berjalan.
- Jika file pilihan tidak valid/hilang, aplikasi menampilkan error dan tidak diam-diam membuka database default.

Build: BUILD_INSTALLER_WINDOWS.bat
