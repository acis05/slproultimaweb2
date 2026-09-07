StokLedger ULTIMA v1.22.27

Perbaikan utama:
1. Negative inventory movement dengan cost berbeda dari average (terutama Retur Pembelian) sekarang menghitung ulang average cost sisa.
2. Average cost dan unit cost inventory internal memakai presisi 6 desimal untuk menghilangkan drift pembulatan qty x average.
3. Startup pertama menjalankan replay seluruh inventory_transactions untuk memperbaiki quantity_before/after, average_cost_before/after, inventory_balances, dan stock_qty produk.
4. Replay tidak membuat jurnal rekonsiliasi. Jurnal tetap mengikuti transaksi sumber.
5. Ringkasan Valuasi Persediaan menghitung nilai awal/masuk/keluar/akhir dari signed inventory movement value (qty_change x unit_cost).
6. Tanggal valuasi menggunakan tanggal dokumen sumber: saldo awal, pembelian, penjualan, retur, dan material proyek.
7. Ringkasan Valuasi total menampilkan:
   - Persediaan Buku Besar
   - Selisih dengan Buku Besar
   - Status Rekonsiliasi SESUAI/SELISIH
8. Ekspor PDF/Excel tetap didukung.

Regression:
Opening 10@100 = 1.000
Purchase 10@200 = +2.000
Purchase Return 2@200 = -400
Nilai akhir Valuasi = 2.600
Persediaan Buku Besar = 2.600
Selisih = 0
Sale setelah retur menggunakan average presisi dan tetap GL = Valuasi.
