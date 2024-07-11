from PIL import Image

def sharpenise(palette: str):
    palette_sharp = ""
    for i in range(0, len(palette)//2):
        for j in range(0, len(palette)//2 - i + 1):
            palette_sharp += palette[i]
    for i in range(len(palette)//2, len(palette)):
        for j in range(0, i - len(palette)//2 + 1):
            palette_sharp += palette[i]
    return palette_sharp

try:
    f = open("settings.txt", "r")
    settings = f.readlines()[0:4]
    f.close()
    palette = settings[0][0:-1:1]
    flip = bool(int(settings[1]))
    sharpness = bool(int(settings[2]))
    fin_size = int(settings[3])
except Exception:
    print("\"settings.txt\" not found")
    palette = "Ñ@#W9876543210?!abc;:+=,._ "
    flip = True
    sharpness = True
    fin_size = 150

if (sharpness):
    palette = sharpenise(palette)
openthis = input("Image Name, w\\o .png: ")

img = Image.open(openthis + ".png")
pix = img.load()
width = img.size[0]
height = img.size[1]

scale = 1
while (width // scale > fin_size):
    scale += 1
img = img.resize((width // scale, height // (scale*2)));

width = img.size[0]
height = img.size[1]
pix = img.load()

s = ""
for j in range(height):
    for i in range(width):
        average = (pix[i, j][0] + pix[i, j][1] + pix[i, j][2]) // 3
        if (flip):
            average = 255 - average
        char = average / (255 / (len(palette) - 1))
        char = int(char)
        char_add = palette[char]
        s += char_add
    s += "\n"
print(s)
input()
