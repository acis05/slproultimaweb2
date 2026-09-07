Perbaikan 11 Agustus 2026
- HPP penjualan: fallback biaya untuk stok legacy/import yang quantity-nya ada tetapi average cost lama masih 0.
- Search barang pada input Penjualan dan Pembelian (SKU, nama, barcode, merk).
- Satuan transaksi diperkuat: base unit selalu tersedia di UI; database legacy tanpa product_units dinormalisasi ke satuan dasar.
- Edit Barang, Pelanggan, dan Pemasok menggunakan referensi DOM eksplisit agar mode edit benar-benar mengisi form lintas browser.
- Python compile dan JavaScript syntax check PASS.
