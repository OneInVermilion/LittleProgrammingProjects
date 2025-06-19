def gcd(a: int, b: int):
    if a == 0: return b
    return (gcd(b % a, a))

def keygen(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2
    while True:
        if gcd(e, phi) == 1: break
        e += 1
    d = pow(e, -1, phi)
    return ((n, e), (n, d))

def encrypt(message: int, pubkey: tuple):
    return pow(message, pubkey[1], pubkey[0])

def decrypt(cipher: int, privkey: tuple):
    return pow(cipher, privkey[1], privkey[0])

def str_to_dec(message: str):
    str_hex = "0x"
    for i in message:
        str_hex += str(hex(ord(i))[2:])
    str_dec = int(str_hex, 16)
    return str_dec

def dec_to_str(number: int):
    num_hex = hex(number)[2:]
    message = ""
    for i in range(0, len(num_hex), 2):
        message += chr(int("0x" + num_hex[i:i+2], 16))
    return message

plain_text = "43f"
plain_number = str_to_dec(plain_text)
public_key, private_key = keygen(999979, 999983)
cipher_number = encrypt(plain_number, public_key)
decrypted_number = decrypt(cipher_number, private_key)
decrypted_text = dec_to_str(decrypted_number)
print("Original Message:\t", plain_text)
print("Converted To Number:\t", plain_number)
print("Message Upper Limit:\t", public_key[0] - 1)
print("Ciphertext:\t\t", cipher_number)
print("Decrypted Number:\t", decrypted_number)
print("Decrypted Message:\t", decrypted_text)
