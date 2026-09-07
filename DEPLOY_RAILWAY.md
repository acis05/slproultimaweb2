# Deploy / Update StokLedger Web v1.3.0 di Railway

1. Replace source repo lokal dengan isi ZIP v1.3.0, tetapi jangan hapus folder `.git`.
2. Dari terminal VS Code:
```bash
git add .
git commit -m "Upgrade StokLedger Web v1.3.0 SaaS admin and trial signup"
git push
```
3. Railway akan redeploy dari GitHub.
4. Pastikan service aplikasi memiliki Variable:
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
STOKLEDGER_WEB_MODE=1
STOKLEDGER_ADMIN_PASSWORD=<minimal 8 karakter>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci tenant>
STOKLEDGER_OWNER_ADMIN_PASSWORD=<password owner pusat>
STOKLEDGER_TOKEN_HOURS=12
```
5. Setelah deploy, buka `/api/health`. Pastikan `database_backend` = `postgresql`.
6. Buka `/` untuk membuat akun trial baru.
7. Buka `/owner-admin` untuk kontrol seluruh trial/langganan dan kode diskon.

## Penting
- Jangan menghapus PostgreSQL Railway saat update.
- Password Owner Admin jangan diberikan ke pelanggan.
- Account trial baru menggunakan schema PostgreSQL tenant terpisah.
