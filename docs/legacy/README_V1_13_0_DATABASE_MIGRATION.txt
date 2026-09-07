STOKLEDGER v1.13.0 - DATABASE MIGRATION

- Mendeteksi database StokLedger Standard melalui struktur schema lama.
- Membuat backup SQLite konsisten sebelum upgrade.
- Memigrasikan akun, barang, pelanggan/pemasok, penjualan, pembelian, detail transaksi, dan jurnal.
- Menambah metadata schema_version dan edisi.
- Tabel legacy dipertahankan dengan prefix legacy_standard_ untuk audit dan pemulihan.
- Upgrade Standard ke Pro atau Pro Ultima didukung; downgrade tidak didukung.
