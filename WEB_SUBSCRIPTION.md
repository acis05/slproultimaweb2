# Trial & Langganan — StokLedger Pro Ultima Web v1.2.0

Versi web memakai lisensi berbasis waktu (bukan dongle USB dan bukan batas jumlah transaksi).

## Trial
- 7 hari sejak database web pertama kali dibuat.
- Maksimal 2 user/device aktif.
- Sesudah trial berakhir, data tetap tersimpan dan Administrator masih dapat login untuk aktivasi, tetapi posting transaksi baru diblokir sampai langganan aktif.

## Paket
| Paket | Harga dasar | User termasuk | Add-on user |
|---|---:|---:|---:|
| 6 bulan | Rp1.200.000 | 2 | Rp100.000/user/6 bulan |
| 1 tahun | Rp2.000.000 | 2 | Rp200.000/user/tahun |

Aktivasi dilakukan dari **Sistem → Trial & Langganan**. Menu ini hanya tampil untuk role Administrator dan perubahan aktivasi tetap membutuhkan `STOKLEDGER_LICENSE_ADMIN_KEY`, yaitu rahasia milik operator/pemilik aplikasi yang disimpan di Railway Variables.

## Railway Variable wajib untuk aktivasi
```text
STOKLEDGER_LICENSE_ADMIN_KEY=buat-kunci-rahasia-yang-panjang-dan-sulit-ditebak
```
Jangan membagikan nilai ini kepada user pelanggan. Password login Administrator perusahaan dan Kunci Admin Aktivasi adalah dua hal yang berbeda.
