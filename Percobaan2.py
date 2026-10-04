import hashlib


def hash_sha256(teks: str) -> str:
    return hashlib.sha256(
        teks.encode("utf-8")
    ).hexdigest()


def verify_hash(teks: str, hash_kiriman: str) -> bool:
    return hash_sha256(teks) == hash_kiriman


def status(ok: bool) -> str:
    return "DITERIMA" if ok else "DITOLAK"


kupon_asli = "KUPON|nadia|5000"
hash_asli = hash_sha256(kupon_asli)

rusak = "KUPON|nadia|500"       # angka terakhir hilang di perjalanan
palsu = "KUPON|nadia|50000"     # nilai diubah oleh penyerang


print(
    "[1] kupon asli                   ->",
    status(verify_hash(kupon_asli, hash_asli))
)

print(
    "[2] rusak di jalan, hash lama    ->",
    status(verify_hash(rusak, hash_asli))
)

print(
    "[3] diedit, hash lama            ->",
    status(verify_hash(palsu, hash_asli))
)

print(
    "[4] diedit, hash dihitung ulang  ->",
    status(verify_hash(palsu, hash_sha256(palsu)))
)