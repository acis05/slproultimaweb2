# Deploy StokLedger Online v1.4.2 Production Security Edition

## 1. Update GitHub dari VS Code

Replace source lama dengan isi source v1.4.2. Jangan hapus folder `.git`.

```bash
git add .
git commit -m "Upgrade StokLedger Online v1.4.2 production security"
git push
```

Railway akan redeploy otomatis.

## 2. Variables aplikasi

Pastikan service aplikasi memiliki:

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
STOKLEDGER_WEB_MODE=1
STOKLEDGER_ADMIN_PASSWORD=<password bootstrap>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci aktivasi>
STOKLEDGER_TOKEN_HOURS=8
STOKLEDGER_OWNER_ADMIN_PASSWORD=<minimal 12 karakter>
STOKLEDGER_OWNER_TOTP_SECRET=<secret TOTP base32>
STOKLEDGER_ALLOWED_ORIGINS=https://DOMAIN-PRODUKSI-ANDA
```

Jangan isi domain Railway sementara pada `STOKLEDGER_ALLOWED_ORIGINS` bila Anda ingin browser hanya menggunakan domain produksi. Bila masih perlu staging, gunakan domain staging terpisah atau daftar beberapa origin dipisahkan koma.

## 3. Siapkan 2FA Owner Admin

Di komputer lokal source:

```bash
python scripts/generate_owner_totp.py
```

Simpan secret ke Railway, lalu masukkan URI yang dicetak script ke aplikasi Authenticator. Setelah redeploy, `/owner-admin` meminta **password + kode 6 digit**.

## 4. PostgreSQL dan backup

- Jangan hapus service PostgreSQL saat redeploy.
- Hindari Public TCP Proxy untuk database bila tidak diperlukan.
- Aktifkan backup terjadwal pada PostgreSQL Railway.
- Simpan backup/`pg_dump` berkala di storage terpisah dari Railway.

## 5. Staging

Buat Railway project/environment terpisah untuk staging dengan PostgreSQL staging sendiri. Jangan pernah menguji migrasi/source baru langsung pada database pelanggan production.

## 6. Verifikasi sesudah deploy

- `/api/health` harus `status: ok` dan `database_backend: postgresql`.
- Login tenant lama dan tenant baru.
- Test 5 password salah: login harus dibatasi sementara.
- Test Owner Admin: password saja tidak cukup; OTP wajib.
- Buka Owner Admin → Security Audit dan pastikan event login terlihat.
- Uji akun perusahaan A tidak dapat mengakses data perusahaan B.
- Test transaksi Penjualan → Inventory → GL → Laporan.

## 7. Cloudflare (disarankan)

Arahkan domain produksi melalui Cloudflare dan aktifkan proxy/WAF/rate protection sesuai kebutuhan. Aplikasi tetap melakukan rate-limit sendiri sebagai lapisan tambahan.
