StokLedger Owner Cloud v1.18.1

Tambahan:
- Pendaftaran akun owner menggunakan kode pairing 6 digit.
- Login/logout owner dengan sesi 30 hari.
- Password disimpan menggunakan PBKDF2-SHA256 dengan salt unik.
- Relasi owner ke perusahaan dan dukungan multi-company dasar.
- Dashboard mobile responsif dan PWA manifest dasar.
- Endpoint dashboard tidak lagi digunakan secara publik; dashboard owner memerlukan token login.
- Dukungan DATABASE_URL Railway postgresql:// dan postgres:// melalui psycopg 3.

Deploy ulang folder owner_cloud_railway ke repository GitHub Railway.
Setelah deployment aktif:
1. Buat kode pairing baru dari desktop.
2. Buka domain Railway.
3. Isi kode, nama owner, email, dan password minimal 8 karakter.
4. Klik Hubungkan dan masuk.
5. Jalankan Sinkronkan Sekarang dari desktop agar dashboard memiliki data terbaru.
