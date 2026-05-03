from PIL import Image

img1 = Image.open("../CTF_DATA/CTF2/Layer1.png")
img2 = Image.open("../CTF_DATA/CTF2/Layer2.png")

img1 = img1.convert("RGB")
img2 = img2.convert("RGB")

pixels1 = img1.load()
pixels2 = img2.load()

width, height = img1.size

# Trial 1: XOR
result1 = Image.new("RGB", (width, height))
pixels_r1 = result1.load()
for x in range(width):
    for y in range(height):
        r1, g1, b1 = pixels1[x, y]
        r2, g2, b2 = pixels2[x, y]
        pixels_r1[x, y] = (r1 ^ r2, g1 ^ g2, b1 ^ b2)

result1.save("../CTF_DATA/CTF2/trial1_xor.png")
result1.show()
print("Trial 1 (XOR) saved!")

# Trial 2: AND
result2 = Image.new("RGB", (width, height))
pixels_r2 = result2.load()
for x in range(width):
    for y in range(height):
        r1, g1, b1 = pixels1[x, y]
        r2, g2, b2 = pixels2[x, y]
        pixels_r2[x, y] = (r1 & r2, g1 & g2, b1 & b2)

result2.save("../CTF_DATA/CTF2/trial2_and.png")
result2.show()
print("Trial 2 (AND) saved!")