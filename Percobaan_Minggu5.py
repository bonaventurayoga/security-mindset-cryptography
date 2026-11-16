"""
Simulasi Key Exchange: Diffie-Hellman, RSA toy, dan skenario MITM
Dibuat untuk Catatan Kriptografi Minggu 5 - Bonaventura Yoga Cahya Nugraha
"""

import random

# ---------- Bagian 1: Diffie-Hellman ----------
def dh_generate_public(secret, g, p):
    return pow(g, secret, p)

def dh_compute_shared(their_public, my_secret, p):
    return pow(their_public, my_secret, p)

def demo_diffie_hellman():
    p, g = 23, 5
    alice_secret = random.randint(2, p - 2)
    bob_secret = random.randint(2, p - 2)

    alice_public = dh_generate_public(alice_secret, g, p)
    bob_public = dh_generate_public(bob_secret, g, p)

    alice_key = dh_compute_shared(bob_public, alice_secret, p)
    bob_key = dh_compute_shared(alice_public, bob_secret, p)

    print(f"[DH] Alice secret={alice_secret}, public A={alice_public}")
    print(f"[DH] Bob   secret={bob_secret}, public B={bob_public}")
    print(f"[DH] Shared key Alice={alice_key}, Bob={bob_key}, cocok={alice_key == bob_key}")
    return alice_key, bob_key


# ---------- Bagian 2: Simulasi MITM pada DH ----------
def demo_mitm_dh():
    p, g = 23, 5
    alice_secret = random.randint(2, p - 2)
    bob_secret = random.randint(2, p - 2)
    mallory_secret_a = random.randint(2, p - 2)  # dipakai Mallory saat bicara ke Alice
    mallory_secret_b = random.randint(2, p - 2)  # dipakai Mallory saat bicara ke Bob

    alice_public = dh_generate_public(alice_secret, g, p)
    bob_public = dh_generate_public(bob_secret, g, p)

    # Mallory mencegat dan mengganti nilai publik
    fake_public_to_bob = dh_generate_public(mallory_secret_a, g, p)
    fake_public_to_alice = dh_generate_public(mallory_secret_b, g, p)

    alice_key = dh_compute_shared(fake_public_to_alice, alice_secret, p)
    bob_key = dh_compute_shared(fake_public_to_bob, bob_secret, p)

    mallory_key_with_alice = dh_compute_shared(alice_public, mallory_secret_a, p)
    mallory_key_with_bob = dh_compute_shared(bob_public, mallory_secret_b, p)

    print(f"[MITM] Alice mengira shared key dengan Bob = {alice_key}")