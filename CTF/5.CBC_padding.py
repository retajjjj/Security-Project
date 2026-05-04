import requests

url = "http://cbc-ctf.westeurope.azurecontainer.io:5000/oracle"

ciphertext = "b248f0e8f4e3548b995d2215f54b72bd5d3b211b522b7a5ea25c5763e7425447e440e4d85933807e1385d11cd1959975"

# Split into blocks 
IV = bytearray.fromhex(ciphertext[0:32])
C1 = bytearray.fromhex(ciphertext[32:64])
C2 = bytearray.fromhex(ciphertext[64:96])

def oracle(iv, block):
    payload = iv.hex() + block.hex()
    response = requests.post(url, json={"ciphertext_hex": payload})
    return response.json()["valid_padding"]

def decrypt_block(iv, block):
   
    INT = bytearray(16)   
    plaintext = bytearray(16)   
    
    for byte_pos in range(15, -1, -1):
        padding_val = 16 - byte_pos  
        
        fake_iv = bytearray(16)
        
        for k in range(byte_pos + 1, 16):
            fake_iv[k] = INT[k] ^ padding_val
        
        for guess in range(256):
            fake_iv[byte_pos] = guess
            
            if oracle(fake_iv, block):
                INT[byte_pos] = guess ^ padding_val
                plaintext[byte_pos] = INT[byte_pos] ^ iv[byte_pos]
                print(f"  Byte {byte_pos}: {chr(plaintext[byte_pos])} ({hex(plaintext[byte_pos])})")
                break
    
    return plaintext

print("Decrypting C1...")
p1 = decrypt_block(IV, C1)

print("Decrypting C2...")
p2 = decrypt_block(C1, C2)

flag = (p1 + p2).decode(errors='replace')
print(f"\nFlag: {flag}")