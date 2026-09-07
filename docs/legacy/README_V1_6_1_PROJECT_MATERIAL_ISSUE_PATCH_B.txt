STOKLEDGER PRO v1.6.1 — PROJECT MATERIAL ISSUE PATCH B
========================================================
- Menu Pengeluaran Material Proyek.
- Nomor otomatis PMI-YYYYMM-######.
- Pilih Proyek, Departemen, Gudang, akun pengeluaran, dan barang.
- Average cost diambil dari saldo gudang saat posting dan disimpan historis.
- Stok gudang berkurang dan masuk Kartu Stok.
- Jurnal: Debit HPP/Beban/Aset, Kredit Persediaan.
- Semua journal_lines membawa project_id dan department_id.
- Realisasi Budget Material dan sisa budget diperbarui otomatis.
- Akun dibatasi tipe HPP, Beban, atau Aset.
- Stok tidak boleh kurang dari qty yang dikeluarkan.
- Patch C untuk realisasi biaya dari transaksi lain belum diterapkan.