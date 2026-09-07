Report Export Fix 1.22.10

- Memperbaiki ekspor Excel Buku Besar ketika summary mengandung struktur nested sections.
- Exporter Excel sekarang hanya menulis nilai cell yang aman dan mengabaikan metadata nested pada ringkasan.
- Export PDF diperkuat untuk laporan dengan banyak kolom: wrap text, ukuran font adaptif, dan lebar kolom mengikuti halaman landscape.
- Nama file ekspor disanitasi agar karakter terlarang tidak menyebabkan error.
- Freeze header dan AutoFilter ditambahkan pada Excel.
- Smoke test otomatis seluruh laporan pada database uji:
  Pro: 39 laporan x 2 format = 78 ekspor, 0 gagal.
  Pro Ultima: 42 laporan x 2 format = 84 ekspor, 0 gagal.
  Service: 41 laporan x 2 format = 82 ekspor, 0 gagal.

Laporan proyek diuji dengan proyek dummy valid karena laporan tersebut memang mensyaratkan pemilihan proyek.
