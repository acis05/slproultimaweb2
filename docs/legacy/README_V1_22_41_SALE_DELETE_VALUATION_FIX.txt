StokLedger PRO ULTIMA v1.22.41
SALE DELETE / INVENTORY VALUATION FIX

- Hapus penjualan tidak lagi membuat mutasi "Pembatalan Penjualan" bertanggal saat penghapusan.
- Reversal stok memakai HPP/unit cost persis dari movement SALE asli.
- Tanggal efektif koreksi stok mengikuti tanggal invoice penjualan asal.
- Jurnal SALE asli di-VOID sehingga Penjualan/PPN/HPP/Persediaan hilang dari GL pada periode invoice asal.
- Edit penjualan memakai jejak SALE_EDIT_REVERSAL, bukan Pembatalan Penjualan.
- Startup repair mengoreksi SALE_VOID legacy: cost disamakan dengan SALE asli, tanggal dipindahkan ke tanggal invoice, lalu valuasi direplay.
