from PIL import Image

image = Image.open("../CTF_DATA/CTF4/stego.png")
w, h = image.size
px = image.load()


def int2bin(n):
    return "{0:08b}".format(n)


def readLSB():
    binaryLSB = ""
    for y in range(h):
        for x in range(w):
            binaryLSB += int2bin(px[x,y])[7]

    output = ""
    for i in range(int(len(binaryLSB) / 8)):
        output += chr(int(binaryLSB[i * 8:i * 8 + 8], 2))

    return output


op = readLSB()
flag = op.split('\x00')[0]
print(flag)

    



    