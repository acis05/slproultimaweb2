StokLedger PRO ULTIMA v1.22.32

Perbaikan:
1. Akun sistem 5140 Beban Diskon Penjualan, 5150 Beban Komisi Salesman, dan 2150 Hutang Komisi Salesman. Diskon dan komisi diposting ke jurnal sehingga masuk Buku Besar, Neraca Saldo, Laba Rugi, dashboard beban, dan laporan akuntansi berbasis jurnal.
2. Dashboard memasukkan saldo awal customer/supplier yang telah jatuh tempo berdasarkan tanggal saldo awal + termin pembayaran.
3. State edit transaksi dibersihkan setelah delete. Jika UI masih membawa ID transaksi VOID lama, penyimpanan otomatis kembali menjadi transaksi baru sehingga tidak terkunci pesan Transaksi sudah dihapus/dibatalkan.
4. Edit adjustment stok mempertahankan akun penyesuaian lama secara otomatis dan tidak meminta pengguna memilih akun lawan lagi. Penerimaan piutang, bayar hutang, dan jurnal manual tetap menggunakan akun yang melekat pada transaksi/baris jurnal tanpa kolom akun lawan tambahan.
