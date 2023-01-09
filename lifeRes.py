# displays a variation of the game of life where a 16-bit number creates a frame for an 8-bit number
# the bits of the 16-bit number are kept static
# the focus is on the 8-bit number, how it changes and whether it will stabilize
# use in command line: python lifeRes.py x y
# x is the 16-bit number and numbers large then 65535 will have large bits dropped
# y is the 8-bit number and all bits large than 8 will be dropped. so 256 will be same as 0, 257 = 1, and so on


import random as r, numpy as np, matplotlib.pyplot as plt, matplotlib.animation as ani, sys


def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(1, 4):
        for j in range(1, 4):
            total = (grid[i, (j - 1) % N], grid[i, (j + 1) % N],
                     grid[(i - 1) % N, j], grid[(i + 1) % N, j],
                     grid[(i - 1) % N, (j - 1) % N], grid[(i - 1) % N, (j + 1) % N],
                     grid[(i + 1) % N, (j - 1) % N], grid[(i + 1) % N, (j + 1) % N]).count(True)
            if grid[i, j]:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = False
            else:
                if total == 3:
                    newGrid[i, j] = True
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def main(e, p):
    if e == -1:
        e = r.randrange(0, 65536)
    if p == -1:
        p = r.randrange(0, 256)
    env = list(np.array(np.unpackbits(np.array([e], dtype=np.uint16).view(np.uint8), bitorder='little'), dtype=bool))
    perm = list(np.array(np.unpackbits(np.array([p], dtype=np.uint8), bitorder='little'), dtype=bool))
    N = 5
    grid = np.array([env[:5], [env[15]] + perm[:3] + [env[5]],
                     [env[14], perm[7], False, perm[3], env[6]],
                     [env[13]] + [perm[6]] + [perm[5]] + [perm[4]] + [env[7]],
                     [env[12]] + [env[11]] + [env[10]] + [env[9]] + [env[8]]])
    print(grid, '\n', e, p)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, vmin=0, vmax=1)
    anime = ani.FuncAnimation(fig, update, fargs=(img, grid, N), frames=30, interval=1000)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main(-1, -1)
    else:
        main(sys.argv[1], sys.argv[2])
