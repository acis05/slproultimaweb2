Update 1.22.20
1. HPP penjualan memakai moving-average cost aktual dari inventory transaction; snapshot laporan disinkronkan dengan HPP jurnal.
2. Endpoint PUT edit COA dipastikan aktif.
3. Search barang ditambahkan pada setiap baris input Penjualan.
4. Saldo awal barang disimpan sebagai metadata dan dapat dikoreksi saat edit; stok dan jurnal koreksi ikut berubah.
5. Barcode import barang opsional; import tanpa kolom/nilai Barcode tetap valid.
6. Hapus barang tanpa transaksi bisnis melakukan hard delete; barang dengan histori transaksi dinonaktifkan.
