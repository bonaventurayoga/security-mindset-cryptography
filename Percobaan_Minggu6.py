"""
Eksperimen Hash Function: avalanche effect, integritas vs HMAC, password hashing
Dibuat untuk Catatan Kriptografi Minggu 6 - Bonaventura Yoga Cahya Nugraha
"""

import hashlib
import hmac
import os
import secrets
import statistics


# ---------- Eksperimen 1: Avalanche effect secara statistik ----------
def flip_one_bit(data: bytes, bit_index: int) -> bytes:
    mutated = bytearray(data)
    mutated[bit_index // 8] ^= 1 << (bit_index % 8)
    return bytes(mutated)


def percent_bits_changed(digest_a: bytes, digest_b: bytes) -> float:
    total_bits = len(digest_a) * 8
    diff_bits = sum(bin(x ^ y).count("1") for x, y in zip(digest_a, digest_b))
    return diff_bits / total_bits * 100


def eksperimen_avalanche(trials: int = 500, seed: int = 2027):
    rng = __import__("random").Random(seed)
    results = {"sha256": [], "sha3_256": []}

    for _ in range(trials):
        message = rng.randbytes(24)
        target_bit = rng.randrange(24 * 8)
        mutated = flip_one_bit(message, target_bit)

        for algo in results:
            d1 = hashlib.new(algo, message).digest()
            d2 = hashlib.new(algo, mutated).digest()
            results[algo].append(percent_bits_changed(d1, d2))

    print("=== Eksperimen 1: Avalanche Effect ===")
    for algo, values in results.items():
        print(f"{algo}: rata-rata={statistics.mean(values):.2f}%  "
              f"std={statistics.stdev(values):.2f}%  "
              f"min={min(values):.1f}%  maks={max(values):.1f}%")

    # Contoh satu pasang untuk ilustrasi
    contoh_a, contoh_b = b"SayHello", b"SayHallo"
    pct = percent_bits_changed(hashlib.sha256(contoh_a).digest(), hashlib.sha256(contoh_b).digest())
    print(f"\nContoh: '{contoh_a.decode()}' vs '{contoh_b.decode()}' -> {pct:.1f}% bit berbeda")


# ---------- Eksperimen 2: Hash biasa vs HMAC untuk integritas ----------
def eksperimen_integritas_hmac():
    print("\n=== Eksperimen 2: Hash Biasa vs HMAC ===")
    dokumen_asli = b"KONTRAK|nilai=50000000|pihak=A-B"

    # Skenario 1: hash biasa, penyerang ubah data DAN digest
    digest_resmi = hashlib.sha256(dokumen_asli).hexdigest()
    dokumen_diubah = b"KONTRAK|nilai=50000000000|pihak=A-B"
    digest_palsu = hashlib.sha256(dokumen_diubah).hexdigest()  # penyerang hitung ulang

    print(f"Digest resmi   : {digest_resmi}")
    print(f"Digest palsu   : {digest_palsu}")
    print("-> Penyerang BISA membuat digest baru yang cocok dengan dokumen palsunya sendiri.")
    print("   Hash biasa gagal mendeteksi ini kalau korban hanya menerima digest dari penyerang.")

    # Skenario 2: HMAC, penyerang tidak punya kunci
    kunci_sah = secrets.token_bytes(32)
    tag_sah = hmac.new(kunci_sah, dokumen_asli, hashlib.sha256).hexdigest()

    kunci_tebakan = secrets.token_bytes(32)
    tag_penyerang = hmac.new(kunci_tebakan, dokumen_diubah, hashlib.sha256).hexdigest()
    tag_dihitung_penerima = hmac.new(kunci_sah, dokumen_diubah, hashlib.sha256).hexdigest()

    print(f"\nTag HMAC sah (kunci benar)     : {tag_sah}")
    print(f"Tag dari penyerang (kunci tebakan): {tag_penyerang}")
    valid = hmac.compare_digest(tag_dihitung_penerima, tag_penyerang)
    print(f"Verifikasi penerima: {'LOLOS' if valid else 'DITOLAK'} (tag penyerang tidak cocok tanpa kunci asli)")


# ---------- Eksperimen 3: Password hashing ----------
def eksperimen_password_hashing():
    print("\n=== Eksperimen 3: Password Hashing ===")
    password = "sayang123"
    pengguna = {"rina": password, "dedi": password, "wulan": "K0pi&Senja!"}

    print("SHA-256 tanpa salt:")
    for nama, pw in pengguna.items():
        print(f"  {nama}: {hashlib.sha256(pw.encode()).hexdigest()[:24]}...")
    print("-> rina dan dedi punya hash identik: penyerang tahu mereka pakai password sama.")

    print("\nSHA-256 dengan salt acak per pengguna:")
    for nama, pw in pengguna.items():
        salt = os.urandom(16)
        h = hashlib.sha256(salt + pw.encode()).hexdigest()
        print(f"  {nama}: salt={salt.hex()[:10]}... hash={h[:24]}...")
    print("-> Hash sekarang berbeda walau password sama, tapi SHA-256 tetap cepat untuk ditebak.")

    try:
        import bcrypt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10))
        print(f"\nbcrypt (cost=10): {hashed.decode()}")
        print(f"Verifikasi password benar : {bcrypt.checkpw(password.encode(), hashed)}")
        print(f"Verifikasi password salah : {bcrypt.checkpw(b'salah', hashed)}")
    except ImportError:
        print("\n(bcrypt belum terpasang - jalankan: pip install bcrypt)")

    wordlist_mini = ["123456", "sayang123", "password", "qwerty123"]
    salt = os.urandom(16)
    target = hashlib.sha256(salt + password.encode()).digest()
    for i, kata in enumerate(wordlist_mini, 1):
        if hashlib.sha256(salt + kata.encode()).digest() == target:
            print(f"\nSerangan kamus (SHA-256+salt): ditemukan di percobaan ke-{i} -> '{kata}'")
            break


if __name__ == "__main__":
    eksperimen_avalanche()
    eksperimen_integritas_hmac()
    eksperimen_password_hashing()