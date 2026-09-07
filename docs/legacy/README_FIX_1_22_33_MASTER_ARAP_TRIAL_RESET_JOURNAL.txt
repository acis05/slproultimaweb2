StokLedger PRO ULTIMA v1.22.33

Perbaikan:
1. Master data diurutkan berdasarkan kode (pelanggan, pemasok, kategori, satuan, merk, salesman, price level dan master berkode terkait).
2. Laporan Piutang/Hutang menghitung pembayaran aktual sampai tanggal laporan. Saldo awal AR/AP kini dapat dibayar dari modul penerimaan/pembayaran dan kolom Total Terbayar serta saldo outstanding ikut terupdate.
3. Trial tetap maksimum 50 transaksi logis. Jurnal ganda dari satu transaksi tidak lagi dihitung sebagai beberapa transaksi trial.
4. Draft Penjualan/Pembelian, termasuk sumber SO/PO, direset saat keluar halaman sehingga transaksi baru tidak membawa data sebelumnya.
5. Jurnal Manual mewajibkan Pelanggan untuk akun Piutang dan Pemasok untuk akun Hutang. Partner tipe BOTH didukung. Validasi dilakukan di UI dan backend.

Regression test: compile Python, logical trial count, sorting partner, pembayaran saldo awal AR/AP, report Total Terbayar, dashboard outstanding.
