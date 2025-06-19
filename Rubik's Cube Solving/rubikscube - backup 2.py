import numpy as np
import random


def print_cube_raw(cube, n):
    cube = np.copy(cube)
    for side in range(6):
        print(side)
        for i in range(n):
            for j in range(n):
                if (cube[side][i][j] < 10): print("0", end="")
                print(cube[side][i][j], end=" ")
            print()
        print()


def print_cube(cube, n):
    cube = np.copy(cube)
    print("XY0\t\tXY1\t\tXZ0\t\tXZ1\t\tYZ0\t\tYZ1")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                if (cube[side][j][i] < 10): print("0", end="")
                print(cube[side][j][i], end=" ")
            print("\t", end="")
        print()

def print_cube_letters(cube, n):
    cube = np.copy(cube)
    print("XY0\t\tXY1\t\tXZ0\t\tXZ1\t\tYZ0\t\tYZ1")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                print(chr(65 + (cube[side][j][i] - 1) // (n*n)), i+1+j*n, sep="" ,end=" ")
            print("\t", end="")
        print()

def order_cube(cube, n):
    cube = np.copy(cube)
    counter = 1
    for side in range(6):
        for i in range(n):
            for j in range(n):
                cube[side][i][j] = counter #each tile is individual number
                counter += 1
    return cube

def randomize_cube(cube, n): #CHANGE LATER TO BE RANDOM TURNS, because this rand does not guarantee solution
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

def inv(arr):
    return arr[::-1]

#0-XY0  1-XY1  2-XZ0  3-XZ1  4-YZ0  5-YZ1
#cube[side, h, :] - horizonral
#cube[side, :, v] - vertical
def turn(cube, n, slice: int, axis: int, rotation: int = -1): #slice 1-n, axis 1-3, rotation 1 or -1
    cube = np.copy(cube)
    slice -= 1
    rot = [0, 0, 0, 0]
    rotslices = [0 for _ in range(4)]
    if axis == 1:
        rot = [0, 3, 1, 2]
        rotslices[0] = np.copy(cube[rot[0], :, slice])
        rotslices[1] = np.copy(cube[rot[1], n-1-slice, :])
        rotslices[2] = np.copy(cube[rot[2], :, n-1-slice])
        rotslices[3] = np.copy(cube[rot[3], slice, :])
        if rotation == -1:
            cube[rot[0], :, slice], cube[rot[1], n-1-slice, :], cube[rot[2], :, n-1-slice], cube[rot[3], slice, :] = inv(rotslices[(0 + rotation) % 4]), rotslices[(1 + rotation) % 4], inv(rotslices[(2 + rotation) % 4]), rotslices[(3 + rotation) % 4]
        elif rotation == 1:
            cube[rot[0], :, slice], cube[rot[1], n-1-slice, :], cube[rot[2], :, n-1-slice], cube[rot[3], slice, :] = rotslices[(0 + rotation) % 4], inv(rotslices[(1 + rotation) % 4]), rotslices[(2 + rotation) % 4], inv(rotslices[(3 + rotation) % 4])
    elif axis == 2:
        rot = [0, 5, 1, 4]
        rotslices[0] = np.copy(cube[rot[0], slice, :])
        rotslices[1] = np.copy(cube[rot[1], slice, :])
        rotslices[2] = np.copy(cube[rot[2], slice, :])
        rotslices[3] = np.copy(cube[rot[3], slice, :])
        cube[rot[0], slice, :], cube[rot[1], slice, :], cube[rot[2], slice, :], cube[rot[3], slice, :] = rotslices[(0 + rotation) % 4], rotslices[(1 + rotation) % 4], rotslices[(2 + rotation) % 4], rotslices[(3 + rotation) % 4]
    elif axis == 3:
        rot = [2, 5, 3, 4]
        rotslices[0] = np.copy(cube[rot[0], :, slice])
        rotslices[1] = np.copy(cube[rot[1], :, slice])
        rotslices[2] = np.copy(cube[rot[2], :, slice])
        rotslices[3] = np.copy(cube[rot[3], :, n-1-slice])
        if rotation == -1:
            cube[rot[0], :, slice], cube[rot[1], :, slice], cube[rot[2], :, slice], cube[rot[3], :, n-1-slice] = inv(rotslices[(0 + rotation) % 4]), rotslices[(1 + rotation) % 4], rotslices[(2 + rotation) % 4], inv(rotslices[(3 + rotation) % 4])
        elif rotation == 1:
            cube[rot[0], :, slice], cube[rot[1], :, slice], cube[rot[2], :, slice], cube[rot[3], :, n-1-slice] = rotslices[(0 + rotation) % 4], rotslices[(1 + rotation) % 4], inv(rotslices[(2 + rotation) % 4]), inv(rotslices[(3 + rotation) % 4])
    return cube

n = 3 #the NxN cube sides
my_cube = np.array([[[0 for _ in range(n)] for _ in range(n)] for _ in range(6)])
my_cube = order_cube(my_cube, n)
print_cube_letters(my_cube, n)