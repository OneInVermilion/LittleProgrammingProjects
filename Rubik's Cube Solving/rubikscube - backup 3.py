import numpy as np
import random


def print_cube_raw(cube, n: int): #prints raw contents of 3d array
    cube = np.copy(cube)
    for side in range(6):
        for i in range(n):
            for j in range(n):
                print("cube[", side, "][", i, "][", j, "] == ", cube[side][i][j], sep="")

def print_cube_values(cube, n: int): #print cube with the values of its tiles
    cube = np.copy(cube)
    l = 1 #longest string representing a value, e.g. for 00 01 02 it's 2, for 0 1 2 it's 1, for 00 4 5 it's 2
    spaces = " " * ((l+1) * n - 4) + "\t" #spaces accounting for potential length of cube printing, so that name of each face begins where said face's printing begins
    print("XY0", spaces, "XY1", spaces, "XZ0", spaces, "XZ1", spaces, "YZ0", spaces, "YZ1", sep="")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                #if (cube[side][j][i] < 10): print("0", end="")
                print(cube[side][j][i], end=" ")
            print("\t", end="")
        print()

def print_cube_letters(cube, n: int): #print cube with a letter A-F which signifies original side of tile, and a number 1-9
    cube = np.copy(cube)
    spaces = " " * (3 * n - 4) + "\t"
    print("XY0", spaces, "XY1", spaces, "XZ0", spaces, "XZ1", spaces, "YZ0", spaces, "YZ1", sep="")
    for j in range(n):
        for side in range(6):
            for i in range(n):
                print(chr(65 + (cube[side][j][i] - 1) // (n*n)), i+1+j*n, sep="" ,end=" ")
            print("\t", end="")
        print()

def inv(arr):
    return arr[::-1]

def turn(cube, n: int, slice: int, axis: int, rotation: int = -1): # makes a turn on a rubik's cube of x slice, around 1 out of 3 axis of rotation, in either direction
    if not (slice >= 1 and slice <= n and axis in (1, 2, 3) and rotation in (-1, 1)):
        print("IMPOSSIBLE TURN DETECTED WITH PARAMETERS", slice, axis, rotation)
        print("MAKE SURE THAT 1 <= Slice <= n; 1 <= axis <= 3; rotation == -1 or 1")
        return cube
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

def order_cube(cube, n: int): #make each tile of cube to have an orderded nubmer (1-54 for 3x3 cube, for example)
    cube = np.copy(cube)
    counter = 1
    for side in range(6):
        for i in range(n):
            for j in range(n):
                cube[side][i][j] = counter
                counter += 1
    return cube

def colorfill_cube(cube, n: int): #make each tile of cube have a number that is shared among the face, just like colors in real rubik's cube
    cube = np.copy(cube)
    for side in range(6):
        for i in range(n):
            for j in range(n):
                cube[side][i][j] = side
    return cube

def randomize_cube(cube, n: int, strength: int): #randomizes cube so that solution is guaranteed, making random turns of cube
    cube = np.copy(cube)
    for r in range(strength):
        slice_rand = random.randint(1, n)
        axis_rand = random.randint(1, 11) % 3 + 1
        rotation_rand = random.randint(0, 1)
        if rotation_rand == 0: rotation_rand = -1
        cube = turn(cube, n, slice_rand, axis_rand, rotation_rand)
        print("Random Turn:", slice_rand, axis_rand, rotation_rand)
    return cube

n = 2 #the NxN cube sides
my_cube = np.array([[[0 for _ in range(n)] for _ in range(n)] for _ in range(6)])
my_cube = colorfill_cube(my_cube, n)
my_cube = randomize_cube(my_cube, n, 10)
print_cube_values(my_cube, n)