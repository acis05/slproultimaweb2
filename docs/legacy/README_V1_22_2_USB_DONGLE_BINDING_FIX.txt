StokLedger Pro Ultima v1.22.2 - USB Dongle Binding Fix

Perubahan lisensi:
- Binding utama hanya APP_ID + USB Volume Serial + signature.
- License ID tidak lagi dipakai untuk menentukan apakah dongle sama/berbeda.
- Binding lama schema v1 otomatis dimigrasikan jika serial USB sama.
- Generate ulang lisensi pada USB yang sama tetap diterima.
- Penggantian USB membutuhkan file izin REBIND yang ditandatangani generator internal.
- Izin REBIND sekali pakai akan dihapus setelah binding berhasil dipindahkan jika media dapat ditulis.

File lisensi: STOKLEDGER_PRO_ULTIMA.LIC
File izin rebind: STOKLEDGER_PRO_ULTIMA_REBIND.AUTH
