StokLedger v1.11.2 - Perbaikan Daftar Penyusutan

- Memperbaiki urutan route API yang membuat /api/fixed-assets/depreciations salah dibaca sebagai ID aktiva.
- Riwayat penyusutan kini tampil otomatis pada halaman Penyusutan Otomatis.
- Setiap riwayat memiliki tombol Hapus.
- Penghapusan membatalkan jurnal penyusutan (status VOID), menghapus riwayat, dan memungkinkan periode diproses kembali.
- Daftar otomatis dimuat ulang setelah proses maupun penghapusan penyusutan.
