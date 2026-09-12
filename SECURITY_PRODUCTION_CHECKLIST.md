# StokLedger Online — Production Security Checklist

Selesaikan checklist ini sebelum menerima pelanggan berbayar.

- [ ] Custom domain HTTPS aktif.
- [ ] `DATABASE_URL` menggunakan PostgreSQL Railway private service reference.
- [ ] Public/TCP database access dimatikan bila tidak diperlukan.
- [ ] `STOKLEDGER_OWNER_ADMIN_PASSWORD` minimal 12 karakter dan unik.
- [ ] `STOKLEDGER_OWNER_TOTP_SECRET` aktif dan tersimpan di Authenticator pemilik.
- [ ] `STOKLEDGER_ALLOWED_ORIGINS` hanya berisi domain production yang sah.
- [ ] Backup PostgreSQL Railway terjadwal aktif.
- [ ] Backup offsite / `pg_dump` diuji dan dapat direstore.
- [ ] Staging memakai database terpisah dari production.
- [ ] GitHub repository private dan tidak menyimpan `.env`/secret.
- [ ] Security Audit Owner Admin menunjukkan event login/signup.
- [ ] Uji brute-force: 5 password salah memicu blok sementara.
- [ ] Uji tenant isolation perusahaan A vs perusahaan B.
- [ ] Uji role user biasa tidak dapat membuka endpoint admin/accounting tanpa permission.
- [ ] Uji transaksi inti dan laporan setelah upgrade.
- [ ] Cloudflare/WAF/rate protection eksternal aktif bila digunakan.

## Password recovery
- User biasa: reset oleh Administrator perusahaan.
- Administrator utama tenant: reset oleh Owner Admin setelah verifikasi pelanggan.
- Password sementara wajib diganti pada login berikutnya.
- Jangan pernah mereset password hanya berdasarkan permintaan email/WhatsApp tanpa verifikasi identitas pelanggan.
