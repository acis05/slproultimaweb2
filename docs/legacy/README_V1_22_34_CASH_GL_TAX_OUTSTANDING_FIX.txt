StokLedger update 1.22.34

Perbaikan:
1. Invoice penjualan/pembelian tunai tidak lagi muncul sebagai outstanding pada AR/AP dan alokasi DP.
2. Ringkasan Total Pembelian UI sudah memasukkan PPN dan mode diskon persen/nominal.
3. Transfer antar akun Kas/Bank membuat jurnal GL (Debit tujuan / Kredit asal), sehingga masuk Buku Besar, Neraca Saldo dan Neraca. Arus Kas Langsung menampilkan transfer internal dengan dampak neto nol.
4. Jurnal Manual yang memakai COA Kas/Bank disinkronkan ke mutasi saldo operasional Kas/Bank sehingga saldo pada modul transaksi, laporan Kas/Bank dan Arus Kas ikut berubah.
