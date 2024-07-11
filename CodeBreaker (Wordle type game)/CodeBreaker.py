import random

#------------------------------------------------------------ Functions ------------------------------------------------------------

def inGameInput(): #Game's own input which checks for special keywords
    guess = input()
    while (guess == "hint!"): #Randomly writing a "hint" on request
        randhint = random.randint(0, len(hints))
        if (difficulty == 4):
            randhint = 0
        if (randhint == len(hints)):
            print("There are a total of", len(hints) + 1, "hints, including this one. Gotta catch them all!")
        else:
            print("\t" + hints[randhint])
        guess = input() #Can be done multiple times
        
    if (guess == "i give up!"): #Possibility to give up
        return False #Can be done only one time, so no 'while' cycle
    return guess

def stringContainsNumbers(s: str):
    for i in s:
        if (i.lower() not in "abcdefghijklmnopqrstuvwxyz"): #Not only digits, but anything apart from letters
            return True
    return False

def generateRandomString(length: int):
    string = ""
    for i in range(length):
        string += chr(random.randint(97, 122)) #97-122 is the range of small letters in ASCII
    return string

def compareStrings(s1: str, s2: str):
    #The cycle 'while' inside the other one guarantees that the strings are the same size
    filledstr = "_" * len(s1)
    anotherplace = ""
    for i in range(len(s1)):
        if (s1[i] == s2[i]): #If the position is correct, 
            filledstr = filledstr[:i] + s1[i] + filledstr[i+1:] #display the letter instead of corresponding '_'.
        if (s1[i] in s2): #If just the existence of letter was guessed,
            if (not s1[i] in anotherplace): #and if it's not already displayed,
                anotherplace += s1[i] #display.
    return(filledstr, anotherplace)
    
#------------------------------------------------------------ Start of the game ------------------------------------------------------------

hints = [
    "There is no help, only suffering",
    "The generation is random, no letter is more likely to appear than the other ones",
    "Remember to fully read the rules!",
    "Letter 'p' either is contained in the code, or isnt",
    "The hints are always helpful!",
    "Also try wordle!",
    "Also try difficulty 4!",
    "Have you heard of Base64 cipher?",
    "Hello World!",
    "If molecular interactions are deterministic, does it mean that all universes are the same?",
    "Follow the white rabbit",
    "Armpits are ontologically parasitic",
    "2 + 2 = 22",
    "hint",
    "Magic: The Gathering is turing complete",
    "ERROR 404: Hint not found",
    "Everybody asks where's the hint, but nobody asks how's the hint :(",
    "beep boop",
    "*lagging modem sounds*",
    "No h1nt 4 U",
    "Self termination in 3...",
    "These hints are not serious. In case you didn't notice",
    "hgaslhasglhshlsdlsdvsfzskzkzg",
    "V2xkR2VtUkhWbmxKUjFadVdubENOVmxZYTJnPQ==",
    "abcdefghijklmnopqrstuvwxyz",
    "This statement is a lie",
    "This statement is weirder than this statement",
    "Google Roko's Basilisk",
    "testing testing 1, 2, 3",
    "My name is Kira Yoshikage",
    "Google... No, don't google it.",
]

divide = "________________________________\n"
title = ""
title += "_________            .___    __________                        __                 " + "\n"
title += "\\_   ___ \\  ____   __| _/____\\______   \\_______   ____ _____  |  | __ ___________ " + "\n"
title += "/    \\  \\/ /  _ \\ / __ |/ __ \\|    |  _/\\_  __ \\_/ __ \\\\__  \\ |  |/ // __ \\_  __ \\" + "\n"
title += "\\     \\___(  <_> ) /_/ \\  ___/|    |   \\ |  | \\/\\  ___/ / __ \\|    <\\  ___/|  | \\/" + "\n"
title += " \\______  /\\____/\\____ |\\___  >______  / |__|    \\___  >____  /__|_ \\\\___  >__|   " + "\n"
title += "        \\/            \\/    \\/       \\/              \\/     \\/     \\/    \\/       " + "\n"
print(title)
print(divide)

win = True

quickstart = input("Quickstart? y/n ") #Quickstart allows to skip difficulty choice (automatic: Normal) and hardcore choice (automatic: Off)
while ((not quickstart in "yn" or len(quickstart) != 1)): #Making sure the code is fool-proof and nothing causes an error. This structure will repeat later
    quickstart = input("Type 'y' for Yes or 'n' for No: ")

difficulty = 2 #Default value (for quickstart)
hardcore = False #Default value (for quickstart)

if (quickstart == "n"): #Manual choice of difficulties
    difficulty = input("Choose difficulty:\n\t1 - Easy (3 letters, ∞ guesses)\n\t2 - Normal (5 letters, 20 guesses)\n\t3 - Hard (8 letters, 15 guesses)\n\t0 - Custom\n\t")
    while (not difficulty in "01234" or len(difficulty) != 1): #Fool-proof
        difficulty = input("Please enter a valid number: ")
    difficulty = int(difficulty)

match difficulty: #Setting variables based on difficulty
    case 1:
        difficulty = "Easy"
        codeLength = 3
        guessesLeft = -1
    case 2:
        difficulty = "Normal"
        codeLength = 5
        guessesLeft = 20
    case 3:
        difficulty = "Hard"
        codeLength = 8
        guessesLeft = 15
    case 4:
        difficulty = "Impossible"
        codeLength = 13
        guessesLeft = 1
        hardcore = True
    case 0: #Custom difficulty - all variables can be choosen manually
        difficulty = "Custom"
        codeLength = input("Please write the length of the code: ")
        while (not codeLength.isdigit() or codeLength == "0"): #Fool-proof
            codeLength = input("Please enter a valid number: ")
        codeLength = int(codeLength)
        guessesLeft = input("Please write the amount of allowed guesses; -1 for infinity: ")
        while (not guessesLeft.isdigit()): #Fool-proof
                if (guessesLeft == "-1"):
                    guessesLeft = -1
                    break
                guessesLeft = input("Please enter a valid number: ")
        guessesLeft = int(guessesLeft)
        #if (guessesLeft < -1): #Just convenience. Because why not?
            #guessesLeft = -1

if (quickstart == "n" and difficulty != "Impossible"): #Manual choice of hardcore mode
    hardcore = input("Enable Hardcore? You will only be able to see symbols on their correct positions. y/n ")
    while ((not hardcore in "yn" or len(hardcore) != 1)): #Fool-proof
        hardcore = input("Type 'y' for Yes or 'n' for No: ")
    if (hardcore == "y"):
        hardcore = True
    else:
        hardcore = False #This is needed to make sure 'hardcore' variable is boolean type (even though disabled is the default value)

code = generateRandomString(codeLength)

#------------------------------------------------------------ Tutorial ------------------------------------------------------------

if (guessesLeft == -1):
    attemptsWriteInTutorial = "∞" #So that it doesn't print '-1'
else:
    attemptsWriteInTutorial = guessesLeft
print(divide)

print("Difficulty: ", difficulty, ";\nCode length: ", codeLength, ";\nAttempts available: ", attemptsWriteInTutorial, ";\nHardcore: ", hardcore, sep="")
print(divide)

if (quickstart == "n"): #We don't need all of this if we're doing quickstart
    print("Welcome to CodeBreaker!")
    print("Your goal is to guess the code (combination of random letters) by typing in your guesses")
    print("You may start guessing the code by typing it (letters only, lower/upper case doesn't matter)")
    print("To help with your guess you will be receiving feedback")
    print("Feedback information:")
    print("\tIf you guessed a letter, it will appear to the right ONCE ONLY, REGARDLESS if you guessed its correct position (disabled in Hardcore)")
    print("\tIf you guessed a letter and its position correctly, it will appear on its position instead of underscores")
    print("\tCode example: ccab")
    print("\tYour attempt example: abcd")
    print("\tFeedback example: ____  |  abc")
    print("You may type in \"hint!\" to recieve a totally helpful hint!")
    print("You may type in \"i give up!\" to give up!")
    print("Good luck!")
    print(divide)

#print(code) #CHEATS

#------------------------------------------------------------ Game process ------------------------------------------------------------

counter = 0 #Counter of attempts made. Different from attempts left
guess = "-" #Default value just so that the first comparison of 'while' cycle is ok

while (guess != code):
    if (guessesLeft == 0): #If we're out of guesses. Written here so that all other information is printed before game understands you've lost
        win = False
        break
    
    counter += 1
    guess = inGameInput()
    if (guess == False): #If giving up
        counter -= 1
        win = False
        break
    
    while (len(guess) != len(code) or stringContainsNumbers(guess)): #If it's not a hint or a give up, make sure that the format is valid
        print("Invalid: please enter a string of the length", codeLength, "and make sure it's letters only") #Fool-proof
        guess = inGameInput()
        if (guess == False): #If giving up
            counter -= 1
            win = False
            break

    if (guess == False): #If giving up; the 'break' above broke out of its own while, but not the main one. So we're breaking here
            break
    
    guess = guess.lower() #So that lower/upper case doesn't matter
    filled, anothers = compareStrings(guess, code)
    output = filled
    if (not hardcore): #Because in hardcore you can't see this information
        output += "  |  " + anothers
    print(output)
    guessesLeft -= 1
    if (guessesLeft >= 0): #Because if you have infinity (negative) guesses, you don't need them printed
        print("Guesses left:", guessesLeft)
    print()

#------------------------------------------------------------ End of the game; Results ------------------------------------------------------------

if (win):
    print("You won!", end="")
    match difficulty:
        case "Easy":
            print(".. but that was easy-breezy!")
        case "Normal":
            print(" Solid attempt!")
        case "Hard":
            print(" Well that was tough!")
        case "Impossible":
            print(" I mean, no you didn't, you cheated.")
        case "Custom":
            print(" Also try other difficulties!")
if (not win):
    print("You lost!", end="")
    match difficulty:
        case "Easy":
            print(".. Never give up! Never let me down!")
        case "Normal":
            print(" Better luck next time!")
        case "Hard":
            print(" You were doing so well! Probably...")
        case "Impossible":
            print(" You are not to blame. I am.")
        case "Custom":
            print(" Was it too difficult or too boring?")
    print("The answer was:", code)
print("Attempts made:", counter)
input("Restart the program to play again!")
