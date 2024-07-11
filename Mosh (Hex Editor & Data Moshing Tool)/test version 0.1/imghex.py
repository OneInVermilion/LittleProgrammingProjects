import random

f = open("birb.png", "r+b") #open file for reading in binary mode, so that it works correctly
h = f.read()
f.close()

#print(type(h), "\n", h) #for debugging

bulk = h.hex() #string



#edit bulk here----------------------
#SEE THE PATTERN WITH IMAGE SIZE AND WHERE EDIT_START IS SAFE
hex_alphabet = "0123456789abcdef"
edit_start = 400
edit_length = 100
#print(bulk)
edit = ""
for i in range(edit_length):
    edit += hex_alphabet[random.randint(0, 15)]
bulk_new = bulk[:edit_start] + edit + bulk[edit_start + edit_length:]
#edit bulk here----------------------



h_bytes = bytes(bytearray.fromhex(bulk_new)) #first from string/hex to bytearray, then from bytearray to bytes
#print(type(h_bytes), "\n", h_bytes) #for debugging


f_new = open("data_moshed.png", "w+b") #create a new file
f_new.write(h_bytes) #fill with edited contents
f_new.close()


