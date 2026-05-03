import hashlib
import random
import json
from module_3 import sign, verify
"""imputs: vault,
            el gamal private a, el gamal public a
            el gamal public b
            a,q params file
"""
# mock things that are dependent on other modules

def aes_encrypt(plain, key):
    return "xyz"

def aes_decrypt(cipher, key):
    return "abc"

mock_vault = [
    {"website": "github.com", "username": "alice", "password": "pass123"}
]


#***********************************************************************************
#key exchange phase
#***********************************************************************************
def send(data):
    with open("send_data.json", 'w') as f:
        json.dump(data, f, indent=2)
    
def recieve():
    with open("recieve_data.json", 'r') as f:
        return json.load(f)
    
def make_signed_package(data: dict, private_key):
    data_string = json.dumps(data, sort_keys=True)   
    signature = sign(data_string, private_key)        
    return {"data": data, "signature": signature}

def verify_signed_package(package: dict, public_key):
    data_bytes = json.dumps(package["data"], sort_keys=True)
    return verify(data_bytes, package["signature"], public_key)

def calculate_session_key(shared_secret):
    secret_bytes = shared_secret.to_bytes(
        (shared_secret.bit_length() + 7) // 8, byteorder='big'
    )
    return hashlib.sha256(secret_bytes).digest()
   
def key_exchange_phase(private_gamal, public_gamal, a,q):
    
    #generate public and private key
    xa = random.randint(2, q - 2) # <q
    ya = pow(a,xa,q)

    #sign the public key (ya) with elgamal private_key
    signed_ya = make_signed_package(ya, private_gamal)
    
    #send signed_ya
    send(signed_ya)
    input("press enter when you recieve the public key from the other device")
    
    #receive signed_yb
    signed_yb = recieve()
    
    #verify the signed_yb
    #note when gamal module is made replace the signed_ya = signed_yb 
    if not verify_signed_package(signed_ya , public_gamal):
        raise Exception("Error in sending the public key. the signature is not verified")
    
    #get yb
    #note when gamal module is made replace the signed_ya = signed_yb 
    yb = signed_ya["data"]
    
    #compute shared secret key
    K = pow(yb, xa, q)

    #compute aes session key by hasing the secret key
    session_key = calculate_session_key(K)
    return session_key

#***********************************************************************************
#Transfer Phase
#***********************************************************************************
def calculate_data_key(master_password):
    return hashlib.sha256(master_password.encode()).digest()

def encrypt_package(vault, session_key):
    return aes_encrypt
    
def decrypt_package(vault, data_key):
    return aes_decrypt

def transfer_phase(vault, master_password, session_key, private_gamal):
    data_key = calculate_data_key(master_password)
    
    plain_vault = decrypt_package(vault, data_key)
    cipher_vault = encrypt_package(plain_vault, session_key)
    signed_vault = make_signed_package(cipher_vault, private_gamal)
    send(signed_vault)

#***********************************************************************************
#import phase
#***********************************************************************************
def import_phase(signed_vault, master_password, session_key, private_gamal ,public_gamal):
    input("press enter when you recieve the public key from the other device")
    recieve(signed_vault)

    if not verify_signed_package(signed_vault , public_gamal):
        raise Exception("Error in sending the public key. the signature is not verified")
    
    plain_vault = decrypt_package(signed_vault, session_key)
    cipher_vault = aes_encrypt(plain_vault, master_password)
    sign(cipher_vault, gamal_xa)
#***********************************************************************************
#Main function
#***********************************************************************************
gamal_ya = 78
gamal_xa = 12
gamal_yb = 123

def main(vault, gamal_xa, gamal_ya, gamal_yb):
    #read a and q
    lines=[]
    with open('deffie-helman-params.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    q = int(lines[0].strip())
    a = int(lines[1].strip())
    
    #note when gamal module is made replace the gamal_ya = gamal_yb 
    private_gamal = {"alpha": a, "x":gamal_xa, "p":q}
    public_gamal = {"alpha": a, "y":gamal_ya, "p":q}
    
    
    master_password = ""
    session_key = key_exchange_phase(private_gamal, public_gamal, a, q)
    signed_vault = transfer_phase(vault, master_password, session_key, private_gamal, public_gamal)
    import_phase(signed_vault, master_password, session_key, private_gamal)
    
    
    #testing module 3 functions
    ans = sign("abc", private_gamal)
    verify("abc",ans, public_gamal)