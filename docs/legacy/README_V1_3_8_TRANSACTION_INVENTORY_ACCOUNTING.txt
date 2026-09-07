STOKLEDGER PRO v1.3.8 - TRANSACTION & INVENTORY ACCOUNTING FIX
==============================================================

1. Dropdown pelanggan pada Penjualan dan pemasok pada Pembelian memakai endpoint khusus.
2. loadTransactionPartners() tersedia dan dipanggil setelah master partner baru dibuat.
3. Kas Masuk/Keluar memiliki Akun Lawan dan otomatis menjurnal:
   - Masuk: Debit Kas/Bank, Kredit Akun Lawan.
   - Keluar: Debit Akun Lawan, Kredit Kas/Bank.
4. Transfer Kas/Bank memastikan pilihan Akun Sumber dan Akun Tujuan terisi.
5. Penyesuaian Stok memiliki Akun Penyesuaian dan jurnal nilai stok otomatis.
6. Master Barang memiliki:
   - Akun Persediaan
   - Akun Penjualan
   - Akun HPP
7. Pembelian stok didebit ke akun Persediaan per barang.
8. Penjualan dikredit ke akun Penjualan per barang.
9. HPP dan pengurangan persediaan mengikuti akun HPP/Persediaan per barang.
10. Data barang lama otomatis memakai default 1200, 4000, dan 5000.