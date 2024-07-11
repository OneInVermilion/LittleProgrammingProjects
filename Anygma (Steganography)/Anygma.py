from PIL import Image
from math import ceil
from os.path import exists
from random import randint

pxn = 7 #Hide info in every nth pixel
formuht = "png" #Format 
img_name_addon = "_encr" #What is added to encrypted new file's name
img_exists_addon = "1" #What is added to encrypted new file's name ON TOP of img_name_addon if such name already exists
img_rewrite = False #If we use img_exists_addon or instead rewrite file with img_name_addon

def ascii_printable(): #Range of "printable" ASCII characters, excluding SPACE and DELETE
    str = ""
    for i in range(33, 127):
        str += chr(i)
    return str

def generate_random_string(length: int): #Generates a string of a certain length
    alphabet = ascii_printable()
    string = ""
    for i in range(length):
        string += alphabet[randint(0, len(alphabet)-1)]
    return string

def bitw_xor(b1: str, b2: str): #Bitwise XOR
    res = ""
    for i in range(len(b1)):
        if (b1[i] == b2[i]):
            res += "0"
        else:
            res += "1"
    return res

def bin_array_to_string(arr):
    bs = "" #BS stands for binary string
    for i in range(len(arr)):
        bs += str(arr[i])
    return bs

def encrypt(msg: str, key: str): #Turns a message into encrypted message by using XOR cipher
    enc = "" #Encoded string
    enc_d = [-1]*len(msg) #Each character from encoded string as a decimal number
    enc_b = [-1]*len(msg)   #Each character from encoded string as a binary number
    enc_bs = "" #Each character from encoded string as a binary number, in a string/tape
    for i in range (len(msg)):
        char_msg = int(ord(msg[i]))
        bchar_msg = "{0:08b}".format(char_msg) #Convert to binary number; if it has <8 digits, add 0s to start until it's 8
        try:
            char_key = int(ord(key[i])) #This crashed the program if you attempted to decrypt with a smaller than needed key
        except Exception:
            char_key = int(ord(key[-1])) #If that happens, just read the last key's symbol
        bchar_key = "{0:08b}".format(char_key)
        bchar_enc = bitw_xor(bchar_msg, bchar_key)
        char_enc = int(bchar_enc, 2)
        enc += chr(char_enc)
        enc_d[i] = char_enc
        enc_b[i] = "{0:08b}".format(char_enc)
    enc_bs = bin_array_to_string(enc_b)
    return (enc, enc_d, enc_b, enc_bs) #Returns all that has gotten here

def decrypt(cip: str, key: str): #Decrypts cipher, using it and the key
    enc_b = [-1]*(len(cip)//8)
    for i in range(0, len(cip), 8):
        try:
            enc_b[i // 8] = cip[i:i+8] #Writing down all 8 digit bin numbers from the cipher/tape into an array
        except Exception:
            print("Unexpected Error. Perhaps, Nothing was Hidden")
            break
    enc = ""
    for i in range(len(enc_b)):
        enc += chr(int(enc_b[i], 2)) #Convert them to decimal numbers and then to characters and then to string
    enc = encrypt(enc, key)[0] #We got the string == encoded string. Get it thourgh the encryption algorythm again with original key to get the original message
    return enc

def encrypt_img(IMAGE_NAME: str, FORMAT: str, tape: str, pxn=1):
    img = Image.open(IMAGE_NAME + "." + FORMAT)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    pixels_are = width * height #Total amount of pixels
    pixels_needed = ceil(len(tape) / 3 * pxn) #Pixels needed to hide the encoded message
    if (pixels_needed > pixels_are):
        return False #The pircure is too small
    tape_counter = 0
    for i in range(0, pixels_are, pxn):
        pxX = i % width #X coordinate of a pixel we're currently working with
        pxY = i // width #Y coordinate
        R = "{0:08b}".format(pix[pxX, pxY][0]) #Red value of a given pixel
        G = "{0:08b}".format(pix[pxX, pxY][1]) #Green value
        B = "{0:08b}".format(pix[pxX, pxY][2]) #Blue value
        if (tape_counter+1 <= len(tape)):
            R = R[0:7] + tape[tape_counter] #Rewriting least significant bit of R' binary representation
        else:
            break
        if (tape_counter+2 <= len(tape)):
            G = G[0:7] + tape[tape_counter + 1] #Rewriting LSB of G
        else:
            break
        if (tape_counter+3 <= len(tape)):
            B = B[0:7] + tape[tape_counter + 2] #Rewriting LSB of B
        else:
            break
        tape_counter += 3
        R = int(R, 2)
        G = int(G, 2)
        B = int(B, 2)
        pix[pxX, pxY] = (R, G, B, pix[pxX, pxY][3]) #Updating the pixel. Don't touch Alpha value
    return(img)

def decrypt_img(IMAGE_NAME: str, FORMAT: str, cipher_length: int, pxn=1):
    cipher_length *= 8
    img = Image.open(IMAGE_NAME + "." + FORMAT)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    pixels_are = width * height
    tape = ""
    tape_counter = 0
    for i in range(0, pixels_are, pxn):
        pxX = i % width
        pxY = i // width
        R = "{0:08b}".format(pix[pxX, pxY][0])
        G = "{0:08b}".format(pix[pxX, pxY][1])
        B = "{0:08b}".format(pix[pxX, pxY][2])
        tape += R[7]
        tape += G[7]
        tape += B[7]
        tape_counter += 3
        if (len(tape) > cipher_length):
            break
    tape = tape[:cipher_length]
    return(tape)

def program_run():
    phrases = [
        "Please, Enter a Valid Response",                                   #0
        "1 for Encrypt, 2 for Decrypt: ",                                   #1
        "Enter Image Name, without .png: ",                                 #2
        "Enter Message (Max Length = 510): ",                               #3
        "Message Length:",                                                  #4
        "1 for Custom Key, 2 for Random Key: ",                             #5
        "Enter Key of Equal Length: ",                                      #6
        "Your Final and Only Valid Key:",                                   #7
        "The Picture is too Small for Your Message",                        #8
        "Encryption Complete!",                                             #9
        "File Saved As: ",                                                  #10
        "Enter Key: ",                                                      #11
        "Inputted Key Length:",                                             #12
        "Decryption Complete!",                                             #13
        "Message:",                                                         #14
        "\nPress ENTER to Exit",                                            #15
        "-"                                                                 #-1
    ]
    print("Welcome to \"Anygma\" Text 2 Image Steganography Tool!")
    print("The Program Works with PNG Files Only and ASCII Symbols Only")
    print("You Must Have The Image in The Same Folder as this Program in order for It to Work")
    print()
    mode = input(phrases[1])
    while (not(mode in "12" and len(mode) == 1)):
        print(phrases[0])
        mode = input(phrases[1])
    if (mode == "1"): #Encrypt
        image = input(phrases[2])
        while (not exists(image + "." + formuht)):
            print(phrases[0])
            image = input(phrases[2])
        message = input(phrases[3])
        while (len(message) > 510):
            print(phrases[0])
            message = input(phrases[3])
        message += "_"
        print(phrases[4], len(message)-1)
        key_mode = input(phrases[5])
        while (not(key_mode in "12" and len(key_mode) == 1)):
            print(phrases[0])
            key_mode = input(phrases[5])
        if (key_mode == "1"):
            key = input(phrases[6])
            while (len(key) != len(message)-1):
                print(phrases[0])
                key = input(phrases[6])
        else:
            key = generate_random_string(len(message)-1)
        key = key.replace(" ", "_")
        key += "_"
        if (key_mode in "23"):
            print(phrases[7])
            print(phrases[-1]*len(key))
            print(key[0:len(key)-1])
            print(phrases[-1]*len(key))
        cipher = encrypt(message, key)
        img = encrypt_img(image, formuht, cipher[3], pxn)
        if (not img):
            print(phrases[8])
        else:
            image_new = image + img_name_addon
            while (exists(image_new + "." + formuht)):
                if (img_rewrite):
                    break
                image_new += img_exists_addon
            img.save(image_new + "." + formuht)
            print(phrases[9])
            print(phrases[10], image_new + "." + formuht, sep="")
    else: #Decrypt
        image = input(phrases[2])
        while (not exists(image + "." + formuht)):
            print(phrases[0])
            image = input(phrases[2])
        key = input(phrases[11])
        print(phrases[12], len(key))
        key += "_"
        cipher = decrypt_img(image, formuht, len(key), pxn)
        message = decrypt(cipher, key)
        message = message[0:len(message) - 1]
        print(phrases[13])
        print(phrases[14], message)
    input(phrases[15])

#-----------------------------------------------------------
    
program_run()
