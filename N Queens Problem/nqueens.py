import random
import math
from datetime import datetime
import matplotlib.pyplot as plt

class Board:
    def __init__(self, arg):
        if isinstance(arg, int):
            self.n: int = arg
            self.values: list = [0]*arg
        elif isinstance(arg, list):
            self.n = len(arg)
            self.values = arg
        else:
            raise TypeError("Board expects int or list")
    def __str__(self):
        return str(self.values)
    def copy(self):
        copied = Board(self.values.copy())
        return copied
    def nextboard(self):
        for i in range(self.n):
            self.values[i] += 1 # array acting like base-n counting system
            if self.values[i] < self.n: break # one digit is one array index, and it can not exceed base number by definition
            self.values[i] = 0 #if it does, it gets set back to 0 and the next index will be increased instead (next for loop iteration)
    def is_solved(self):
        vertical_check = set() # check if queen attacks another vertically
        diagonal_check1 = set() # check if queen attacks another diagonally down-right
        diagonal_check2 = set() # check if queen attacks another diagonally down-left
        # no queen attacks another queen horizontally by definition of this data structure
        # since each row is each element in the array
        # therefore two queens on the same row would mean two elements in the same index, which is physically impossible
        for i in range(self.n):
            val = self.values[i]
            dif1 = val - i
            dif2 = val + i - self.n
            if val in vertical_check or dif1 in diagonal_check1 or dif2 in diagonal_check2:
                return False
            vertical_check.add(val)
            diagonal_check1.add(dif1)
            diagonal_check2.add(dif2)
        return True
    def get_fittness(self):
        factor = 0 # how many queens are attacking each other
        for i in range(self.n):
            val = self.values[i]
            for j in range(self.n): # for each value checking all other pieces
                if i != j: # so that we don't count each queen attacking itself
                    val2 = self.values[j]
                    if val == val2 or val - i == val2 - j or val + i - self.n == val2 + j - self.n: factor += 1
        return factor
    def get_most_fit(boards: list["Board"]):
        fittest = boards[0]
        for i in boards:
            if i.get_fittness() < fittest.get_fittness():
                fittest = i
        return fittest
    def is_fittness_sorted(boards: list["Board"]): # is a list of boards is sorted by fittness (ascending in fittness value <==> closest solution to furthest)
        for i in range(len(boards) - 1):
            if boards[i].get_fittness() > boards[i+1].get_fittness(): return False
        return True
    def sort_fittness(boards: list["Board"]):
        while Board.is_fittness_sorted(boards) == False:
            for i in range(len(boards) - 1):
                if boards[i].get_fittness() > boards[i+1].get_fittness():
                    boards[i], boards[i+1] = boards[i+1].copy(), boards[i].copy()
        return boards
    def print_boards(boards: list["Board"]):
        for b in boards:
            print(b, b.get_fittness())
    def randomize(self):
        random.shuffle(self.values)
    def plot(queens: list["int"]):
        n = len(queens)
        _, ax = plt.subplots()
        for i in range(n):
            for j in range(n):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                ax.add_patch(plt.Rectangle((i, j), 1, 1, color=color))
        for row in range(len(queens)):
            col = queens[row]
            ax.text(float(col) + 0.5, float(row) + 0.5, '♛', ha='center', va='center', fontsize=28, color='black')
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        plt.gca().invert_yaxis()
        plt.show()
    def solve_bruteforce(self, break_on_solution_found: bool = True):
        current_board = self.copy()
        solutions: list = []
        for i in range(current_board.n ** current_board.n):
            if current_board.is_solved():
                solutions.append(current_board.values.copy())
                if break_on_solution_found: return Board(solutions[0])
            current_board.nextboard()
        return solutions
    def solve_greedy(self, find_fittness_zero: bool = False):
        #fittnesses_plot = []
        current_board = self.copy()
        while True: # until finds a solution
            possible_steps = [] # put here possible steps to choose the fittest
            for i in range(current_board.n):
                temp = current_board.values.copy()
                temp[i] = temp[i] - 1 if temp[i] != 0 else current_board.n - 1 # move queen 1 step to the left or wrap around the board
                possible_steps.append(Board(temp))
                temp = current_board.values.copy()
                temp[i] = temp[i] + 1 if temp[i] != current_board.n - 1 else 0 # 1 step to the right or wrap
                possible_steps.append(Board(temp))
            best_neighbor = Board.get_most_fit(possible_steps)
            #fittnesses_plot.append(best_neighbor.get_fittness())
            if current_board.get_fittness() <= best_neighbor.get_fittness() and (current_board.get_fittness() == 0 or not find_fittness_zero):
                #if we're stuck in a maxima AND (this solution is full OR we're satisfied with local maxima)
                #plt.plot(fittnesses_plot)
                #plt.title("N = " + str(current_board.n) + ", Solution = " + str(current_board) + " (Fittness " + str(current_board.get_fittness()) + ")")
                #plt.show()
                return current_board
            elif current_board.get_fittness() <= best_neighbor.get_fittness():
                #if we're stuck in a maxima {implied: AND the 'or' statement above was false == we're not at fittness 0 but we're looking for it}
                rand_board = Board(list(range(current_board.n)))
                rand_board.randomize()
                current_board = rand_board #randomize to possibly fall into another maxima, which can be with fittness 0
            current_board = best_neighbor.copy()
    def solve_annealing(self, acceptable_fittness: int = 0, temperature_start: float = 100, temperature_decrease: float = 0.1):
        #fittnesses_plot = []
        current_board = self.copy()
        t = temperature_start
        while (t > 0):
            random_queen_index = random.randrange(current_board.n)
            random_queen_new_position = random.randrange(current_board.n)
            new_board = current_board.copy()
            new_board.values[random_queen_index] = random_queen_new_position
            delta = new_board.get_fittness() - current_board.get_fittness()
            chance = 1 if delta < 0 else math.exp(-delta / t)
            if random.random() <= chance: current_board = new_board.copy()
            t -= temperature_decrease
            #fittnesses_plot.append(current_board.get_fittness())
            if current_board.get_fittness() <= acceptable_fittness:
                #plt.plot(fittnesses_plot)
                #plt.title("N = " + str(current_board.n) + ", Solution = " + str(current_board) + " (Fittness " + str(current_board.get_fittness()) + ")")
                #plt.show()
                return current_board
        #plt.plot(fittnesses_plot)
        #plt.title("N = " + str(current_board.n) + ", Solution = " + str(current_board) + " (Fittness " + str(current_board.get_fittness()) + ")")
        #plt.show()
        return current_board
    def solve_genetic(self, population_size: int = 150, crossover_pairs: int = 50, mutation_chance: float = 0.1, iterations_limit: int = 30):
        #fittnesses_plot = []
        current_board = self.copy()
        population = list()
        fittest_selection = list() # the selection of the fittest boards for crossovers and mutations
        for i in range(population_size):
            b = Board(list(range(current_board.n)))
            b.randomize() # creating pool of random boards
            population.append(b) # and adding to population
        for it in range(iterations_limit): # doing until stopping condition (solution found or too many iterations) is met
            Board.sort_fittness(population) # sort by fittness, so that the closest to solution boards are at the start
            #fittnesses_plot.append(population[0].get_fittness())
            #print(population[0].get_fittness())
            if population[0].get_fittness() == 0: # return solved board if found
                #plt.plot(fittnesses_plot)
                #title = "N = " + str(population[0].n) + ", Stats = "
                #title += str(population_size) + " " + str(crossover_pairs) + " " + str(mutation_chance) + " " + str(iterations_limit)
                #title += " (Fittness " + str(population[0].get_fittness()) + ")"
                #plt.title(title)
                #plt.show()
                return population[0]
            if crossover_pairs > population_size // 2: crossover_pairs = population_size // 2 # prevention of out of bounds error for "population" list
            for i in range(crossover_pairs * 2):
                fittest_selection.append(population.pop(0)) # putting the fittest boards into a special crossing over pool
            for i in range(crossover_pairs): # crossing over
                c1: list = fittest_selection[i*2].copy().values
                c2: list = fittest_selection[i*2+1].copy().values
                k = random.randint(1, current_board.n - 1) # place where the crossover will happen
                c1_new = c1[:k] + c2[k:]
                c2_new = c2[:k] + c1[k:]
                fittest_selection[i*2] = Board(c1_new)
                fittest_selection[i*2+1] = Board(c2_new)
            for i in range(crossover_pairs * 2): # mutations
                for index in range(len(fittest_selection[i].values)): # for each board's value
                    if random.random() <= mutation_chance:
                        fittest_selection[i].values[index] = random.randint(0, current_board.n - 1)
            while(len(fittest_selection) > 0):
                population.append(fittest_selection.pop())
        Board.sort_fittness(population)
        #plt.plot(fittnesses_plot)
        #title = "N = " + str(population[0].n) + ", Stats = "
        #title += str(population_size) + " " + str(crossover_pairs) + " " + str(mutation_chance) + " " + str(iterations_limit)
        #title += " (Fittness " + str(population[0].get_fittness()) + ")"
        #plt.title(title)
        #plt.show()
        return population[0] # return closest to solved board if iterations are exhausted


# ----------------------------------------
#todo
#implement matplotlib for visualizing changes in fittness for greedy and annealing
#do a plot of fitnesses of all boards in order (nextboard)
n = 8
alg = 1

"""
fittnesses = []
b = Board(n)
for i in range(pow(n, n)):
    fittnesses.append(b.get_fittness())
    b.nextboard()
plt.plot(fittnesses)
plt.title("N = " + str(n))
plt.show()
"""

start = datetime.now()
solution = Board(1)
match alg:
    case 1:
        solution = Board(n).solve_bruteforce()
    case 2:
        solution = Board(n).solve_greedy()
    case 3:
        solution = Board(n).solve_annealing()
    case 4:
        solution = Board(n).solve_genetic()
print(solution, solution.get_fittness())
print(datetime.now() - start)
Board.plot(solution.values)
