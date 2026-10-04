import base64


def encode_base64(teks: str) -> str:
    return base64.b64encode(
        teks.encode("utf-8")
    ).decode("ascii")


def decode_base64(kode: str) -> str:
    return base64.b64decode(
        kode
    ).decode("utf-8")


def server_terima(kode: str) -> bool:
    jenis, pemilik, nilai = decode_base64(kode).split("|")
    return jenis == "KUPON" and nilai.isdigit()


kupon_asli = "KUPON|nadia|5000"
kode_asli = encode_base64(kupon_asli)

# Penyerang membaca isi Base64, mengubah nilainya,
# lalu melakukan encode kembali
terbaca = decode_base64(kode_asli)
diedit = terbaca.replace("|5000", "|50000")
kode_palsu = encode_base64(diedit)


print("Kupon asli        :", kupon_asli)
print("Kode di aplikasi  :", kode_asli)
print("Setelah di-decode :", terbaca)
print("Setelah diedit    :", diedit)
print("Kode palsu        :", kode_palsu)

print(
    "Server menerima kode asli ?",
    server_terima(kode_asli)
)

print(
    "Server menerima kode palsu?",
    server_terima(kode_palsu)
)