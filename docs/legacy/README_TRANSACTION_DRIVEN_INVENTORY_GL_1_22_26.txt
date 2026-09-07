StokLedger ULTIMA v1.22.26

Perubahan konsep persediaan:
- Jurnal 'SYSTEM_INVENTORY_RECON' / 'SYSTEM_HPP_RECON' dari build lama otomatis di-VOID.
- Tidak ada lagi jurnal rekonsiliasi persediaan otomatis ke Laba Ditahan.
- Nilai persediaan mengikuti mutasi stok yang sebenarnya.
- Saldo awal barang: debit Persediaan / kredit Ekuitas sesuai qty x cost.
- Edit saldo awal turun: kredit Persediaan memakai moving-average cost aktual yang benar-benar keluar.
- Edit saldo awal naik: debit Persediaan memakai cost barang yang masuk.
- Jika harga saldo awal diedit sebelum ada transaksi bisnis, nilai opening inventory dan jurnal opening langsung direvalue.
- Penjualan: Debit HPP / Kredit Persediaan berdasarkan moving-average cost pada saat barang keluar.
- Migrasi database lama menormalkan pasangan HPP/Persediaan langsung di jurnal SALE asli, bukan membuat jurnal rekonsiliasi terpisah.
- Hapus barang tanpa transaksi juga membersihkan source opening journal yang benar (OPENING_PRODUCT).
- Startup hanya melaporkan akun persediaan legacy yang masih unresolved; sistem tidak menutup selisih secara paksa ke Laba Ditahan.

Regression:
Opening 10@100 -> Persediaan GL 1.000 = nilai stok 1.000
Purchase 10@200 -> nilai stok/GL 3.000
Sale 4 @ avg 150 -> HPP 600; nilai stok/GL 2.400
Edit opening 10 -> 8 setelah transaksi -> movement keluar memakai avg cost, nilai stok tetap = GL
Legacy SYSTEM_INVENTORY_RECON -> otomatis VOID
Corrupt HPP SALE -> pasangan HPP/Persediaan diperbaiki di jurnal SALE yang sama
