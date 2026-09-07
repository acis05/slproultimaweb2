StokLedger ULTIMA v1.22.30

Revisi 15 Agustus 2026

1. PDF Laporan Keuangan
- Laba Rugi, Neraca, Arus Kas Langsung dan Buku Besar memakai layout khusus yang mengikuti struktur preview.
- Laporan tabular keuangan (Jurnal, Neraca Saldo, Piutang, Hutang) memakai layout tabel keuangan yang lebih rapi, repeat header, wrap text, lebar kolom terkontrol, dan ringkasan di bawah.
- Periode filter ikut tercetak.
- PDF diuji dengan render ke PNG; tidak ditemukan clipping/overlap pada sampel Laba Rugi, Neraca, dan Arus Kas.

2. Import Rekening Koran Multi-Bank
- BCA tetap memakai parser khusus.
- Ditambah parser generik PDF teks untuk Mandiri, BRI, BNI, CIMB Niaga, Permata, Danamon, OCBC, BSI, Maybank, Panin dan bank lain dengan pola tanggal + mutasi + saldo.
- Mendukung DB/DEBIT dan CR/CREDIT/KREDIT, serta format angka Indonesia/internasional.
- PDF scan tanpa text layer tetap harus menggunakan PDF teks atau CSV/Excel.

3. Edit Daftar Kas Masuk/Keluar
- Transaksi lama di-VOID untuk audit trail.
- Jurnal CASH_TRANSACTION lama di-VOID dan transaksi pengganti membuat jurnal baru POSTED.
- Saldo Kas/Bank dihitung ulang kronologis.
- Baris lama/pembalikan internal tidak ikut Buku Kas/Bank dan Arus Kas.
- Buku Besar, Neraca Saldo, Neraca, laporan Kas/Bank dan Dashboard membaca transaksi pengganti aktif.
- UI selesai edit langsung refresh modul Kas/Bank + Akuntansi.

4. Aktiva Tetap Masa Manfaat 0
- useful_life_months=0 sekarang valid untuk tanah/aset non-depreciable.
- UI menerima nilai 0 dan menampilkan 'Tidak disusutkan'.
- Penyusutan bulanan = 0.
- Proses Penyusutan Otomatis melewati aset masa manfaat 0 tanpa error dan tanpa jurnal penyusutan.
- Database lama dengan CHECK useful_life_months>0 dimigrasikan otomatis menjadi >=0 tanpa menghapus histori aktiva.

Regression:
- Tanah masa manfaat 0 berhasil dibuat, monthly depreciation = 0, tidak membuat jurnal penyusutan.
- Kas Masuk 100.000 diedit menjadi Kas Keluar 25.000: jurnal lama VOID, pengganti POSTED, laporan hanya membaca transaksi pengganti.
- Parser Mandiri/BRI/BNI membaca debit/kredit dari format teks contoh.
- PDF Laba Rugi/Neraca/Arus Kas berhasil dibuat dan dirender tanpa layout rusak.
