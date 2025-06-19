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

def turn_many(cube, n: int, moves):
    cube = np.copy(cube)
    for move in moves:
        cube = turn(cube, n, move[0], move[1], move[2])
    return cube

def init_cube(n: int):
    return np.array([[[0 for _ in range(n)] for _ in range(n)] for _ in range(6)])

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
    turns = []
    for r in range(strength):
        slice_rand = random.randint(1, n)
        axis_rand = random.randint(1, 11) % 3 + 1
        rotation_rand = random.randint(0, 1)
        if rotation_rand == 0: rotation_rand = -1
        cube = turn(cube, n, slice_rand, axis_rand, rotation_rand)
        turns.append((slice_rand, axis_rand, rotation_rand))
    return (cube, turns)

def num_to_turn(num: int):
    dir = num % 2
    if dir == 0: dir = -1
    num //= 2
    axis = num % 3 + 1
    num //= 3
    slice = num + 1
    return (slice, axis, dir)

def is_solved(cube):
    cube = np.copy(cube)
    for side in cube:
        init_color = side[0][0]
        for i in side:
            for j in i:
                if j != init_color:
                    return False
    return True

def cube_to_str(cube, n: int):
    cube = np.copy(cube)
    string = ""
    for side in cube:
        for i in side:
            for j in i:
                string += str(j)
    return string

def cube_from_str(str: str, n: int):
    counter = 0
    cube = init_cube(n)
    for side in range(6):
        for i in range(n):
            for j in range(n):
                cube[side][i][j] = int(str[counter])
                counter += 1
    return cube

def dfs(cube_state, n: int, maxdepth: int, path=None, visited=None, depth=0):
    if path is None: path = []
    if visited is None: visited = set()
    if is_solved(cube_state):
        print(path)
        return True
    cube_id = cube_to_str(cube_state, n)
    if (cube_id in visited) or (depth > maxdepth):
        return False
    visited.add(cube_id)
    for i in range(6*n):
        potential_turn = num_to_turn(i)
        new_cube_state = turn(cube_state, n, potential_turn[0], potential_turn[1], potential_turn[2])
        path.append(potential_turn)
        if dfs(new_cube_state, n, maxdepth, path, visited, depth + 1): return True
        path.pop()
    return False


n = 3 #the NxN cube sides
s = 5 #strength of cube randomizing
mode = 2 #1 for solving, 2 for testing

if mode == 1: #solving
    my_cube, random_turns = randomize_cube(colorfill_cube(init_cube(n), n), n, s)
    print_cube_values(my_cube, n)
    print(cube_to_str(my_cube, n))
    print(random_turns)
    dfs(my_cube, n, s+1)
elif mode == 2: #testing
    my_cube_id = "535030535424121424222505222333414333000444000111555111"
    solution = [(1, 1, -1), (1, 1, -1), (1, 1, -1), (2, 1, -1), (1, 1, -1), (1, 2, -1), (3, 2, -1)]
    new_cube = cube_from_str(my_cube_id, n)
    new_cube = turn_many(new_cube, n, solution)
    print_cube_values(new_cube, n)