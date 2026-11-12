# Menjalankan analisis di Windows

1. Ekstrak ZIP dengan klik kanan > Extract All. Masuk ke folder yang menampilkan README.md, requirements.txt, data, docs, dan scripts.
2. Klik bilah alamat File Explorer, ketik cmd, lalu Enter. Kotak perintah akan terbuka langsung di folder proyek.
3. Ketik perintah di bawah satu per satu. Jika Windows tidak mengenali py, coba python. Jika keduanya belum tersedia, pasang Python 3 untuk Windows dari https://www.python.org/downloads/windows/ lalu buka ulang cmd.

```bat
py --version
py -m pip install -r requirements.txt
py scripts\risiko.py
py scripts\penjualan.py
py scripts\keuangan.py
```

Setiap skrip mengunduh data aslinya ke data/raw pada pemakaian pertama lalu memakai salinan itu pada pemakaian berikutnya. Pembacaan lebih dari satu juta baris Excel memerlukan waktu. Jika unduhan otomatis terganggu, unduh dari URL pada skrip dan simpan di data/raw dengan nama schedule.csv, retail.zip (tetap ZIP), atau FactFinance.csv. Untuk memakai rilis sumber yang lebih baru, pindahkan salinan mentah lama sebelum menjalankan ulang.

Bandingkan hasil/risiko.csv untuk Mei 2026 (1.050 jadwal mundur >90 hari), hasil/penjualan.csv untuk 2010 (19.627 pesanan), dan hasil/keuangan.csv (laba operasi aktual 390.894). Perubahan rilis sumber dapat mengubah hasil. check.py memeriksa CSV ringkasan yang dikemas dengan dashboard. File .dax berisi rumus model masing-masing proyek.

Untuk GitHub cukup unggah data ringkasan, hasil, docs, scripts, README.md, requirements.txt, dan .gitignore. Simpan data/raw dan __pycache__ di laptop. Saat mengunggah manual lewat browser, keluarkan kedua folder tersebut dari pilihan unggahan.
