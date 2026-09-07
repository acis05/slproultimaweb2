StokLedger PRO ULTIMA v1.22.31
Revisi 18 Agustus 2026

Perbaikan:
1. Edit Kas Masuk/Keluar
- Laporan Kas/Bank sekarang menyaring transaksi VOID dan reversal internal, sama seperti daftar kas dan arus kas.
- Histori VOID ditautkan ke ID transaksi pengganti aktif.
- Setelah edit/hapus kas, modul kas, jurnal, neraca saldo, dashboard, dan ringkasan di-refresh.

2. Beban Dashboard
- Ringkasan laba-rugi Dashboard memakai sumber yang sama dengan Laporan Laba Rugi (journal POSTED + subtype COA).
- Beban operasional, HPP, pendapatan, dan laba dashboard konsisten dengan laporan akuntansi pada periode yang sama.

3. Refresh Form Transaksi
- State mode edit maintenance dibersihkan saat keluar halaman transaksi, menutup halaman, atau membuka form transaksi baru.
- Form transaksi baru tidak lagi mewarisi ID edit transaksi sebelumnya.

4. Jurnal Manual Setelah Hapus/Edit
- Edit jurnal manual dilakukan atomik pada jurnal POSTED, tidak lagi VOID dahulu lalu mencoba update ID yang sama.
- Setelah jurnal dihapus, state edit UI dibersihkan sehingga jurnal baru dengan akun/keterangan serupa dapat disimpan normal.
