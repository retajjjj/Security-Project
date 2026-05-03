from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

plaintext = b"Hello World"
password = "password123"


def hashPassword(password):
    # encode string into bytes before hashing, return 32 byte key to use in AES
    return sha256(password.encode()).digest()


def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_GCM)  # create cipher object
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + ciphertext + tag  # tag provides authentication


def decrypt(key, packed):
    nonce = packed[:16]
    ciphertext = packed[16:32]
    tag = packed[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


def createVault(password, fileName):
    key = hashPassword(password)
    data = {"credentials": []}

    json.dumps(data).encode()

    packed = encrypt(key, data)

    vault = {"encrypted_vault": packed.hex(), "signature": None}

    with open(fileName, "w") as file_object:
        json.dump(vault, file_object)

def loadVault(password, fileName):
    key = hashPassword(password)

    with open(fileName, "r") as file_object:
        vault = json.load(file_object)

    packed = bytes.fromhex(vault["encrypted_vault"])

    plaintext = decrypt(key, packed)
    return json.loads(plaintext.decode()), vault

def saveVault(password, fileName):
    key = hashPassword(password)

    pass

def add(password, credentials):
    pass


def retrieve(password, credentials):
    pass


def update(password, credentials):
    pass


def accessVault():
    pass


key = hashPassword(password)
n, c, t = encrypt(key, plaintext)
print(decrypt(key, n, c, t))
