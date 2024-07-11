import random

imgname = input("Image name, without .png: ")
#custom_chance = float(input("Corruption degree (recommended around 1): "))
custom_chance = 0.01
print("Please make sure that the image is small (~100 KB) for small runtime\n")

f = open(imgname + ".png", "r+b") #open file for reading in binary mode, so that it works correctly
h = f.read()
f.close()
#birb S400 L100

#print(type(h), "\n", h) #for debugging

bulk = h.hex() #string



#edit bulk here----------------------
#SEE THE PATTERN WITH IMAGE SIZE AND WHERE EDIT_START IS SAFE
hex_alphabet = "0123456789abcdef"
edit_start = 20
until_the_end = len(bulk) - edit_start
#print(until_the_end)
edit_length = until_the_end
edit_chance = float(custom_chance)
#print(bulk)
edit = ""
percentage_written = []
for i in range(edit_length):
    rand = random.random() * 100
    if rand <= edit_chance:
        edit += hex_alphabet[random.randint(0, 15)]
    else:
        edit += bulk[edit_start + i]
bulk_new = bulk[:edit_start] + edit + bulk[edit_start + edit_length:]
#edit bulk here----------------------



h_bytes = bytes(bytearray.fromhex(bulk_new)) #first from string/hex to bytearray, then from bytearray to bytes
#print(type(h_bytes), "\n", h_bytes) #for debugging


f_new = open(imgname + "_moshed.png", "w+b") #create a new file
f_new.write(h_bytes) #fill with edited contents
f_new.close()
print("New file saved as: " + imgname + "_moshed.png")
input("Press ENTER to exit")


