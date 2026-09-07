StokLedger PRO ULTIMA v1.22.49

Fix 2026-08-24:
1. Import kategori tanpa kolom Jenis Kategori kini default BOTH, sehingga kategori tersedia untuk Barang dan Jasa; tipe JASA tetap masuk ke Kategori Jasa.
2. Search Master Barang dilakukan secara lokal dari data master penuh (SKU/nama/barcode/merk/kategori), menghindari race request saat mengetik.
3. Adjustment Stok menampilkan stok sesuai Gudang yang dipilih, bukan total semua gudang; label diperbarui saat Gudang berubah.
