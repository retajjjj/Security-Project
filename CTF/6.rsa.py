from sympy import factorint

n = 143991606075158483660871570161405209117
e = 65537
ciphertext = 34130411904650996210426832018051041635

# print(factorint(n))

p, q = 12405339649142310293, 11607228028223627369

phi = (p-1)*(q-1)
d = pow(e, -1, phi)

plaintext = pow(ciphertext, d, n)

print(plaintext)
print(bytes.fromhex(hex(plaintext)[2:]).decode())  # CMPN{f4c70r_m3}
