STOKLEDGER PRO v1.4.5c — USER ACCESS INDEPENDENT HOTFIX
=========================================================

Penyebab error:
- Modul User & Hak Akses memanggil designerEscape().
- Fungsi tersebut milik modul Desain Dokumen dan tidak selalu tersedia.
- JavaScript berhenti saat merender nama role/user/permission.

Perbaikan:
- Modul User & Hak Akses sekarang memiliki accessEscape() sendiri.
- Tidak lagi bergantung pada Desain Dokumen.
- Respons /api/roles, /api/users, dan /api/permissions divalidasi.
- Mendukung respons API berbentuk {items:[...]} maupun array langsung.
- Dropdown Role, Daftar User, Daftar Role, dan Permission Matrix dirender
  secara independen.
- Ditambahkan tombol Coba Muat Ulang bila API gagal.
- Dashboard, sidebar, refreshAll(), dan modul lain tidak diubah.