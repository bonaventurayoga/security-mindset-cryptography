\# Security Mindset: Eksperimen Kriptografi



Repository ini berisi beberapa percobaan sederhana untuk memahami cara kerja keamanan data dari sisi attacker dan defender.



Percobaan ini dibuat untuk melihat bahwa mengubah bentuk data atau menggunakan hash saja belum tentu cukup untuk mengamankan data.



\## Isi Percobaan



\### Percobaan 1 — Base64



File: `Percobaan1.py`



Percobaan ini menunjukkan bahwa \*\*Base64 bukan enkripsi\*\*.



Data yang sudah diubah ke Base64 masih dapat di-decode, dibaca, diubah, lalu di-encode kembali.



Contohnya:



```text

KUPON|nadia|5000

```



dapat diubah menjadi Base64. Setelah itu, nilainya dapat dimodifikasi menjadi:



```text

KUPON|nadia|50000

```



Kemudian data tersebut di-encode kembali.



\*\*Kesimpulan:\*\* Base64 hanya mengubah bentuk data, bukan memberikan perlindungan terhadap perubahan data.



\---



\### Percobaan 2 — SHA-256



File: `Percobaan2.py`



Percobaan ini menggunakan SHA-256 untuk melihat bagaimana hash dapat digunakan untuk mendeteksi perubahan data.



Jika data berubah, hash yang dihasilkan juga akan berubah.



Namun, ada masalah lain. Jika attacker dapat mengubah data dan menghitung hash baru, maka hash tersebut dapat ikut diganti.



\*\*Kesimpulan:\*\* Hash dapat membantu mengecek integritas data, tetapi hash saja belum cukup untuk memastikan bahwa data benar-benar berasal dari pihak yang dipercaya.



\---



\### Percobaan 3 — HMAC dan Replay Attack



File: `Percobaan3.py`



Percobaan ini menggunakan \*\*HMAC-SHA256\*\* dengan secret key.



Berbeda dengan hash biasa, HMAC membutuhkan kunci rahasia untuk membuat tanda autentikasi.



Jika attacker mengubah isi transaksi tetapi tidak mengetahui secret key, HMAC yang dikirim tidak akan cocok dengan hasil perhitungan server.



Percobaan ini juga menunjukkan \*\*replay attack\*\*.



Walaupun HMAC dapat memastikan data tidak diubah, paket yang valid masih dapat dikirim ulang oleh attacker.



Untuk mengatasi masalah tersebut, digunakan:



\* \*\*Nonce\*\* untuk memastikan paket tidak digunakan kembali.

\* \*\*Timestamp\*\* untuk membatasi umur paket.



\*\*Kesimpulan:\*\* HMAC membantu menjaga integritas dan autentikasi data, tetapi untuk mencegah replay attack masih diperlukan mekanisme tambahan seperti nonce dan timestamp.



\## Cara Menjalankan



Pastikan Python sudah terinstall.



Masuk ke folder repository, kemudian jalankan:



```bash

python Percobaan1.py

```



Untuk percobaan SHA-256:



```bash

python Percobaan2.py

```



Untuk percobaan HMAC dan replay attack:



```bash

python Percobaan3.py

```



\## Tujuan Pembelajaran



Dari ketiga percobaan ini, alurnya kurang lebih seperti berikut:



```text

Base64

&#x20;  ↓

Bukan enkripsi

&#x20;  ↓

SHA-256

&#x20;  ↓

Bisa mendeteksi perubahan, tetapi belum mengautentikasi sumber

&#x20;  ↓

HMAC

&#x20;  ↓

Menggunakan secret key untuk autentikasi

&#x20;  ↓

Replay Attack

&#x20;  ↓

Masih membutuhkan nonce dan timestamp

```



Intinya, keamanan data tidak cukup hanya dengan melihat apakah data memiliki hash atau sudah "diubah bentuknya". Kita juga perlu memikirkan \*\*siapa yang membuat data, apakah data pernah diubah, dan apakah data lama sedang digunakan kembali\*\*.



\## Catatan



Project ini dibuat untuk keperluan pembelajaran mata kuliah Kriptografi dan Security Mindset.



Semua percobaan dilakukan dalam lingkungan latihan dan bukan untuk menyerang sistem nyata.



