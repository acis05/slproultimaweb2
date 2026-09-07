STOKLEDGER PRO v1.8.0 - INSTALLER & LISENSI DONGLE
===================================================

MODE TRIAL
- Maksimal 50 transaksi penjualan berstatus POSTED.
- Maksimal 2 user aktif.
- Setelah batas transaksi tercapai, data tetap dapat dibuka dan dilaporkan, tetapi transaksi penjualan baru ditolak.

MODE LIFETIME DONGLE
- File STOKLEDGER_PRO.LIC harus berada di root USB dongle.
- Lisensi terikat pada serial volume USB dan ditandatangani Ed25519.
- Dongle harus terpasang saat aplikasi digunakan.
- Maksimal 3 user aktif.
- Tidak ada batas transaksi dan tidak ada tanggal kedaluwarsa.

ALUR REGISTRASI PELANGGAN
1. Colok USB yang akan dijadikan dongle ke komputer Windows.
2. Jalankan tools\READ_DONGLE_SERIAL.bat untuk melihat serial 8 digit.
3. Di komputer Anda, jalankan:
   GENERATE_LICENSE.bat "Nama Pelanggan" SERIAL_USB
4. Salin STOKLEDGER_PRO.LIC hasil generator ke root USB tersebut.
5. Colok USB ke komputer pelanggan lalu jalankan StokLedger Pro.

KEAMANAN
- Jangan pernah memberikan license_private_key.pem kepada pelanggan.
- Folder tools/generator hanya untuk pemilik aplikasi.
- Pelanggan cukup menerima installer dan USB berisi STOKLEDGER_PRO.LIC.

DATA APLIKASI
- Database: C:\ProgramData\StokLedger Pro\data\stokledger_pro.db
- Log: C:\ProgramData\StokLedger Pro\logs\server.log
- Uninstall/update aplikasi tidak menghapus database di ProgramData.

MEMBUAT INSTALLER WINDOWS
1. Install Python 3.11+ 64-bit dan Inno Setup 6.
2. Jalankan BUILD_INSTALLER_WINDOWS.bat sebagai Administrator.
3. Hasil: installer\output\StokLedgerPro_Setup_v1.8.0.exe
