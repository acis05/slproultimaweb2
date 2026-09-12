# StokLedger Online v1.4.3

## Update v1.4.3 — UI status lebih sederhana
- Sidebar tidak lagi menampilkan versi internal, port server, status lisensi teknis, atau jumlah hak akses.
- Status koneksi cukup tampil **Online**.
- Badge trial sekarang selalu menjelaskan paket awal **Trial 7 hari**, lalu menampilkan sisa hari aktual. Contoh: `Trial 7 hari · sisa 3 hari · 2 user`.
- Seluruh fitur v1.4.2 tetap dipertahankan: role-aware UI, multi-tab, security hardening, Owner 2FA, dan password recovery.

## Railway Variables
```text
STOKLEDGER_WEB_MODE=1
DATABASE_URL=${{Postgres.DATABASE_URL}}
STOKLEDGER_ADMIN_PASSWORD=<password bootstrap>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci aktivasi>
STOKLEDGER_TOKEN_HOURS=8
STOKLEDGER_OWNER_ADMIN_PASSWORD=<minimal 12 karakter>
STOKLEDGER_OWNER_TOTP_SECRET=<secret TOTP>
STOKLEDGER_ALLOWED_ORIGINS=https://DOMAIN-PRODUKSI-ANDA
```
