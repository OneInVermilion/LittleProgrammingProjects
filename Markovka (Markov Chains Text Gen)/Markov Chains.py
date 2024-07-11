from random import randint
from time import time

start_time = time()

def find_in_list(arr, item):
    for i in range(len(arr)):
        if arr[i] == item:
            return i
    return False

try:
    f = open("text.txt", "r")
    base = f.read()
    f.close()
except Exception:
    print("\"text.txt\" not found")
    input()
    quit()

try:
    f = open("settings.txt", "r")
    sett = f.readlines()[0:2]
    f.close()

    fintext_length = int(sett[0])
    chain_length = int(sett[1])
    fintext_length -= chain_length
except Exception:
    print("\"settings.txt\" not found or is incorrectly filled")
    print("settings template:")
    print("final text length")
    print("n-gram length")
    input()
    quit()


grams = [0]*(len(base) - chain_length + 1)
for i in range(len(base) - chain_length + 1):
    gram = ""
    for j in range(i, i + chain_length):
        gram += base[j]
    grams[i] = gram

chain_length += 1
grams1 = [0]*(len(base) - chain_length + 1) #for finding next character after the gram
for i in range(len(base) - chain_length + 1):
    gram = ""
    for j in range(i, i + chain_length):
        gram += base[j]
    grams1[i] = gram
chain_length -= 1


grams_unique = []
for i in range(len(grams)): #adding unique grams
    if (grams[i] not in grams_unique):
        grams_unique.append(grams[i])

grams_unique_count = [0]*len(grams_unique)
for i in range(len(grams_unique)): #counting unique grams
    grams_unique_count[i] = grams.count(grams_unique[i])

follows = []
follows_length = []
for i in range(len(grams_unique)):
    fols = []
    for j in range(len(grams) - 1):
        if (grams[j] == grams_unique[i]):
            fols.append(grams1[j][-1]) #adding the following gram
    follows.append(fols)
    follows_length.append(len(fols))

fintext = grams[randint(0, len(grams)-1)]
for i in range(fintext_length):
    current = fintext[i : i + chain_length]
    k = find_in_list(grams_unique, current)
    try:
        fintext += follows[k][randint(0, follows_length[k] - 1)]
    except Exception:
        break

if (fintext[0] == " "):
    fintext = fintext[1:]
print(fintext)
print(time() - start_time, "seconds")
input()
