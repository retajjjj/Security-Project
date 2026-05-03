from module_2 import hashPassword, encrypt, decrypt, saveVault, createVault, loadVault, checkIndex, checkCredentials, add, retrieve,update,delete, accessVault
import json
password = "password123"
text = "abc"

gamal_ya = 78
gamal_xa = 12
gamal_yb = 123

private_gamal = {"alpha": 8, "x":gamal_xa, "p":101}
public_gamal = {"alpha": 8, "y":gamal_ya, "p":101}
    
#.encode() is to convert form string to bytes
updated = {"website": "123", "username": "retag", "password": "123"}
cred = {"website": "hi", "username": "retag", "password": "123"}
json.dumps(updated, sort_keys=True).encode()



#input string, output: password in bytes
pass_hashed = hashPassword(password) 

#input plain text in bytes and hashed password, outputs cipher, counce,tag as one large bytes
encrypted_object = encrypt(pass_hashed, text.encode()) 
encrypted_object.hex() #to convert from bytes to hex
    
#input encrypted text in byes and hashed password, output string 
plain_text = decrypt(pass_hashed, encrypted_object)

#input password as string, filename, private key for sig
#output vault file encrypted vault and signature
#combine signautre and encryption

createVault(password, "vault_create_text.json", private_gamal)


#combine verification and decrpytion
#output vault in text format
loadVault(password, "vault_create_text.json", public_gamal)



#input data as plain text and makes sure website, password and username are present
checkCredentials(updated)

#same inputs but extra data as dict (website, username, pass)
add(password, "vault_create_text.json", cred, private_gamal, public_gamal)

#combine encryption and signing of data
saveVault(password, "vault_create_text.json", updated,private_gamal )

#flow: create , add , load at any time, dont save then load

#retreive a dict by index
retrieve(password, "vault_create_text.json", 0, public_gamal)

update(password, "vault_create_text.json",updated,0, private_gamal, public_gamal )

delete(password, "vault_create_text.json", 0,private_gamal, public_gamal )


#function to use accessvault, load, create