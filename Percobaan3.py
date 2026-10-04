import hashlib
import hmac


KUNCI_SERVER = b"kunci-latihan-kantin"  # hanya contoh untuk latihan


def hmac_sha256(teks: str, kunci: bytes) -> str:
    return hmac.new(
        kunci,
        teks.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def verify_hmac(teks: str, hmac_kiriman: str) -> bool:
    hmac_server = hmac_sha256(teks, KUNCI_SERVER)

    return hmac.compare_digest(
        hmac_server,
        hmac_kiriman
    )


def status(ok: bool) -> str:
    return "DITERIMA" if ok else "DITOLAK"


kupon_asli = "KUPON|nadia|5000"
hmac_asli = hmac_sha256(kupon_asli, KUNCI_SERVER)

nilai_naik = "KUPON|nadia|50000"
pemilik_diganti = "KUPON|raka|5000"


uji = [
    (
        "[1] kupon asli",
        kupon_asli,
        hmac_asli
    ),

    (
        "[2] nilai dinaikkan, HMAC lama",
        nilai_naik,
        hmac_asli
    ),

    (
        "[3] pemilik diganti, HMAC lama",
        pemilik_diganti,
        hmac_asli
    ),

    (
        "[4] nilai dinaikkan, kunci tebakan",
        nilai_naik,
        hmac_sha256(
            nilai_naik,
            b"tebakan"
        )
    ),

    (
        "[5] dibuat pemegang kunci (server)",
        nilai_naik,
        hmac_sha256(
            nilai_naik,
            KUNCI_SERVER
        )
    ),
]


for nama, isi, tanda in uji:
    print(
        f"{nama:42s}->",
        status(verify_hmac(isi, tanda))
    )