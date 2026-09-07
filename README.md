# StokLedger Pro Ultima Web v1.2.1 — PostgreSQL Edition

Versi web ini menggunakan **PostgreSQL sebagai database utama** dan ditujukan untuk deployment Railway. Basis fitur tetap berasal dari StokLedger Pro Ultima Desktop v1.22.55 + Web v1.1.1.

## Fitur Web
- UI mobile-friendly.
- Trial 7 hari / 2 user.
- Admin Trial & Langganan.
- Paket 6 bulan Rp1.200.000 / 2 user.
- Paket 1 tahun Rp2.000.000 / 2 user.
- Add-on user Rp100.000 / 6 bulan atau Rp200.000 / 1 tahun.
- PostgreSQL melalui `DATABASE_URL`.
- Dokumen Proyek dan logo perusahaan disimpan di PostgreSQL, sehingga tidak membutuhkan Railway Volume untuk file tersebut.
- Health check `/api/health`.

## Railway
Buat service PostgreSQL di Railway, lalu pada service aplikasi tambahkan reference variable:

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Nama `Postgres` harus mengikuti nama service PostgreSQL Anda.

Tambahkan juga:

```text
STOKLEDGER_WEB_MODE=1
STOKLEDGER_ADMIN_PASSWORD=GANTI_PASSWORD_KUAT
STOKLEDGER_LICENSE_ADMIN_KEY=GANTI_KUNCI_ADMIN_AKTIVASI
STOKLEDGER_TOKEN_HOURS=12
```

Tidak perlu `STOKLEDGER_DB_PATH` dan tidak wajib membuat Volume `/data` untuk database.

Lihat `DEPLOY_RAILWAY.md` untuk langkah lengkap.

## Catatan migrasi
Build ini membuat schema PostgreSQL baru secara otomatis pada startup pertama. Jangan arahkan Web v1.2.1 ke database produksi PostgreSQL yang sudah berisi schema lain.

Database SQLite Desktop/Web lama **tidak otomatis diimpor** ke PostgreSQL pada build ini. Bila perlu memindahkan data lama, lakukan migrasi terkontrol setelah backup dan verifikasi laporan akuntansi/persediaan.
