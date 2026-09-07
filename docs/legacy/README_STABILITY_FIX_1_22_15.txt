Stability Fix 1.22.15

- Startup UI dibuat fault-tolerant: satu loader gagal tidak menghentikan dashboard/dropdown lain.
- Pelanggan dan pemasok transaksi dimuat melalui endpoint khusus setiap membuka form Penjualan/Pembelian.
- Jurnal Manual, Adjustment Stok, Kas Masuk/Keluar membuka form terlebih dahulu; loader data berjalan setelahnya dengan Promise.allSettled.
- Dashboard summary dimuat independen dan dashboard analytics ikut refresh pada startup.
- Event listener tidak bergantung pada global element-ID browser.
- Auto fresh-form setelah save dipertahankan tetapi dibuat defensif.
- Fitur impor Excel penjualan/pembelian dari versi sebelumnya dipertahankan.
