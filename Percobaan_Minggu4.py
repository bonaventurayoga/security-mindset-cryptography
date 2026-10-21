"""
Kriptografi Minggu 4: Confidentiality Primitive (Block Cipher)
Topik: kebocoran pola pada mode ECB dan perbandingannya dengan CBC/GCM.

Kebutuhan:
    pip install pycryptodome

Isi:
    Percobaan 1 : ECB mainan (hash berkunci) + analisis frekuensi
    Percobaan 2 : AES-ECB asli, pengelompokan blok, dan serangan tukar blok
    Percobaan 3 : ECB vs CBC vs GCM berdasarkan jumlah blok ciphertext unik

Catatan: kunci di bawah hanya untuk demo. Pada sistem nyata, kunci dibuat
dengan get_random_bytes() dan tidak ditulis langsung di dalam kode.
"""

import hashlib
from collections import Counter

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KUNCI = b"kunci-rahasia-16"  # tepat 16 byte (AES-128)
UKURAN_BLOK = 16


# ---------------------------------------------------------------------------
# Percobaan 1: ECB mainan
# ---------------------------------------------------------------------------
def blok_mainan(blok, kunci):
    """Pengganti block cipher: deterministik, blok + kunci sama -> output sama."""
    return hashlib.sha256((kunci + blok).encode()).hexdigest()[:8]


def ecb_mainan(pesan, kunci="rahasia", ukuran=8):
    """Pecah pesan menjadi blok, lalu enkripsi tiap blok secara independen."""
    blok = [pesan[i:i + ukuran] for i in range(0, len(pesan), ukuran)]
    return blok, [blok_mainan(b, kunci) for b in blok]


def percobaan_1():
    print("=" * 60)
    print("PERCOBAAN 1: ECB mainan")
    print("=" * 60)

    status = ["APPROVED", "REJECTED", "APPROVED",
              "APPROVED", "REJECTED", "APPROVED"]
    blok, cblok = ecb_mainan("".join(status))

    for i, (p, c) in enumerate(zip(blok, cblok), 1):
        print(f"Rekaman {i}: {p} -> {c}")

    frekuensi = Counter(cblok)
    print("\nCiphertext paling sering muncul:", frekuensi.most_common(1)[0])
    print("Jumlah ciphertext berbeda:", len(frekuensi))


# ---------------------------------------------------------------------------
# Percobaan 2: AES-ECB asli
# ---------------------------------------------------------------------------
DATA = [
    ("Andi", "APPROVED"),
    ("Budi", "REJECTED"),
    ("Citra", "APPROVED"),
    ("Dewi", "APPROVED"),
    ("Eko", "REJECTED"),
]


def susun(nama, status):
    """Satu rekaman = 2 blok 16 byte: blok nama + blok status."""
    return nama.ljust(UKURAN_BLOK).encode() + status.ljust(UKURAN_BLOK).encode()


def potong(ct):
    """Pecah byte menjadi daftar blok 16 byte."""
    return [ct[i:i + UKURAN_BLOK] for i in range(0, len(ct), UKURAN_BLOK)]


def percobaan_2():
    print("\n" + "=" * 60)
    print("PERCOBAAN 2: AES-ECB asli")
    print("=" * 60)

    ecb = AES.new(KUNCI, AES.MODE_ECB)
    tabel = [ecb.encrypt(susun(n, s)) for n, s in DATA]

    # 1) Penyerang hanya melihat blok status (blok ke-2) lalu mengelompokkannya
    kelompok = Counter(potong(r)[1].hex()[:12] for r in tabel)
    print("Kelompok blok status:", dict(kelompok))

    # 2) Cut-and-paste: tempel blok status Andi (APPROVED) ke rekaman Budi
    tabel[1] = potong(tabel[1])[0] + potong(tabel[0])[1]
    hasil = AES.new(KUNCI, AES.MODE_ECB).decrypt(tabel[1])
    print("Rekaman Budi setelah dimanipulasi:", hasil.decode().strip())


# ---------------------------------------------------------------------------
# Percobaan 3: ECB vs CBC vs GCM
# ---------------------------------------------------------------------------
PLAINTEXT = (b"APPROVED".ljust(UKURAN_BLOK) * 3) + b"REJECTED".ljust(UKURAN_BLOK)


def blok_unik(ct):
    """Jumlah blok ciphertext yang berbeda (makin sedikit = makin bocor)."""
    return len(set(potong(ct)))


def enkripsi_semua():
    ecb = AES.new(KUNCI, AES.MODE_ECB).encrypt(PLAINTEXT)
    cbc = AES.new(KUNCI, AES.MODE_CBC, get_random_bytes(16)).encrypt(PLAINTEXT)
    gcm, _tag = AES.new(KUNCI, AES.MODE_GCM).encrypt_and_digest(PLAINTEXT)
    return {"ECB": ecb, "CBC": cbc, "GCM": gcm}


def percobaan_3():
    print("\n" + "=" * 60)
    print("PERCOBAAN 3: ECB vs CBC vs GCM")
    print("=" * 60)

    total_blok = len(potong(PLAINTEXT))
    for percobaan in (1, 2):
        print(f"--- Percobaan {percobaan} ---")
        for mode, ct in enkripsi_semua().items():
            print(f"{mode}: blok unik = {blok_unik(ct)}/{total_blok} "
                  f"| {ct[:8].hex()}...")


if __name__ == "__main__":
    percobaan_1()
    percobaan_2()
    percobaan_3()
