"""
Kriptografi Minggu 2
Percobaan: Membongkar Vigenere dan Menganalisis Desain Login

Semua data dalam program ini adalah data latihan/fiktif.
Program ini tidak digunakan untuk menyerang sistem nyata.
"""

from collections import defaultdict
import hashlib
import math
import string


# ============================================================
# BAGIAN A - VIGENERE CIPHER
# ============================================================

ABC = string.ascii_uppercase

CIPHERTEXT = (
    "BABPNHONSJLMCHUBJMXAZSCHSNPPBCKNWTFSLODPNGBIGBFSXTMXNAQABPXSRADXDMWAFHIJOSQBOSKNSVILKPMCCLSAPXGAXTMBYELAIPFSZODPHCOUMCASXDMCXSPTMGJWCEDIUQKNSHOVKHPXEGXFUGGSCIWDXWSNUSCYENMZUFENFJEDKTUWUFZEYTWSRAZRCHREDKCYONQGY"
)

KEY = "KAMPUS"

PLAINTEXT = (
    "RAPAT PENGURUS HIMPUNAN DIPINDAHKAN KE LABORATORIUM "
    "LANTAI TIGA PADA HARI JUMAT SORE"
)


def encrypt_vigenere(text, key):
    """Mengenkripsi teks menggunakan Vigenere Cipher."""
    hasil = []
    key = key.upper()
    key_index = 0

    for char in text.upper():
        if char in ABC:
            p = ABC.index(char)
            k = ABC.index(key[key_index % len(key)])

            cipher = (p + k) % 26
            hasil.append(ABC[cipher])

            key_index += 1

    return "".join(hasil)


def decrypt_vigenere(ciphertext, key):
    """Mendekripsi ciphertext menggunakan Vigenere Cipher."""
    hasil = []
    key = key.upper()
    key_index = 0

    for char in ciphertext.upper():
        if char in ABC:
            c = ABC.index(char)
            k = ABC.index(key[key_index % len(key)])

            plain = (c - k) % 26
            hasil.append(ABC[plain])

            key_index += 1

    return "".join(hasil)


# ============================================================
# BAGIAN B - KASISKI EXAMINATION
# ============================================================

def cari_pengulangan(ciphertext, panjang=3):
    """
    Mencari potongan ciphertext yang muncul lebih dari sekali.
    Hasil berupa:
    {
        potongan: [posisi1, posisi2, ...]
    }
    """
    posisi = defaultdict(list)

    for i in range(len(ciphertext) - panjang + 1):
        potongan = ciphertext[i:i + panjang]
        posisi[potongan].append(i)

    return {
        teks: posisi_teks
        for teks, posisi_teks in posisi.items()
        if len(posisi_teks) > 1
    }


def hitung_jarak(posisi):
    """Menghitung jarak antar kemunculan potongan ciphertext."""
    jarak = []

    for i in range(len(posisi) - 1):
        jarak.append(posisi[i + 1] - posisi[i])

    return jarak


def faktor_bersama(angka):
    """Mencari faktor dari sebuah angka."""
    faktor = []

    for i in range(2, angka + 1):
        if angka % i == 0:
            faktor.append(i)

    return faktor


# ============================================================
# BAGIAN C - ANALISIS FREKUENSI DAN CHI-SQUARE
# ============================================================

# Frekuensi perkiraan huruf bahasa Indonesia.
# Nilai tidak dimaksudkan sebagai statistik resmi.
FREKUENSI_INDONESIA = {
    "A": 0.19,
    "B": 0.04,
    "C": 0.02,
    "D": 0.05,
    "E": 0.08,
    "F": 0.01,
    "G": 0.03,
    "H": 0.04,
    "I": 0.08,
    "J": 0.01,
    "K": 0.05,
    "L": 0.03,
    "M": 0.04,
    "N": 0.08,
    "O": 0.04,
    "P": 0.03,
    "Q": 0.00,
    "R": 0.06,
    "S": 0.07,
    "T": 0.05,
    "U": 0.04,
    "V": 0.01,
    "W": 0.01,
    "X": 0.00,
    "Y": 0.01,
    "Z": 0.00,
}


def bagi_kolom(ciphertext, panjang_kunci):
    """
    Membagi ciphertext berdasarkan posisi kunci.

    Jika panjang kunci = 6:
    kolom 1 -> karakter 0, 6, 12, ...
    kolom 2 -> karakter 1, 7, 13, ...
    """
    kolom = [""] * panjang_kunci

    for i, char in enumerate(ciphertext):
        kolom[i % panjang_kunci] += char

    return kolom


def geser_teks(teks, shift):
    """
    Mengembalikan teks setelah digeser ke belakang
    sebanyak shift karakter.
    """
    hasil = []

    for char in teks:
        posisi = ABC.index(char)
        hasil.append(ABC[(posisi - shift) % 26])

    return "".join(hasil)


def chi_square(teks, frekuensi):
    """
    Menghitung skor chi-square.
    Semakin kecil skor, semakin dekat distribusinya
    dengan distribusi frekuensi yang digunakan.
    """
    n = len(teks)

    if n == 0:
        return float("inf")

    skor = 0.0

    for huruf in ABC:
        aktual = teks.count(huruf)
        harapan = frekuensi.get(huruf, 0) * n

        if harapan > 0:
            skor += ((aktual - harapan) ** 2) / harapan

    return skor


def cari_kandidat_huruf(kolom):
    """
    Mencoba seluruh 26 kemungkinan pergeseran
    dan mengambil kandidat dengan chi-square terkecil.
    """
    kandidat = []

    for shift in range(26):
        hasil_geser = geser_teks(kolom, shift)
        skor = chi_square(hasil_geser, FREKUENSI_INDONESIA)

        kandidat.append(
            {
                "huruf": ABC[shift],
                "shift": shift,
                "skor": skor,
            }
        )

    kandidat.sort(key=lambda x: x["skor"])

    return kandidat


def analisis_kunci(ciphertext, panjang_kunci):
    """
    Menganalisis setiap kolom dan mengambil kandidat
    huruf dengan skor chi-square terkecil.
    """
    kolom = bagi_kolom(ciphertext, panjang_kunci)
    hasil = []

    for nomor, teks in enumerate(kolom, start=1):
        kandidat = cari_kandidat_huruf(teks)

        hasil.append(
            {
                "kolom": nomor,
                "teks": teks,
                "kandidat": kandidat[0],
            }
        )

    return hasil


# ============================================================
# BAGIAN D - ANALISIS DESAIN LOGIN
# ============================================================

def hash_sha256(password):
    """Menghasilkan SHA-256 dari password."""
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def simulasi_login(password_input, hash_database):
    """
    Simulasi login sederhana.

    Password input di-hash kemudian dibandingkan
    dengan hash yang tersimpan.
    """
    hash_input = hash_sha256(password_input)

    return hash_input == hash_database


def demo_login():
    """
    Contoh sederhana bagaimana password diproses
    sebelum dibandingkan dengan database.
    """
    password = "Kampus123!"

    hash_database = hash_sha256(password)

    print("\n=== SIMULASI LOGIN ===")
    print("Password asli       :", password)
    print("SHA-256 di database :", hash_database)

    berhasil = simulasi_login(
        "Kampus123!",
        hash_database
    )

    print("Hasil login         :", "Berhasil" if berhasil else "Gagal")


# ============================================================
# PROGRAM UTAMA
# ============================================================

def main():

    print("=" * 60)
    print("KRIPTOGRAFI MINGGU 2")
    print("VIGENERE CIPHER DAN DESAIN LOGIN")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Verifikasi Vigenere
    # --------------------------------------------------------

    print("\n[1] VERIFIKASI VIGENERE")

    ciphertext_hasil = encrypt_vigenere(
        PLAINTEXT,
        KEY
    )

    plaintext_hasil = decrypt_vigenere(
        ciphertext_hasil,
        KEY
    )

    print("Plaintext :", PLAINTEXT)
    print("Key       :", KEY)
    print("Ciphertext:", ciphertext_hasil)
    print("Dekripsi  :", plaintext_hasil)

    # --------------------------------------------------------
    # 2. Kasiski Examination
    # --------------------------------------------------------

    print("\n[2] KASISKI EXAMINATION")

    pengulangan = cari_pengulangan(
        CIPHERTEXT,
        panjang=3
    )

    jumlah = 0

    for teks, posisi in pengulangan.items():
        jarak = hitung_jarak(posisi)

        print(
            f"{teks} -> posisi {posisi}, "
            f"jarak {jarak}"
        )

        jumlah += 1

        if jumlah >= 10:
            break

    # Contoh analisis kandidat panjang kunci.
    print("\nKandidat panjang kunci:")
    print("2, 3, 4, 5, 6, ...")
    print("Dalam percobaan ini digunakan kandidat: 6")

    # --------------------------------------------------------
    # 3. Membagi ciphertext menjadi kolom
    # --------------------------------------------------------

    print("\n[3] PEMBAGIAN KOLOM")

    panjang_kunci = 6
    kolom = bagi_kolom(
        CIPHERTEXT,
        panjang_kunci
    )

    for nomor, teks in enumerate(kolom, start=1):
        print(f"Kolom {nomor}: {teks}")

    # --------------------------------------------------------
    # 4. Chi-square
    # --------------------------------------------------------

    print("\n[4] ANALISIS CHI-SQUARE")

    hasil_analisis = analisis_kunci(
        CIPHERTEXT,
        panjang_kunci
    )

    kandidat_kunci = ""

    for hasil in hasil_analisis:
        kandidat = hasil["kandidat"]

        kandidat_kunci += kandidat["huruf"]

        print(
            f"Kolom {hasil['kolom']} -> "
            f"{kandidat['huruf']} "
            f"(skor {kandidat['skor']:.2f})"
        )

    print("\nKandidat kunci hasil analisis:", kandidat_kunci)

    # --------------------------------------------------------
    # 5. Dekripsi ciphertext
    # --------------------------------------------------------

    print("\n[5] DEKRIPSI")

    plaintext = decrypt_vigenere(
        CIPHERTEXT,
        KEY
    )

    print("Key      :", KEY)
    print("Plaintext:", plaintext)

    # --------------------------------------------------------
    # 6. Analisis login
    # --------------------------------------------------------

    demo_login()

    print("\n" + "=" * 60)
    print("SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    main()