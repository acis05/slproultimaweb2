# v1.4.2 Security Migration Notes

- Tidak mengubah schema transaksi tenant.
- Menambah tabel pusat `saas_security_attempts`, `saas_rate_limits`, dan `saas_security_audit` di schema `public`.
- Existing tenant/user tidak perlu dibuat ulang.
- Token lama di `localStorage` dimigrasikan sekali ke `sessionStorage` lalu dihapus dari localStorage.
- Login public/bootstrap schema dinonaktifkan pada PostgreSQL SaaS mode.
- Owner Admin sekarang wajib TOTP jika production hardening digunakan.
- Sebelum upgrade, buat backup PostgreSQL.
