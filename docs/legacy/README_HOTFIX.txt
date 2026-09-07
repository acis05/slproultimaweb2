STOKLEDGER PRO v0.8.1 HOTFIX
================================

PERBAIKAN
- Memperbaiki NameError brand_id saat menyimpan barang.
- Menambahkan kolom brand_id pada INSERT produk.
- Mengembalikan brand_id dan brand_name di API produk.
- Validasi merk, kategori, satuan, dan gudang.
- Pesan duplikasi lebih spesifik.
- Error internal mempunyai nomor referensi di browser dan log.
- Smoke test mencakup barang dengan merk dan stok awal.

MIGRASI
Salin data\stokledger_pro.db dari v0.8 ke folder data v0.8.1 setelah server lama ditutup dan database dibackup.
