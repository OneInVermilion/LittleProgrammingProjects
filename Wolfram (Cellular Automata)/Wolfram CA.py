import pygame
from time import sleep

#rule = 30
rule = int(input("Rule: "))

sqr_size = 1

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 750

#--------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("WolframCA")

steps = WINDOW_HEIGHT // sqr_size
grid_size = WINDOW_WIDTH // sqr_size
if (rule > 255 or rule < 1):
    sys.exit(0)

def next_cell(left: str, mid: str, right: str, rule: int):
    rule = "{0:08b}".format(rule)
    state = 7 - int(left + mid + right, 2)
    return rule[state]

def next_gen(grid: str, rule: int):
    grid_next = ""
    for i in range(len(grid) - 1):
        grid_next += next_cell(grid[i-1], grid[i], grid[i+1], rule)
    grid_next += next_cell(grid[-2], grid[-1], grid[0], rule)
    return grid_next
    
def format_grid(grid: str, zero: str, one: str):
    zero = " "
    one = "@"
    grid = grid.replace("0", zero)
    grid = grid.replace("1", one)
    return grid

def grid_to_pygame(grid: str, y: int):
    for i in range(len(grid)):
        if (grid[i] == "1"):
            pygame.draw.rect(screen, (255, 255, 255), (i*sqr_size + (WINDOW_WIDTH - grid_size*sqr_size)/2, y, sqr_size, sqr_size))

#--------------------------------------------------

grid = "0"*grid_size
grid = grid[:len(grid)//2] + "1" + grid[len(grid)//2+1:]

for i in range(steps):
    grid_to_pygame(grid, i*sqr_size)
    grid = next_gen(grid, rule)
pygame.display.flip()

a = input()
#sleep(1)
#pygame.quit()

"""
print("\n"*32)
for k in range(1, 256):
    screen.fill((0, 0, 0))
    grid = "0"*grid_size
    grid = grid[:len(grid)//2] + "1" + grid[len(grid)//2+1:]
    for i in range(steps):
        grid_to_pygame(grid, i*sqr_size)
        grid = next_gen(grid, k)
    pygame.display.flip()
    print(k)
    sleep(1)
"""
