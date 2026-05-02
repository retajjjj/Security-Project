from secrets import randbelow
import json
from hashlib import sha256
from math import gcd


# Stub Module 1 
def stub_generate_keypair():
    # Tiny prime for fast testing. Replace with 1024-bit for real runs.
    p = 30803  # any small prime
    alpha = 2  # ideally a primitive root mod p; 2 works for many primes
    x = randbelow(p - 2) + 1
    y = pow(alpha, x, p)
    private_key = {"p": p, "alpha": alpha, "x": x}
    public_key  = {"p": p, "alpha": alpha, "y": y}
    return private_key, public_key

# Stub Module 2
def stub_encrypted_vault():
    return "a3f8b2c1d4e5fakeencryptedvaultcontents"


# Module 3
#helpers
def extended_euclidean(a, b) -> tuple[int, int, int]:
    """Return (g, x, y) with  a*x + b*y == g == gcd(a, b).
    """
    r_old, r_cur = a, b
    x_old, x_cur = 1, 0
    y_old, y_cur = 0, 1

    while r_cur != 0:
        q = r_old // r_cur                         
        r_old, r_cur = r_cur, r_old - q * r_cur    
        x_old, x_cur = x_cur, x_old - q * x_cur   
        y_old, y_cur = y_cur, y_old - q * y_cur   

    # when r_cur == 0, r_old holds gcd and x_old, y_old hold the coefficients
    return r_old, x_old, y_old

def find_modular_inverse(a, b) -> int:
    """Compute the modular multiplicative inverse of e mod phi.
    """

    g, x, y = extended_euclidean(a, b)
    if g != 1:
        raise ValueError("Inverse does not exist")
    
    return x % b #ensure psotive

def parse_signature(sig_string:str)->tuple[int,int]:
    r_str, s_str = sig_string.split(":")
    return int(r_str), int(s_str)

def serialize_signature(r,s):
    return f"{r}:{s}"

#sign and verify
def sign(vault_string,priv):
    
    h_int = int.from_bytes(sha256(vault_string.encode("utf-8")).digest(), "big") #hashed vault string converted to int
    #generate random nonce k
    while True:
        k = randbelow(priv["p"]-2) +1 #k in [1,p-2]
        if gcd(k,priv["p"]-1) ==1:
            break
    r = pow(priv["alpha"],k,priv["p"])
    k_inv = find_modular_inverse(k,priv["p"]-1)
    s = ((h_int-(priv["x"])*r)*k_inv) % (priv["p"] - 1)
    if s == 0:                              
        return sign(vault_string, priv) 
    return serialize_signature(r,s)

def verify(vault_string,sig_string, pub):
    try:
        r, s = parse_signature(sig_string)
    except (ValueError, AttributeError, TypeError):
        return False
    if not (0 < r < pub["p"]):
        return False
    h_int = int.from_bytes(sha256(vault_string.encode("utf-8")).digest(), "big")
    c1 = pow(pub["alpha"],h_int,pub["p"])
    c2 = (pow(pub["y"], r, pub["p"]) * pow(r, s, pub["p"])) % pub["p"]
    return c1 == c2


