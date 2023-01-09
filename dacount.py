# experiment trying to find useful patterns in Conway style cellular automata
# uses game of life rules in a restricted 5x5 grid
# the grid is arranged by wrapping the bits of the 16-bit int around the outside of the grid starting at
# the top left and going clockwise around the grid
# these cells are kept static and only used to affect the rest of the grid
# function generates every reaction from an 8-bit number surrounded by a 16-bit number based on game of life rules
# and records data such as whether combinations that fall into a pattern or combinations that freeze
# particular attention is placed on the center value and how often it lives or dies
# script will create a json file with the results of each number combination
# TODO pickle the output file for easier future use

import random as r, multiprocessing as mp, numpy as np, json


def test_perm(env_int):
    if env_int in [1000, 5000, 10000, 25000, 50000]:  # track progress
        print(env_int)

    # turn number into a list of bits and setup tracking variables
    env = list(np.array(np.unpackbits(np.array([env_int], dtype=np.uint16).view(np.uint8), bitorder='little'), dtype=bool))
    lock_on = 0
    lock_off = 0
    loop = 0
    fire_rates = []
    fire_counts = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '>5': 0}

    # runs the game for all 8-bit numbers
    for x in range(256):
        perm = list(np.array(np.unpackbits(np.array([x], dtype=np.uint8), bitorder='little'), dtype=bool))
        n = 5
        grid = np.array([env[:5],
                         [env[15]] + perm[:3] + [env[5]],
                         [env[14], perm[7], False, perm[3], env[6]],
                         [env[13]] + [perm[6]] + [perm[5]] + [perm[4]] + [env[7]],
                         [env[12]] + [env[11]] + [env[10]] + [env[9]] + [env[8]]])
        not_done = True
        seq = []
        num_fires = 0
        while not_done:
            new_grid = grid.copy()
            last_inner = np.array(grid[1:4, 1:4])
            for i in range(1, 4):
                for j in range(1, 4):
                    total = (grid[i, (j - 1) % n], grid[i, (j + 1) % n],
                             grid[(i - 1) % n, j], grid[(i + 1) % n, j],
                             grid[(i - 1) % n, (j - 1) % n], grid[(i - 1) % n, (j + 1) % n],
                             grid[(i + 1) % n, (j - 1) % n], grid[(i + 1) % n, (j + 1) % n]).count(True)
                    if grid[i, j]:
                        if (total < 2) or (total > 3):
                            new_grid[i, j] = False
                    else:
                        if total == 3:
                            new_grid[i, j] = True
            inner_grid = np.array(new_grid[1:4, 1:4])
            match = [m for m in seq if np.array_equal(inner_grid, m)]
            if (inner_grid == last_inner).all():  # check for freeze
                seq.append(inner_grid)
                if inner_grid[1, 1]:
                    num_fires += 1
                    seq.append('locked repeat on after %d' % len(seq))
                    lock_on += 1
                else:
                    seq.append('locked repeat off after %d' % len(seq))
                    lock_off += 1
                not_done = False
            elif len(match) > 0:  # check for loops
                index = 0
                for s in seq:
                    if np.array_equal(inner_grid, s):
                        break
                    else:
                        index += 1
                cycle_len = len(seq) - index
                number_fires = len([f for f in seq[index:] if f[1, 1]])
                seq.append('cycle from %d with length %d and %d fires' % (index, cycle_len, number_fires))
                loop += 1
                if number_fires not in fire_rates:
                    fire_rates.append(number_fires)
                if inner_grid[1, 1]:
                    num_fires += 1
                not_done = False
            else:
                if inner_grid[1, 1]:
                    num_fires += 1
                seq.append(inner_grid)
            grid = new_grid
        if num_fires == 0:
            fire_counts['0'] += 1
        if num_fires == 1:
            fire_counts['1'] += 1
        if num_fires == 2:
            fire_counts['2'] += 1
        if num_fires == 3:
            fire_counts['3'] += 1
        if num_fires == 4:
            fire_counts['4'] += 1
        if num_fires == 5:
            fire_counts['5'] += 1
        if num_fires > 5:
            fire_counts['>5'] += 1
    return {env_int: {'locked on': lock_on,
                          'locked off': lock_off,
                          'looping': loop,
                          'fire rates': fire_rates,
                           'fire counts': fire_counts}}


def test_env(perm_int):  # same as test_perm but creates the data from the 8-bit number perspective
    if perm_int in [20, 60, 120, 240]:
        print(perm_int)
    perm = list(np.array(np.unpackbits(np.array([perm_int], dtype=np.uint8), bitorder='little'), dtype=bool))
    lock_on = 0
    lock_off = 0
    loop = 0
    fire_rates = []
    fire_counts = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '>5': 0}
    for x in range(65536):
        env = list(np.array(np.unpackbits(np.array([x], dtype=np.uint16).view(np.uint8), bitorder='little'), dtype=bool))
        n = 5
        grid = np.array([env[:5],
                         [env[15]] + perm[:3] + [env[5]],
                         [env[14], perm[7], False, perm[3], env[6]],
                         [env[13]] + [perm[6]] + [perm[5]] + [perm[4]] + [env[7]],
                         [env[12]] + [env[11]] + [env[10]] + [env[9]] + [env[8]]])
        not_done = True
        seq = []
        num_fires = 0
        while not_done:
            new_grid = grid.copy()
            last_inner = np.array(grid[1:4, 1:4])
            for i in range(1, 4):
                for j in range(1, 4):
                    total = (grid[i, (j - 1) % n], grid[i, (j + 1) % n],
                             grid[(i - 1) % n, j], grid[(i + 1) % n, j],
                             grid[(i - 1) % n, (j - 1) % n], grid[(i - 1) % n, (j + 1) % n],
                             grid[(i + 1) % n, (j - 1) % n], grid[(i + 1) % n, (j + 1) % n]).count(True)
                    if grid[i, j]:
                        if (total < 2) or (total > 3):
                            new_grid[i, j] = False
                    else:
                        if total == 3:
                            new_grid[i, j] = True
            inner_grid = np.array(new_grid[1:4, 1:4])
            match = [m for m in seq if np.array_equal(inner_grid, m)]
            if (inner_grid == last_inner).all():
                seq.append(inner_grid)
                if inner_grid[1, 1]:
                    num_fires += 1
                    seq.append('locked repeat on after %d' % len(seq))
                    lock_on += 1
                else:
                    seq.append('locked repeat off after %d' % len(seq))
                    lock_off += 1
                not_done = False
            elif len(match) > 0:
                index = 0
                for s in seq:
                    if np.array_equal(inner_grid, s):
                        break
                    else:
                        index += 1
                cycle_len = len(seq) - index
                number_fires = len([f for f in seq[index:] if f[1, 1]])
                seq.append('cycle from %d with length %d and %d fires' % (index, cycle_len, number_fires))
                loop += 1
                if number_fires not in fire_rates:
                    fire_rates.append(number_fires)
                if inner_grid[1, 1]:
                    num_fires += 1
                not_done = False
            else:
                if inner_grid[1, 1]:
                    num_fires += 1
                seq.append(inner_grid)
            grid = new_grid
        if num_fires == 0:
            fire_counts['0'] += 1
        if num_fires == 1:
            fire_counts['1'] += 1
        if num_fires == 2:
            fire_counts['2'] += 1
        if num_fires == 3:
            fire_counts['3'] += 1
        if num_fires == 4:
            fire_counts['4'] += 1
        if num_fires == 5:
            fire_counts['5'] += 1
        if num_fires > 5:
            fire_counts['>5'] += 1
    return {perm_int: {'locked on': lock_on,
                       'locked off': lock_off,
                       'looping': loop,
                       'fire rates': fire_rates,
                       'fire counts': fire_counts}}


def main():
    """bits = set(list(combo_r([True, False, True, False, True, False, True, False], 8)))
    env = []
    t = 16
    while t > 0:
        env.append(bool(r.getrandbits(1)))
        t -= 1"""  # for testing
    pool = mp.Pool(processes=6)  # set number of processing threads
    ra = pool.map(test_env, range(256))
#    ra = pool.map(test_perm, range(65536))  # swap lines to test with
    raw = {}
    for num in ra:
        raw.update(num)
    with open('raw.txt', 'r+') as file:
        file.write(json.dumps(raw))


if __name__ == '__main__':
    main()
