Core Master Stability Fix 1.22.16

Perbaikan:
- COA dimuat independen dari jurnal, template, dan buku besar.
- Semua akun Jurnal Manual dan Kas Masuk/Keluar memakai loader COA inti yang sama.
- Loader Kas/Bank tidak bergantung pada implicit browser globals.
- Daftar Barang aman walau kontrol Adjustment/Transfer tidak ada pada varian tertentu.
- Master Jasa, kategori jasa, dan akun jasa memakai DOM eksplisit.
- Daftar Jasa tahan terhadap referensi unit/COA legacy yang sudah hilang.
- Compile Python dan syntax JavaScript diuji.
