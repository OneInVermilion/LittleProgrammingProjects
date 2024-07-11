from random import randint
from os import system

print("Please wait, the words are loading...")
file = open("words.txt", "r", encoding='utf-8')
words_raw = file.readlines()
file.close()
words = []

for i in range(len(words_raw)):
    this_word = words_raw[i].split('\t') #splitting based on tab sign
    while '' in this_word: #removing extra symbols if many tab signs are there
        this_word.remove('')
    this_word[1] = this_word[1].replace('\n', '')
    if this_word not in words: #removing duplicates
        words.append(this_word)

mode = int(input("1 for Deu -> Eng\n2 for Eng -> Deu\n"))
mode -= 1 #mode 0 will choose element 0 of array, which will be german word and vice versa
print()

while True:
    system("cls") #turn off if running in idle
    rnd = randint(0, len(words) - 1)
    print(words[rnd][mode])
    input()
    print(words[rnd][int(not bool(mode))])
    input()
