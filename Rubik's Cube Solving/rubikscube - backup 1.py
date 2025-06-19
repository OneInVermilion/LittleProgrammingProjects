import numpy as np
import random


def print_cube_raw(cube):
    cube = np.copy(cube)
    for side in range(6):
        print(side)
        for i in range(n):
            for j in range(n):
                if (cube[side][i][j] < 10): print("0", end="")
                print(cube[side][i][j], end=" ")
            print()
        print()


def print_cube(cube):
    cube = np.copy(cube)
    print("XY0\t\tXY1\t\tXZ0\t\tXZ1\t\tYZ0\t\tYZ1")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                if (cube[side][j][i] < 10): print("0", end="")
                print(cube[side][j][i], end=" ")
            print("\t", end="")
        print()

def print_cube_letters(cube):
    cube = np.copy(cube)
    print("XY0\tXY1\tXZ0\tXZ1\tYZ0\tYZ1")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                print(chr(65 + cube[side][j][i]), end=" ")
            print("\t", end="")
        print()

def order_cube(cube):
    cube = np.copy(cube)
    counter = 1
    for side in range(6):
        for i in range(n):
            for j in range(n):
                #cube[side][i][j] = counter #each tile is individual number
                cube[side][i][j] = side #each tile is side number
                counter += 1
    return cube

def randomize_cube(cube): #CHANGE LATER TO BE RANDOM TURNS, because this rand does not guarantee solution
    cube = np.copy(cube)
    colors = [0 for _ in range(6*n*n)]
    counter = 0
    for color in range(1, 7):
        for i in range(n*n):
            colors[counter] = color
            counter += 1
    random.shuffle(colors)
    counter = 0
    for side in range(6):
        for i in range(n):
            for j in range(n):
                cube[side][i][j] = colors[counter]
                counter += 1
    return cube

#0-XY0  1-XY1  2-XZ0  3-XZ1  4-YZ0  5-YZ1
#X: XY0 -> XZ0 -> XY1 -> XZ1  0 2 1 3
#Y: XY0 -> YZ0 -> XY1 -> YZ1  0 4 1 5
#Z: XZ0 -> YZ0 -> XZ1 -> YZ1  2 4 3 5
def turn(cube, slice: int, axis: int, rotation: int = 1): #slice 1-n, axis 1-3, rotation 1 or -1
    cube = np.copy(cube)
    slice -= 1
    rot = [0, 0, 0, 0]
    if axis == 1:
        rot = [0, 2, 1, 3]
        temp = np.array(cube[rot[0], :, slice])
        cube[rot[0], :, slice], cube[rot[1], :, slice], cube[rot[2], :, slice], cube[rot[3], :, slice], = cube[rot[(0 + rotation) % 4], :, slice], cube[rot[(1 + rotation) % 4], :, slice], cube[rot[(2 + rotation) % 4], :, slice], cube[rot[(3 + rotation) % 4], :, slice]
        cube[rot[3], :, slice] = temp
    elif axis == 2:
        rot = [0, 4, 1, 5]
        temp = np.array(cube[rot[0], slice, :])
        cube[rot[0], slice, :], cube[rot[1], slice, :], cube[rot[2], slice, :], cube[rot[3], slice, :], = cube[rot[(0 + rotation) % 4], slice, :], cube[rot[(1 + rotation) % 4], slice, :], cube[rot[(2 + rotation) % 4], slice, :], cube[rot[(3 + rotation) % 4], slice, :]
        cube[rot[3], slice, :] = temp
    elif axis == 3:
        rot = [2, 4, 3, 5]
        temp = np.array(cube[rot[0], slice, :])
        cube[rot[0], slice, :], cube[rot[1], :, slice], cube[rot[2], slice, :], cube[rot[3], :, slice], = cube[rot[(0 + rotation) % 4], slice, :], cube[rot[(1 + rotation) % 4], :, slice], cube[rot[(2 + rotation) % 4], slice, :], cube[rot[(3 + rotation) % 4], :, slice]
        cube[rot[3], :, slice] = temp
    return cube

n = 3 #the NxN cube sides
my_cube = np.array([[[0 for _ in range(n)] for _ in range(n)] for _ in range(6)])
my_cube = order_cube(my_cube)
print_cube_letters(my_cube)
my_cube = turn(my_cube, 1, 1)
print_cube_letters(my_cube)
#print_cube(turn(my_cube, 1, 1, 1))
#print_cube(turn(my_cube, 1, 2, 1))
#print_cube(turn(my_cube, 1, 3, 1))

#rotation -1 is broken
#xz0 -> yz1 to be reversed