import hashlib
import random
import json
import os
from module_3 import sign, verify
from module_2 import encrypt, decrypt, hashPassword, loadVault, saveVault
from module_1 import load_private_key, load_public_key


#***********************************************************************************
#key exchange phase
#***********************************************************************************
def send(data:dict, myusername, hisusername):
    with open(f"Password-Manager/keys/{myusername}_send_data_to_{hisusername}.json", 'w') as f:
        json.dump(data, f, indent=2)
    
def recieve(myusername, hisusername):
    with open(f"Password-Manager/keys/{hisusername}_send_data_to_{myusername}.json", 'r') as f:
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
   
def key_exchange_phase(private_gamal, public_gamal, a,q, myusername, hisusername):
    
    #generate public and private key
    xa = random.randint(2, q - 2) # <q
    ya = pow(a,xa,q)

    #sign the public key (ya) with elgamal private_key
    signed_ya = make_signed_package(ya, private_gamal)
    
    #send signed_ya
    send(signed_ya, myusername, hisusername)
    input("press enter when you recieve the public key from the other device")
    
    #receive signed_yb
    signed_yb = recieve(myusername, hisusername)
    
    #verify the signed_yb
    
    if not verify_signed_package(signed_yb , public_gamal):
        raise Exception("Error in sending the public key. the signature is not verified")
    
    #get yb
    yb = signed_yb["data"]
    
    #compute shared secret key
    K = pow(yb, xa, q)

    #compute aes session key by hasing the secret key
    session_key = calculate_session_key(K)
    return session_key

#***********************************************************************************
#Transfer Phase
#***********************************************************************************


def transfer_phase(vault_name, master_password, session_key, private_gamal, public_gamal):
    
    print("SESSION KEY (sender):", session_key.hex())
    plain_vault_data = loadVault(master_password, vault_name, public_gamal)
    
    #session_key_str = session_key.hex()
    #saveVault(session_key,vault_name, plain_vault_data, private_gamal)
    
    
    plaintext = json.dumps(plain_vault_data).encode()

    try:
        packed = encrypt(session_key, plaintext)
    except Exception:
        raise Exception("Encryption failed") 
    signature = sign(packed.hex(), private_gamal)  # add signature

    vault = {"encrypted_vault": packed.hex(), "signature": signature}
    with open(vault_name, "w") as file_object:
        json.dump(vault, file_object)
    
    """
    plain_vault_data = loadVault(master_password, vault_name, public_gamal)
    # convert session_key bytes to hex string so hashPassword can handle it
    session_key_str = session_key.hex()
    saveVault(session_key_str, vault_name, plain_vault_data, private_gamal)
    #send(json.loads(open(vault_name).read()), myusername, hisusername)
    """
    

#***********************************************************************************
#import phase
#***********************************************************************************
def import_phase(vault_name, master_password, session_key, private_gamal ,public_gamal, myusername):
    
    print("SESSION KEY (reciever):", session_key.hex())
    input("press enter when you recieve the public key from the other device")
    
    #session_key_str = session_key.hex()
    #plain_vault = loadVault(session_key.hex(), vault_name, public_gamal)
    
    if not os.path.exists(vault_name):
        raise Exception("Vault does not exist")

    

    with open(vault_name, "r") as file_object:
        vault = json.load(file_object)

    packed_hex = vault["encrypted_vault"]

    if not verify(packed_hex, vault["signature"], public_gamal):  # verify signature
        raise Exception("Vault tampered!")

    packed = bytes.fromhex(vault["encrypted_vault"])

    try:
        plaintext = decrypt(session_key, packed)
    except Exception:
        raise Exception("Invalid password or corrupted vault")

    plain_vault = json.loads(plaintext.decode())
    cipher_vault = saveVault(master_password, get_vault_from_username(myusername), plain_vault, private_gamal)
    """
    input("Press enter when you have received the exported vault from the other device: ")
    #exported_vault = recieve(myusername, hisusername)
    with open(vault_name, "w") as f:
        json.dump(vault_name, f)
    # same fix — convert to hex string
    session_key_str = session_key.hex()
    plain_vault = loadVault(session_key_str, vault_name, public_gamal)
    saveVault(master_password, vault_name, plain_vault, private_gamal)
    """
    
    
    
#***********************************************************************************
#Main function
#***********************************************************************************

def get_vault_from_username(username):
    return f"Password-Manager/keys/{username}_vault.json"

def main_transfer(myusername, master_password, hisusername):
    
    #read elgamal xa,ya, yb
    xa = load_private_key(myusername, master_password)
    ya = load_public_key(myusername)
    yb = load_public_key(hisusername)

    vault = get_vault_from_username(myusername)
    
    session_key = key_exchange_phase(xa, yb, ya["alpha"], ya["p"], myusername, hisusername)
    signed_vault = transfer_phase(vault, master_password, session_key, xa, ya)
    
    
def main_import(myusername, master_password, hisusername):
    
    xa = load_private_key(myusername, master_password)
    ya = load_public_key(myusername)
    yb = load_public_key(hisusername)
    
    
    vault = get_vault_from_username(hisusername)
    
    session_key = key_exchange_phase(xa, yb,ya["alpha"], ya["p"], myusername, hisusername)
    import_phase(vault, master_password, session_key, xa, yb, myusername)
    
    
    
    