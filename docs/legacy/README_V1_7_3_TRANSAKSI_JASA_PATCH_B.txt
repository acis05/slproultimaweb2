STOKLEDGER PRO v1.7.3 — TRANSAKSI JASA PATCH B
=================================================
PENJUALAN
- Satu invoice dapat berisi campuran Barang dan Jasa.
- Harga jual default diambil dari Master Jasa.
- Pendapatan jasa memakai Akun Penjualan pada Master Jasa.
- Jasa tidak mengurangi stok dan tidak membentuk jurnal HPP/Persediaan.

PEMBELIAN
- Satu faktur dapat berisi campuran Barang dan Jasa.
- Harga beli default diambil dari Master Jasa.
- Pembelian jasa memakai Akun Pembelian pada Master Jasa.
- Jasa tidak menambah stok dan tidak masuk Kartu Stok.

KOMPATIBILITAS
- Master Jasa disinkronkan ke item transaksi internal bertipe SERVICE.
- Data Master Barang tetap terpisah dan item internal jasa tidak tampil di Daftar Barang.
- Jasa yang sudah digunakan transaksi tidak dapat dihapus; dapat dinonaktifkan.
- Dokumen, pajak, diskon, pembayaran, piutang/hutang, proyek, dan departemen
  tetap memakai engine transaksi yang stabil.

BELUM DI PATCH B
- Laporan Penjualan per Jasa (Patch C / v1.7.4).