StokLedger 1.22.43 - In-place Valuation Edit Fix

- Edit saldo awal barang tidak lagi membuat OPENING_EDIT/koreksi baru.
- Movement OPENING asli diupdate quantity/cost-nya dan jurnal saldo awal asli diupdate.
- Edit Sales tidak menyisakan SALE_EDIT/VOID/DELETE di rincian valuasi.
- Cost SALE direplay dari moving-average dan jurnal HPP/Persediaan disinkronkan ke cost valuasi.
- Repair startup menggabungkan legacy OPENING_EDIT ke opening asli.
