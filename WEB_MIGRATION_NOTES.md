# Web v1.2.1 PostgreSQL Migration Notes

- Database utama: PostgreSQL (`DATABASE_URL`).
- SQLite tetap tersedia hanya sebagai fallback development bila `DATABASE_URL` kosong.
- Railway Volume tidak diperlukan untuk record transaksi.
- Dokumen Proyek dan logo perusahaan pada mode PostgreSQL disimpan sebagai `BYTEA` di database.
- Trial/langganan tersimpan di PostgreSQL.
- Web v1.2.1 membuat schema baru otomatis.
- Migrasi data existing dari SQLite harus dilakukan terpisah dan diverifikasi sebelum go-live.
