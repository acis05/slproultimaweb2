# StokLedger Pro Ultima Web v1.3.2 — SaaS PostgreSQL Edition

## v1.3.2 hotfix

- Memperbaiki login akun trial PostgreSQL yang sebelumnya dapat berakhir dengan `Kesalahan internal server` saat response mengandung nilai `NUMERIC/Decimal`.
- Memperbaiki API Owner Admin (akun, status, aktivasi, dan kode diskon) dengan serializer JSON PostgreSQL-safe.
- Menghapus tautan Owner Admin dari halaman login publik. Owner Admin tetap tersedia hanya melalui URL `/owner-admin`.


Build ini melanjutkan v1.2.1 PostgreSQL dengan fitur SaaS account management.

## Fitur baru
- Landing/login Web baru yang berbeda dari Desktop.
- Pendaftaran akun trial mandiri: 7 hari / maksimal 2 user.
- Setiap akun trial baru menggunakan schema PostgreSQL terisolasi (`tenant_*`).
- Owner Admin di `/owner-admin` untuk melihat akun trial/langganan.
- Owner dapat reset trial, suspend/aktifkan akun, dan aktivasi paket.
- Kode diskon langganan: persen atau nominal, periode berlaku, batas pemakaian, paket tertentu.
- Paket 6 bulan: Rp1.200.000 / 2 user; add-on Rp100.000/user.
- Paket 1 tahun: Rp2.000.000 / 2 user; add-on Rp200.000/user.
- Mobile UI fix v1.2.1 tetap dipertahankan.

## Railway Variables wajib
```
STOKLEDGER_WEB_MODE=1
DATABASE_URL=${{Postgres.DATABASE_URL}}
STOKLEDGER_ADMIN_PASSWORD=<bootstrap password minimal 8 karakter>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci aktivasi tenant>
STOKLEDGER_OWNER_ADMIN_PASSWORD=<password khusus /owner-admin>
STOKLEDGER_TOKEN_HOURS=12
```

`STOKLEDGER_OWNER_ADMIN_PASSWORD` wajib dirahasiakan karena dapat mengontrol seluruh akun SaaS.

## URL
- Aplikasi / pendaftaran trial: `/`
- Owner Admin: `/owner-admin`
- Health check: `/api/health`

## Catatan database
Akun baru dibuat dalam schema PostgreSQL terpisah agar data antar pelanggan tidak tercampur. Jangan menghapus service PostgreSQL Railway saat redeploy.
