StokLedger ULTIMA v1.22.29

Perbaikan khusus selisih Valuasi Persediaan vs Buku Besar/Neraca:

Akar bug build sebelumnya:
- Adjustment Stok dengan Nomor Referensi kosong tidak dapat dicocokkan ke jurnal STOCK_ADJUSTMENT.
- Build source-sync lama lalu membuat jurnal INVENTORY_SOURCE_ADJUSTMENT baru.
- Akibatnya Persediaan GL dapat terhitung dua kali, sementara nilai valuation tidak berubah.
- Baris koreksi 'Sinkron nilai persediaan ...' dari build lama juga dapat tertinggal pada jurnal sumber.

Perbaikan build ini:
1. Mapping inventory source memakai source ID transaksi asli, bukan reference_no umum.
2. STOCK_ADJUSTMENT selalu dicocokkan dengan inventory_transaction.id, termasuk saat reference_no kosong.
3. Jurnal legacy SYSTEM_INVENTORY_RECON, SYSTEM_HPP_RECON, dan INVENTORY_SOURCE_* otomatis dibuat VOID.
4. Baris lama 'Sinkron nilai persediaan ...' dan 'Lawan sinkron nilai persediaan ...' otomatis dibersihkan.
5. Jurnal Manual/Manual Excel lama yang langsung mengenai akun kontrol Persediaan direklasifikasi ke Penyesuaian Stok.
6. Opening inventory dan SALE/HPP dinormalisasi ulang dari inventory transaction.
7. Replay book value dipaksa jalan kembali pada database yang sebelumnya sudah menjalankan repair versi lama.
8. Source correction hanya dilakukan pada jurnal sumber asli yang berhasil dipetakan.
9. Tidak lagi membuat jurnal inventory baru hanya karena reference_no kosong/tidak ditemukan.

Regression:
- Nilai stok 1.200.000.
- Database disimulasikan rusak oleh duplicate INVENTORY_SOURCE_ADJUSTMENT +200.000
  dan old injected sync pair +50.000.
- Sebelum cleanup GL = 1.450.000, valuation = 1.200.000.
- Sesudah cleanup GL = 1.200.000, valuation = 1.200.000, selisih 0, status SESUAI.
- Test kedua: jurnal adjustment sengaja salah + manual inventory legacy 1.400.000.
  Canonical source repair mengembalikan valuation = GL dan status SESUAI.
