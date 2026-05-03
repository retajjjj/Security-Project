import hashlib
import random
import json
from module_3 import sign, verify
from module_2 import encrypt, decrypt, hashPassword, loadVault, saveVault
from module_1 import load_private_key, load_public_key


mock_vault = [
    {"website": "github.com", "username": "alice", "password": "pass123"}
]


#***********************************************************************************
#key exchange phase
#***********************************************************************************
def send(data:dict):
    with open("a_send_data_to_b.json", 'w') as f:
        json.dump(data, f, indent=2)
    
def recieve():
    with open("a_recieve_data_from_b.json", 'r') as f:
        return json.load(f)
    
def make_signed_package(data: dict, private_key):
    data_string = json.dumps(data, sort_keys=True)   
    signature = sign(data_string, private_key)        
    return {"data": data, "signature": signature}

def verify_signed_package(package: dict, public_key):
    data_string = json.dumps(package["data"], sort_keys=True)
    return verify(data_string, package["signature"], public_key)

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


def transfer_phase(vault_name, master_password, session_key, private_gamal, public_gamal):
    
    plain_vault_data = loadVault(master_password, vault_name, public_gamal)
    cipher_vault = saveVault(session_key,vault_name, plain_vault_data, private_gamal)
    #send(cipher_vault)
    #return cipher_vault

#***********************************************************************************
#import phase
#***********************************************************************************
def import_phase(vault_name, master_password, session_key, private_gamal ,public_gamal):
    
    input("press enter when you recieve the public key from the other device")
    #recieve(cipher_vault)
    
    plain_vault = loadVault(session_key, vault_name, public_gamal)
    cipher_vault = saveVault(master_password, vault_name, plain_vault, private_gamal)
    
    
#***********************************************************************************
#Main function
#***********************************************************************************

def get_vault_from_username(username):
    return "vault_file"



def main_transfer(username, master_password, username_b):
    
    #read elgamal xa,ya, yb
    xa = load_private_key(username, master_password)
    ya = load_public_key(username)
    yb = load_public_key(username_b)

    vault = get_vault_from_username(username)
    
    session_key = key_exchange_phase(xa, yb, ya["alpha"], ya["p"])
    signed_vault = transfer_phase(vault, master_password, session_key, xa, yb)
    
    
def main_import(username, master_password, username_b):
    
    xa = load_private_key(username, master_password)
    ya = load_public_key(username)
    yb = load_public_key(username_b)
    
    
    vault = get_vault_from_username(username)
    
    session_key = key_exchange_phase(xa, yb,ya["alpha"], ya["p"])
    import_phase(vault, master_password, session_key, xa)
    
    
    
    