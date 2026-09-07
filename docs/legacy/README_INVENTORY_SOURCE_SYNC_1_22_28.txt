StokLedger ULTIMA v1.22.28

Tujuan: total nilai barang = akun kontrol Persediaan di Buku Besar/Neraca.

Perubahan:
1. Inventory balance sekarang menyimpan BOOK VALUE moneter eksplisit, bukan mengandalkan qty x average yang bisa drift.
2. Setiap inventory transaction menyimpan value_before, value_change, value_after.
3. Movement value dibulatkan 2 desimal dan nilai yang sama dipakai sebagai dasar jurnal Persediaan/HPP.
4. Startup pertama replay histori inventory untuk membentuk kembali book value persediaan.
5. Startup pertama melakukan SOURCE SYNC:
   - membandingkan nilai inventory movement per referensi dengan baris akun Persediaan pada jurnal referensi yang sama;
   - bila ada selisih legacy, koreksi ditambahkan di jurnal sumber yang sama, bukan RECON-INV global;
   - opening tetap ditangani per barang oleh OPENING_PRODUCT;
   - SALE/HPP tetap ditangani di jurnal SALE.
6. Jurnal Manual/Import Jurnal Manual lama yang langsung memakai akun kontrol Persediaan direklasifikasi ke akun Penyesuaian Stok, karena tidak memiliki barang/gudang.
7. Jurnal Manual baru dilarang memakai akun kontrol Persediaan. User harus memakai Saldo Awal Barang, Pembelian, Retur, atau Adjustment Stok.
8. Ringkasan Valuasi menampilkan nilai persediaan Buku Besar, selisih, dan status SESUAI/SELISIH.

Regression:
- dibuat selisih legacy sumber pembelian +400.000;
- dibuat jurnal manual langsung ke Persediaan +1.400.000;
- sebelum sync: valuation != GL;
- setelah source sync: valuation = GL, selisih 0, status SESUAI.
