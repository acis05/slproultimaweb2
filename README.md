# StokLedger Online v1.4.2 — Production Security Edition

## v1.4.2 Password Recovery

- Semua user yang sedang login mempunyai menu **Ubah Password**.
- Perubahan password sendiri wajib memasukkan password saat ini dan password baru minimal 8 karakter.
- Administrator perusahaan tetap dapat reset password user lain melalui **User & Hak Akses**. Password hasil reset ditandai sebagai password sementara dan user wajib menggantinya pada login berikutnya.
- Jika Administrator utama perusahaan lupa password, Owner Admin dapat memilih **Reset Password Admin** pada akun tenant. Sistem menghasilkan password sementara satu kali, mencabut sesi admin lama, dan mewajibkan ganti password setelah login.
- Tidak ada reset tanpa verifikasi melalui halaman publik. Ini mencegah pengambilalihan akun hanya dengan mengetahui email.


## v1.4.2 Role-Aware UI
- Menu desktop, menu mobile, kartu fitur, dan tab workspace mengikuti permission role user yang login.
- Fitur tanpa izin disembunyikan agar add-on user hanya melihat pekerjaan yang memang tersedia untuk rolenya.
- Dashboard ikut disembunyikan bila role tidak memiliki `dashboard.view`; aplikasi otomatis membuka modul pertama yang diizinkan.
- Startup tidak lagi memuat daftar transaksi/admin yang jelas tidak dimiliki role tersebut, sehingga mengurangi request 403 yang tidak perlu.
- Backend permission tetap menjadi lapisan keamanan utama; perubahan ini adalah penyederhanaan UX berdasarkan role.


Versi ini melanjutkan v1.3.5 (branding StokLedger Online + multi-tab) dan menambah hardening untuk deployment komersial.

## Security hardening v1.4.2

- **Owner Admin 2FA/TOTP wajib**: password + kode Authenticator 6 digit.
- **Login lockout**: 5 kegagalan dari kombinasi user/IP dalam 15 menit akan diblokir sementara.
- **Signup rate limit**: maksimal 5 pendaftaran trial per IP per jam.
- **Owner login protection**: brute-force protection dengan blokir lebih ketat.
- **Security Audit pusat** di `/owner-admin` → `Security Audit`.
- **Tenant guard**: login aplikasi PostgreSQL tidak boleh fallback ke schema public/bootstrap. Semua user harus terikat ke tenant.
- **Origin protection** untuk request POST/PUT/DELETE browser.
- **Security headers**: CSP, HSTS saat HTTPS, anti-frame, no-sniff, same-origin opener/resource policy.
- **Session token** aplikasi dan Owner Admin dipindahkan ke `sessionStorage`, bukan persistent `localStorage`.
- Session aplikasi default dipersingkat menjadi **8 jam**, Owner Admin **4 jam**.

## Railway Variables wajib

```text
STOKLEDGER_WEB_MODE=1
DATABASE_URL=${{Postgres.DATABASE_URL}}
STOKLEDGER_ADMIN_PASSWORD=<password bootstrap>
STOKLEDGER_LICENSE_ADMIN_KEY=<kunci aktivasi>
STOKLEDGER_TOKEN_HOURS=8
STOKLEDGER_OWNER_ADMIN_PASSWORD=<minimal 12 karakter>
STOKLEDGER_OWNER_TOTP_SECRET=<base32 secret authenticator>
STOKLEDGER_ALLOWED_ORIGINS=https://DOMAIN-PRODUKSI-ANDA
```

Generate secret TOTP sebelum deploy:

```bash
python scripts/generate_owner_totp.py
```

Masukkan `STOKLEDGER_OWNER_TOTP_SECRET` yang dihasilkan ke Railway Variables dan tambahkan URI `otpauth://...` ke Google Authenticator, Microsoft Authenticator, 1Password, Authy, atau aplikasi TOTP lain.

## URL penting

- Aplikasi pelanggan: `/`
- Owner Admin: `/owner-admin`
- Health check: `/api/health`

## Production checklist

1. Gunakan custom domain HTTPS.
2. PostgreSQL hanya diakses dari service aplikasi/private network; jangan expose TCP proxy bila tidak diperlukan.
3. Aktifkan backup PostgreSQL Railway dan backup offsite berkala.
4. Gunakan project/environment **staging** terpisah untuk testing update.
5. Taruh Cloudflare/WAF di depan domain produksi bila memungkinkan.
6. Jangan commit file `.env` atau secret ke GitHub.
7. Pastikan Owner 2FA aktif sebelum mulai menjual akun.
8. Uji tenant A tidak dapat membaca tenant B sebelum setiap release besar.

## Catatan

Hardening aplikasi mengurangi risiko tetapi tidak menggantikan backup, monitoring, patch dependency, pengaturan Railway, Cloudflare/WAF, serta prosedur operasional yang baik.
