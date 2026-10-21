"""
Percobaan Minggu 3 - Matematika Kriptografi
Topik: modulo, bilangan prima, inverse modulo, cipher, trapdoor, brute force, RSA mini
Catatan: butuh Python 3.8+ (pow(e, -1, phi) tidak jalan di versi lebih lama)
"""
import time

# ------------------------------------------------------------
# 1. MODULO
# ------------------------------------------------------------
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


def uraikan_modulo(a, n):
    """Tampilkan a = q x n + r, sama seperti definisi di materi."""
    q, r = divmod(a, n)
    print(f"{a} mod {n} = {r}  (karena {a} = {q} x {n} + {r})")
    return r


def hari_setelah(mulai, selisih):
    """Modulo 7 dipakai sebagai 'jam' untuk hari dalam seminggu."""
    posisi = HARI.index(mulai)
    return HARI[(posisi + selisih) % 7]


def demo_modulo():
    print("=== 1. MODULO ===")
    uraikan_modulo(29, 7)
    uraikan_modulo(100, 12)
    uraikan_modulo(45, 6)
    print("100 hari setelah Rabu  :", hari_setelah("Rabu", 100))
    print("29 hari setelah Jumat  :", hari_setelah("Jumat", 29))
    print("-3 mod 26 di Python    :", -3 % 26)


# ------------------------------------------------------------
# 2. BILANGAN PRIMA (Sieve of Eratosthenes)
# ------------------------------------------------------------
def sieve(batas):
    prima = [True] * (batas + 1)
    prima[0] = prima[1] = False
    for i in range(2, int(batas ** 0.5) + 1):
        if prima[i]:
            for kelipatan in range(i * i, batas + 1, i):
                prima[kelipatan] = False
    return [i for i, p in enumerate(prima) if p]


def demo_prima():
    print("\n=== 2. BILANGAN PRIMA ===")
    semua = sieve(50)
    print("Prima di bawah 50   :", semua, f"(total {len(semua)})")
    antara = [p for p in semua if p >= 20]
    print("Prima 20 sampai 50  :", antara, f"(total {len(antara)})")


# ------------------------------------------------------------
# 3. INVERSE MODULO (Extended Euclidean Algorithm)
# ------------------------------------------------------------
def egcd(a, b):
    """Mengembalikan (gcd, x, y) dengan a*x + b*y = gcd."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def inverse_modulo(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        return None
    return x % n


def demo_inverse():
    print("\n=== 3. INVERSE MODULO ===")
    for a in [3, 5, 7, 11, 2, 13]:
        inv = inverse_modulo(a, 26)
        if inv is None:
            print(f"a = {a:>2} : tidak ada inverse (gcd = {egcd(a, 26)[0]})")
        else:
            print(f"a = {a:>2} : inverse = {inv:>2}  (cek: {a} x {inv} = {a * inv}, "
                  f"mod 26 = {(a * inv) % 26})")
    valid = [a for a in range(1, 26) if egcd(a, 26)[0] == 1]
    print("Kunci valid mod 26  :", valid, f"(total {len(valid)})")


# ------------------------------------------------------------
# 4. CIPHER: Caesar (additive) dan Multiplicative
# ------------------------------------------------------------
def ubah_huruf(teks, fungsi):
    """Terapkan fungsi(x) ke setiap huruf (A=0..Z=25), simbol dibiarkan."""
    hasil = []
    for ch in teks:
        if ch.isalpha():
            dasar = 65 if ch.isupper() else 97
            hasil.append(chr(fungsi(ord(ch) - dasar) % 26 + dasar))
        else:
            hasil.append(ch)
    return "".join(hasil)


def caesar_enkripsi(teks, k):
    return ubah_huruf(teks, lambda x: x + k)


def caesar_dekripsi(teks, k):
    return ubah_huruf(teks, lambda x: x - k)


def mult_enkripsi(teks, k):
    return ubah_huruf(teks, lambda x: x * k)


def mult_dekripsi(teks, k):
    inv = inverse_modulo(k, 26)
    if inv is None:
        raise ValueError(f"Kunci {k} tidak punya inverse mod 26 "
                         f"(gcd({k}, 26) = {egcd(k, 26)[0]})")
    return ubah_huruf(teks, lambda x: x * inv)


def demo_cipher():
    print("\n=== 4. CIPHER ===")
    print("-- Caesar (aktivitas kelas) --")
    for kata, k in [("KUNCI", 5), ("RAHASIA", 3), ("AMAN", 7)]:
        c = caesar_enkripsi(kata, k)
        print(f"{kata:<8} shift {k} -> {c:<8} (balik: {caesar_dekripsi(c, k)})")

    print("-- Multiplicative --")
    pesan = "HELLO"
    for k in [3, 5, 7]:
        c = mult_enkripsi(pesan, k)
        print(f"key {k}: {pesan} -> {c} -> {mult_dekripsi(c, k)}")

    print("-- Key yang tidak valid --")
    # pasangan huruf yang bertabrakan: key 2 -> A & N, key 13 -> B & D
    for k, uji in [(2, "AN"), (13, "BD")]:
        c = mult_enkripsi(uji, k)
        print(f"key {k}: '{uji}' jadi '{c}' (dua huruf berbeda jadi sama)")
        try:
            mult_dekripsi(c, k)
        except ValueError as err:
            print("        error:", err)


# ------------------------------------------------------------
# 5. TRAPDOOR: perkalian vs faktorisasi
# ------------------------------------------------------------
def faktorkan(n):
    f = 2
    while f * f <= n:
        if n % f == 0:
            return f, n // f
        f += 1
    return None


def demo_trapdoor():
    print("\n=== 5. TRAPDOOR ===")
    for angka in [77, 91, 391]:
        print(f"{angka} = {faktorkan(angka)}")

    p, q = 1000003, 1000033
    awal = time.perf_counter()
    n = p * q
    waktu_kali = time.perf_counter() - awal

    awal = time.perf_counter()
    hasil = faktorkan(n)
    waktu_faktor = time.perf_counter() - awal

    print(f"p x q = {n}")
    print(f"faktorisasi = {hasil}")
    print(f"waktu kali     : {waktu_kali:.8f} detik")
    print(f"waktu faktor   : {waktu_faktor:.8f} detik")
    print(f"selisih        : sekitar {waktu_faktor / waktu_kali:,.0f}x lebih lama")


# ------------------------------------------------------------
# 6. BRUTE FORCE AES-128 (mengikuti asumsi materi: 10^18 percobaan/detik)
# ------------------------------------------------------------
def demo_bruteforce():
    print("\n=== 6. BRUTE FORCE AES-128 ===")
    kecepatan = 10 ** 18
    detik_per_tahun = 365.25 * 24 * 3600
    usia_semesta = 1.38e10
    tahun = 2 ** 128 / kecepatan / detik_per_tahun
    print(f"ruang kunci   : 2^128 = {2 ** 128:,}")
    print(f"waktu         : {tahun:.2e} tahun")
    print(f"perbandingan  : {tahun / usia_semesta:.0f}x usia alam semesta")


# ------------------------------------------------------------
# 7. RSA MINI (contoh bonus materi: p=11, q=13)
# ------------------------------------------------------------
def demo_rsa():
    print("\n=== 7. RSA MINI ===")
    p, q, e = 11, 13, 7
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)          # inverse e terhadap phi(n)
    print(f"n = {n}, phi(n) = {phi}, e = {e}, d = {d}")
    print(f"cek 7 x {d} = {e * d}, mod {phi} = {(e * d) % phi}")

    m = 9
    c = pow(m, e, n)
    kembali = pow(c, d, n)
    print(f"pesan {m} -> cipher {c} -> dekripsi {kembali}")

    # kunci publik (7, 143) dipecah paksa karena n kecil
    pq = faktorkan(n)
    phi_curian = (pq[0] - 1) * (pq[1] - 1)
    print(f"n = {n} bisa difaktorkan jadi {pq}, d curian = {pow(e, -1, phi_curian)}")


if __name__ == "__main__":
    demo_modulo()
    demo_prima()
    demo_inverse()
    demo_cipher()
    demo_trapdoor()
    demo_bruteforce()
    demo_rsa()
