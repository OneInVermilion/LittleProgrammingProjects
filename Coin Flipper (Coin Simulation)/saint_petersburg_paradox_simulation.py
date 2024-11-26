import random
ITER = 10**6

def num_length(num: int):
    if num == 0:
        return 1
    res = 0
    while num > 0:
        num //= 10
        res += 1
    return res

def equalize_num_string(num: int, maxi: int): #equalizes the number to the length of the maxi number by adding zeros to the front
    res = str(num)
    for i in range(num_length(maxi) - num_length(num)):
        res = " " + res
    return res

def num_to_line(num: int, limit: int, char: chr):
    vis = ""
    for i in range(min(num, limit)):
        vis += char
    if limit < num:
        vis += "+"
        vis += str(num - limit)
    return vis

def run_simulation():
    flips = 0
    result = random.randint(0, 1)
    while result:
        flips += 1
        result = random.randint(0, 1)
    return flips

results = []
for i in range(ITER):
    results.append(run_simulation())
uniques = []
for i in results:
    if i not in uniques:
        uniques.append(i)
uniques.sort()

won_total = 0
for i in results:
    won_total += 2**i

counters = []

print("RULES:\nA coin is being flipped. You start at winnings = 1$. Double it on each heads result. End game and claim winnings on tails.")
print("--------Simulation Start--------\n")

for i in range(uniques[-1] + 1):
    counter = results.count(i)
    counters.append(counter)
    percentage = counter / len(results) * 100
    percentage_format = "%0.2f" % percentage
    if len(percentage_format) == 4:
        percentage_format = "0" + percentage_format
    temp = counters.copy()
    temp.sort()
    print(equalize_num_string(i, uniques[-1]), " (", equalize_num_string(counters[i], temp[-1]), " | ", percentage_format, " %) ", sep="",  end=": ")
    print(num_to_line(results.count(i), 128, '@'))

print()
print("Simulation Ran Times:\t", len(results))
print("Biggest Win:\t\t", 2**uniques[-1], "$")
print("Total Winnings:\t\t", won_total, "$")
print("Average Win per Game:\t", won_total / len(results))
print("\n--------Simulation End--------")
