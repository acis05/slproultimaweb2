# Deploy StokLedger Pro Ultima Web v1.2.1 PostgreSQL ke Railway

## 1. Push source ke GitHub
Replace source v1.1.1 di folder repo lokal dengan isi source v1.2.1 ini, tetapi jangan hapus folder `.git`. Commit lalu Push dari VS Code.

## 2. PostgreSQL Railway
Jika service PostgreSQL sudah dibuat, biarkan tetap ada. Jika belum:
- Railway Project → New → Database → PostgreSQL.

## 3. Hubungkan aplikasi ke PostgreSQL
Buka service **StokLedger Web → Variables** dan tambahkan:

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Jika nama service database bukan `Postgres`, ganti nama pada reference variable sesuai nama service Anda.

Tambahkan:

```text
STOKLEDGER_WEB_MODE=1
STOKLEDGER_ADMIN_PASSWORD=<password-admin-minimal-8-karakter>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci-rahasia-aktivasi-minimal-8-karakter>
STOKLEDGER_TOKEN_HOURS=12
```

Jangan isi `STOKLEDGER_DB_PATH` untuk PostgreSQL edition.

## 4. Deploy
Push ke GitHub akan memicu redeploy otomatis. Startup pertama akan membuat tabel PostgreSQL dan master default.

Health check:

```text
/api/health
```

Respons harus menampilkan:

```json
{"status":"ok","database_backend":"postgresql"}
```

## 5. Volume
Untuk v1.2.1 PostgreSQL **Volume `/data` tidak wajib** untuk database. Dokumen Proyek dan logo perusahaan juga disimpan di PostgreSQL.

Log lokal container bersifat sementara; gunakan Railway Logs untuk monitoring.

## 6. Login pertama
- Username: `admin`
- Password: nilai `STOKLEDGER_ADMIN_PASSWORD`

Password variable hanya dipakai saat user admin pertama dibuat.

## 7. Backup
Gunakan fasilitas backup PostgreSQL Railway. Jangan mengandalkan backup `.db` karena build ini tidak memakai SQLite sebagai database utama ketika `DATABASE_URL` terpasang.

## 8. Update berikutnya
Update source → commit → push. Railway redeploy otomatis dan tetap memakai database PostgreSQL yang sama.

## 9. Jika deployment gagal
Cek Railway Logs. Kesalahan paling umum:
- `DATABASE_URL` belum direferensikan ke service PostgreSQL.
- PostgreSQL service belum aktif.
- password admin kurang dari 8 karakter.
- source lama masih memiliki variable `STOKLEDGER_DB_PATH` yang tidak diperlukan.
