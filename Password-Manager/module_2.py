from hashlib import sha256
from Crypto.Cipher import AES
import json
import os

plaintext = b"Hello World"
password = "password123"


def hashPassword(password):
    # encode string into bytes before hashing, return 32 byte key to use in AES
    return sha256(password.encode()).digest()


def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_GCM)  # create cipher object
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext  # tag provides authentication


def decrypt(key, packed):
    nonce = packed[:16]
    tag = packed[16:32]
    ciphertext = packed[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


def saveVault(password, fileName, data, privateKey):
    key = hashPassword(password)
    plaintext = json.dumps(data).encode()

    try:
        packed = encrypt(key, plaintext)
    except Exception:
        raise Exception("Encryption failed") 
    signature = sign(packed.hex(), privateKey)  # add signature

    vault = {"encrypted_vault": packed.hex(), "signature": signature}
    with open(fileName, "w") as file_object:
        json.dump(vault, file_object)


def createVault(password, fileName, privateKey):
    if os.path.exists(fileName):
        raise Exception("Vault already exists")
    data = {"credentials": []}
    saveVault(password, fileName, data, privateKey)


def loadVault(password, fileName, publicKey):
    if not os.path.exists(fileName):
        raise Exception("Vault does not exist")

    key = hashPassword(password)

    with open(fileName, "r") as file_object:
        vault = json.load(file_object)

    packed_hex = vault["encrypted_vault"]

    if not verify(packed_hex, vault["signature"], publicKey):  # verify signature
        raise Exception("Vault tampered!")

    packed = bytes.fromhex(vault["encrypted_vault"])

    try:
        plaintext = decrypt(key, packed)
    except Exception:
        raise Exception("Invalid password or corrupted vault")

    return json.loads(plaintext.decode())


def checkIndex(index, data):
    if index < 0 or index >= len(data["credentials"]):
        raise Exception("Invalid index")


def checkCredentials(credentials):
    required = {"website", "username", "password"}
    if not isinstance(credentials, dict) or not required.issubset(credentials):
        raise Exception("Invalid credential format")


def add(password, fileName, credentials, privateKey, publicKey):
    checkCredentials(credentials)
    data = loadVault(password, fileName, publicKey)
    data["credentials"].append(credentials)
    saveVault(password, fileName, data, privateKey)


def retrieve(password, fileName, index, publicKey):
    data = loadVault(password, fileName, publicKey)
    checkIndex(index, data)
    return data["credentials"][index]


def update(password, fileName, credentials, index, privateKey, publicKey):
    checkCredentials(credentials)
    data = loadVault(password, fileName, publicKey)
    checkIndex(index, data)
    data["credentials"][index] = credentials
    saveVault(password, fileName, data, privateKey)


def delete(password, fileName, index, privateKey, publicKey):
    data = loadVault(password, fileName, publicKey)
    checkIndex(index, data)
    data["credentials"].pop(index)
    saveVault(password, fileName, data, privateKey)


def accessVault(action, password, filename, privateKey, publicKey, **kwargs):
    if action == "add":
        return add(password, filename, kwargs["credentials"], privateKey, publicKey)

    elif action == "retrieve":
        return retrieve(password, filename, kwargs["index"], publicKey)

    elif action == "update":
        return update(
            password,
            filename,
            kwargs["credentials"],
            kwargs["index"],
            privateKey,
            publicKey,
        )

    elif action == "delete":
        return delete(
            password,
            filename,
            kwargs["index"],
            privateKey,
            publicKey,
        )
