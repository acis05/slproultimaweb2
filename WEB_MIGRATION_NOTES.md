# StokLedger Web v1.3.3 SaaS Migration Notes

- Melanjutkan seluruh fitur PostgreSQL v1.2.1.
- Menambah registry SaaS pada schema `public` untuk akun pelanggan, sesi tenant, Owner Admin, dan kode diskon.
- Pendaftaran trial membuat schema PostgreSQL baru `tenant_<random>` untuk setiap pelanggan.
- Login email akan diarahkan ke schema tenant yang sesuai.
- Sesi aplikasi dipetakan ke tenant sehingga query bisnis tetap memakai repository lama tetapi search_path PostgreSQL diisolasi per akun.
- Owner Admin tersedia di `/owner-admin` dan memakai `STOKLEDGER_OWNER_ADMIN_PASSWORD`.
- Aktivasi Owner menyinkronkan status paket ke tabel subscription di tenant.
- Kode diskon dapat berupa persen atau nominal, dibatasi masa berlaku, kuota, dan paket.
