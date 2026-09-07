StokLedger PRO ULTIMA v1.22.42

SALE DELETE - INVENTORY VALUATION CLEANUP

- Hapus Sales tidak lagi membuat SALE_VOID, SALE_DELETE, atau SALE_EDIT_REVERSAL di inventory history.
- Movement OUT SALE dari invoice yang dihapus ikut dihapus dari Rincian Valuasi Persediaan.
- Edit Sales membersihkan movement Sales lama lalu membuat movement Sales baru saja.
- Startup cleanup menghapus reversal legacy dan movement Sales dari invoice yang benar-benar sudah VOID.
- Inventory balances/book value direplay setelah pembersihan sehingga valuation mengikuti movement yang masih sah.
