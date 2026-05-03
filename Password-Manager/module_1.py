

import os

import random
import json

import hashlib

def _encrypt_private_key(data: dict, master_password: str) -> str:
    plaintext = json.dumps(data).encode()
    key = hashlib.sha256(master_password.encode()).digest()
    encrypted = bytes(plaintext[i] ^ key[i % len(key)] 
                     for i in range(len(plaintext)))
    return encrypted.hex()

def _decrypt_private_key(encrypted: str, master_password: str) -> dict:
    encrypted_bytes = bytes.fromhex(encrypted)
    key = hashlib.sha256(master_password.encode()).digest()
    plaintext = bytes(encrypted_bytes[i] ^ key[i % len(key)] 
                     for i in range(len(encrypted_bytes)))
    return json.loads(plaintext.decode())



def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean Algorithm.

    Returns (g, x, y) such that  a*x + b*y == g == gcd(a, b).
    """
    # Variables initialization for the extended Euclidean algorithm.
    # Matching the lecture table (slide 12):
    #   r_{i-2}, r_{i-1}  start as  a, b
    #   x_{i-2}, x_{i-1}  start as  1, 0
    #   y_{i-2}, y_{i-1}  start as  0, 1
    
    r_old, r_cur = a, b
    x_old, x_cur = 1, 0
    y_old, y_cur = 0, 1

    # TODO: Implement the extended Euclidean algorithm.
    while r_cur != 0:
        q = r_old // r_cur 
        
        
        
        r_old, r_cur = r_cur, r_old - q * r_cur
        x_old, x_cur = x_cur, x_old - q * x_cur
        y_old, y_cur = y_cur, y_old - q * y_cur

    return r_old, x_old, y_old
    


def mod_inverse(e: int, phi: int) -> int:
    """Compute the modular multiplicative inverse of e mod phi.
    """

    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Inverse does not exist")
    # x is the the value of e inverse
    return x % phi


def load_params(filepath="deffie-helman-params.txt"):

    lines = []
    with open(filepath) as f:
        lines = f.readlines()       
        p = int(lines[0].strip())
        alpha = int(lines[1].strip())

    return p, alpha
    


def generate_keypair(username: str, master_password: str) -> dict:
    p, alpha = load_params()
    x = random.randint(2, p - 2) # private key
    y = pow(alpha, x, p) #public
    
    private_key = {"p": p, "alpha": alpha, "x": x}
    public_key  = {"p": p, "alpha": alpha, "y": y}
    
    os.makedirs("Password-Manager/keys", exist_ok=True)
    
    encrypted = _encrypt_private_key(private_key, master_password)
    with open(f"Password-Manager/keys/{username}_private.json", "w") as f:
        json.dump({"encrypted_key": encrypted}, f)
    
    # Public key → plain
    with open(f"Password-Manager/keys/{username}_public.json", "w") as f:
        json.dump(public_key, f)
    
    return public_key 

def sign(hash_value: int, username: str, master_password: str) -> tuple:


    private_key = load_private_key(username, master_password)
    p     = private_key["p"]
    alpha = private_key["alpha"]
    x     = private_key["x"]
    

    while True:
        k = random.randint(2, p - 2)
        g, _, _ = extended_gcd(k, p - 1)   # first return value is gcd
        if g == 1:
            break
    
   
    r = pow(alpha, k, p)

    k_inv = mod_inverse(k, p - 1)
    s = ((hash_value - x * r) * k_inv) % (p - 1)
    
    return (r, s)

def verify(hash_value: int, signature: tuple, username: str) -> bool:
    # Load public key internally
    public_key = load_public_key(username)
  
    p     = public_key["p"]
    alpha = public_key["alpha"]
    y     = public_key["y"]
    r, s = signature
    if not (1 <= r < p):
        return False
    left = pow(alpha, hash_value, p)
    right = (pow(y, r, p) * pow(r, s, p)) % p
    return left == right              
  

def load_private_key(username: str, master_password: str) -> dict:
    with open(f"Password-Manager/keys/{username}_private.json") as f:
        data = json.load(f)
    return _decrypt_private_key(data["encrypted_key"], master_password)

def load_public_key(username: str) -> dict:
    with open(f"Password-Manager/keys/{username}_public.json") as f:
        return json.load(f)
    



if __name__ == "__main__":
    import hashlib
    
    print("=" * 50)
    
    # TEST 1: Generate keys
    print("\n[TEST 1] Generating keys for 'alice'...")
    master_password = "mypassword123"
    pub = generate_keypair("alice", master_password)
    print(f"  Public key y = {pub['y']}")
    
    # TEST 2: Load private key back
    print("\n[TEST 2] Loading private key...")
    priv = load_private_key("alice", master_password)
    print(f"  Private key x = {priv['x']}")
    
    # TEST 3: Wrong password should fail
    print("\n[TEST 3] Wrong password should fail...")
    try:
        priv_bad = load_private_key("alice", "wrongpassword")
        print("  ERROR: Should have failed!")
    except Exception as e:
        print(f"  Correctly rejected wrong password!")
    
    # TEST 4: Sign a hash
    print("\n[TEST 4] Signing a hash...")
    fake_hash = int(hashlib.sha256(b"test vault data").hexdigest(), 16) % (pub['p'] - 1)
    sig = sign(fake_hash, "alice", master_password)
    print(f"  Signature = {sig}")
    
    # TEST 5: Verify signature
    print("\n[TEST 5] Verifying signature...")
    result = verify(fake_hash, sig, "alice")
    print(f"  Valid? = {result}")
    
    # TEST 6: Tampered hash should fail
    print("\n[TEST 6] Tampered hash should fail...")
    result2 = verify(fake_hash + 1, sig, "alice")
    print(f"  Tampered valid? = {result2}")
    
    print("\n" + "=" * 50)
    print("ALL TESTS DONE")