StokLedger PRO ULTIMA v1.22.53

- Search dropdown transaksi tetap terbuka saat halaman/area discroll; posisi popover mengikuti field aktif.
- Edit Pembelian dibuat atomik dan in-place; No Good Receive yang sama pada transaksi yang sedang diedit tidak dianggap duplikat.
- Edit Sales/Pembelian yang sudah mempunyai angsuran diperbolehkan selama total baru tidak lebih kecil dari pembayaran/alokasi yang sudah terjadi.
- Kegagalan validasi edit tidak lagi membatalkan jurnal/transaksi lama karena seluruh proses edit berjalan dalam satu transaksi SQLite.
