StokLedger Pro Ultima v1.9.9 - DATABASE SELECTOR

Perubahan:
- Layar pemilihan database tampil sebelum halaman login.
- Tombol Buat Database Baru membuat database perusahaan baru tanpa menimpa file lama.
- Tombol Buka Database membuka database SQLite StokLedger yang sudah ada.
- Tombol Gunakan Terakhir tersedia jika database terakhir masih ditemukan.
- Lokasi database aktif disimpan di database_selection.json pada folder data aplikasi.
- Auto backup saat aplikasi ditutup tetap aktif untuk database yang sedang dipilih.

Catatan keamanan:
- File yang dibuka diverifikasi sebagai SQLite.
- Database baru hanya diinisialisasi setelah pengguna memilih nama file yang belum ada.
