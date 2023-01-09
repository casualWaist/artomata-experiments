# a cellular automata where the cells or pixels swap color values based on the averages of the whole image
# different algorithms have different rules creating different results
# the results can also be manipulated by restricting the color value ranges
# can also use an image for the starting values
# 100 x 100 is the default size runs well on my machine but will slow quickly if increased
# run from the command line: python pixelLife.py (algo) (r) (g) (b) (image)
# input values:
#   algo = 1 - 5
#   r, g, b = 1, 2, 3, or int up to 254
#   image = path/to/image or null
# r, g, b values:
#   1 = full range of values 0 --- 255
#   2 = lower half of range 0 --- 127
#   3 = upper half of range 128 --- 255
#   any other number up to 254 wil give a range from that number to 255, greater than 254 will crash
# a prompt to save the resulting video will appear after the plot is closed

import numpy as np
from random import randrange as rr
from matplotlib.animation import FuncAnimation as FA
from PIL import Image
from datetime import datetime as DT
import matplotlib.pyplot as plt
from imageio.v2 import imread
import sys

ARG = 1  # Default algorithm to run
WIDTH = 100  # Width and height of the image
# WTR = AWR['ffmpeg']
VID = [Image.new('RGB', (WIDTH, WIDTH), (0, 0, 0))]


def rgb_to_h(r, g, b):  # turns rgb values into degrees based on the dominant color
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if df == 0.0:
        df = 0.001
    h = 0
    if mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    return h


def deg_to_ab(j):  # turns degrees into a simple vector used to define the rules
    a = 0
    b = 0
    if j <= 22:
        a = 1
    elif 22 < j <= 67:
        a = 1
        b = 1
    elif 67 < j <= 112:
        b = 1
    elif 112 < j <= 157:
        a = -1
        b = 1
    elif 157 < j <= 202:
        a = -1
    elif 202 < j <= 247:
        a = -1
        b = -1
    elif 247 < j <= 292:
        b = -1
    elif 292 < j <= 337:
        a = 1
        b = -1
    else:
        a = 1
    return a, b


def live(l, m, n):
    o = rr(0, 10) * m
    p = rr(0, 10) * (n/m)
    q = rr(0, 10) * n
    return l + o + p + q


def update1(frameNum, img, pixs):  # compares local averages to global averages
    newpixs = pixs.copy()
    rgb = [np.average(pixs[:, :, 0]), np.average(pixs[:, :, 1]), np.average(pixs[:, :, 2])]
    jib = int(rgb_to_h(rgb[0], rgb[1], rgb[2]))
    c, d = deg_to_ab(jib)
    for x in range(1, np.size(pixs, 0) - 1):
        for y in range(1, np.size(pixs, 1) - 1):
            r = np.average(pixs[x-1:x+1, y-1:y+1, 0])
            g = np.average(pixs[x-1:x+1, y-1:y+1, 1])
            b = np.average(pixs[x-1:x+1, y-1:y+1, 2])
            l = live(0, 0.1, 0.01)
            jab = int(rgb_to_h(r, g, b))
            if jab > jib:
                l = int(l)
            else:
                l = round(l)
            e, f = deg_to_ab(jab)
            if r >= g and r >= b:
                if c >= e:
                    if d >= f:
                        newpixs[x, y, 0] = rr(0, 256, rr(6, 9))
                    else:
                        newpixs[x, y, 1] = pixs[x+c, y+f, l]
                else:
                    if d > f:
                        newpixs[x, y, 1] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 2] = pixs[x+c, y+d, l]
            elif b > r and b > g:
                if c > e:
                    if d > f:
                        newpixs[x, y, 2] = rr(0, 256, rr(1, 6))
                    else:
                        newpixs[x, y, 0] = pixs[x+c, y+f, l]
                else:
                    if d > f:
                        newpixs[x, y, 0] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 1] = pixs[x+c, y+d, l]
            else:
                if c > e:
                    if d > f:
                        newpixs[x, y, 1] = rr(84, 160, rr(1, 3))
                    else:
                        newpixs[x, y, 2] = pixs[x+c, y+f, l]
                else:
                    if d >= f:
                        newpixs[x, y, 2] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 0] = pixs[x+c, y+d, l]
    img.set_data(newpixs)
    VID.append(newpixs)
    pixs[:] = newpixs[:]
    return img


def update2(frameNum, img, pixs):
    newpixs = pixs.copy()
    rgb = [np.average(pixs[:, :, 0]), np.average(pixs[:, :, 1]), np.average(pixs[:, :, 2])]
    jib = int(rgb_to_h(rgb[0], rgb[1], rgb[2]))
    c, d = deg_to_ab(jib)
    for x in range(1, np.size(pixs, 0) - 1):
        for y in range(1, np.size(pixs, 1) - 1):
            r = np.average(pixs[x-1:x+1, y-1:y+1, 0])
            g = np.average(pixs[x-1:x+1, y-1:y+1, 1])
            b = np.average(pixs[x-1:x+1, y-1:y+1, 2])
            l = live(0, 0.1, 0.01)
            jab = int(rgb_to_h(r, g, b))
            if jab > jib:
                l = int(l)
            else:
                l = round(l)
            e, f = deg_to_ab(jab)
            if r >= g and r >= b:
                if c < e:
                    if d < f:
                        newpixs[x, y, 0] = pixs[x+c, y+d, l]
                    else:
                        newpixs[x, y, 1] = pixs[x+c, y+f, l]
                else:
                    if d > f:
                        newpixs[x, y, 1] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 2] = pixs[x+e, y+f, l]
            elif b > r and b > g:
                if c > e:
                    if d < f:
                        newpixs[x, y, 2] = pixs[x+c, y+d, l]
                    else:
                        newpixs[x, y, 0] = pixs[x+c, y+f, l]
                else:
                    if d > f:
                        newpixs[x, y, 0] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 1] = pixs[x+e, y+f, l]
            else:
                if c < e:
                    if d < f:
                        newpixs[x, y, 1] = pixs[x+c, y+d, l]
                    else:
                        newpixs[x, y, 2] = pixs[x+c, y+f, l]
                else:
                    if d > f:
                        newpixs[x, y, 2] = pixs[x+e, y+d, l]
                    else:
                        newpixs[x, y, 0] = pixs[x+e, y+f, l]
    img.set_data(newpixs)
    VID.append(newpixs)
    pixs[:] = newpixs[:]
    return img


def update3(frameNum, img, pixs):
    newpixs = pixs.copy()
    rgb = [np.average(pixs[:, :, 0]), np.average(pixs[:, :, 1]), np.average(pixs[:, :, 2])]
    jib = int(rgb_to_h(rgb[0], rgb[1], rgb[2]))
    c, d = deg_to_ab(jib)
    for x in range(1, np.size(pixs, 0) - 1):
        for y in range(1, np.size(pixs, 1) - 1):
            r = np.average(pixs[x-1:x+1, y-1:y+1, 0])
            g = np.average(pixs[x-1:x+1, y-1:y+1, 1])
            b = np.average(pixs[x-1:x+1, y-1:y+1, 2])
            jab = int(rgb_to_h(r, g, b))
            e, f = deg_to_ab(jab)
            if r > g and r > b:
                if c > e:
                    if pixs[x+c, y+e, 0] > newpixs[x, y, 0]:
                        newpixs[x, y, 0] = pixs[x+c, y+e, 0]
                    else:
                        newpixs[x, y, 1] = pixs[x + c, y + e, 1]
                else:
                    if pixs[x+d, y+f, 1] > newpixs[x, y, 1]:
                        newpixs[x, y, 1] = pixs[x+d, y+f, 1]
                    else:
                        newpixs[x, y, 2] = pixs[x + d, y + f, 2]
            elif g > r and g > b:
                if c > e:
                    if pixs[x+d, y+c, 2] > newpixs[x, y, 2]:
                        newpixs[x, y, 2] = pixs[x+d, y+c, 2]
                    else:
                        newpixs[x, y, 0] = pixs[x + d, y + c, 0]
                else:
                    if pixs[x+f, y+e, 0] > newpixs[x, y, 0]:
                        newpixs[x, y, 0] = pixs[x+f, y+e, 0]
                    else:
                        newpixs[x, y, 1] = pixs[x + f, y + e, 1]
            else:
                if c > e:
                    if pixs[x+f, y+d, 1] > newpixs[x, y, 1]:
                        newpixs[x, y, 1] = pixs[x+f, y+d, 1]
                    else:
                        newpixs[x, y, 2] = pixs[x + f, y + d, 2]
                else:
                    if pixs[x+e, y+c, 2] > newpixs[x, y, 2]:
                        newpixs[x, y, 2] = pixs[x+e, y+c, 2]
                    else:
                        newpixs[x, y, 0] = pixs[x + e, y + c, 0]
    img.set_data(newpixs)
    VID.append(newpixs)
    pixs[:] = newpixs[:]
    return img


def update4(frameNum, img, pixs):
    newpixs = pixs.copy()
    rgb = [np.average(pixs[:, :, 0]), np.average(pixs[:, :, 1]), np.average(pixs[:, :, 2])]
    roff = rgb[0] - np.average(rgb[1:])
    goff = rgb[1] - np.average([rgb[0], rgb[2]])
    boff = rgb[2] - np.average(rgb[:2])
    jib = int(rgb_to_h(rgb[0], rgb[1], rgb[2]))
    c, d = deg_to_ab(jib)
    for x in range(1, np.size(pixs, 0) - 1):
        for y in range(1, np.size(pixs, 1) - 1):
            r = np.average(pixs[x-1:x+1, y-1:y+1, 0])
            g = np.average(pixs[x-1:x+1, y-1:y+1, 1])
            b = np.average(pixs[x-1:x+1, y-1:y+1, 2])
            if r > g and r > b:
                if 120 < jib < 240:
                    newpixs[x, y] = pixs[x+c, y+d]
                else:
                    newpixs[x, y] = [r, pixs[x+c, y+d, 1], pixs[x+c, y+d, 2]]
            elif g > r and g > b:
                if jib < 240:
                    newpixs[x, y] = [pixs[x+c, y+d, 2], g, pixs[x+c, y+d, 0]]
                else:
                    newpixs[x, y] = pixs[x+c, y+d]
            else:
                if jib > 120:
                    newpixs[x, y] = [pixs[x+c, y+d, 1], pixs[x+c, y+d, 0], b]
                else:
                    newpixs[x, y] = pixs[x+c, y+d]
    img.set_data(newpixs)
    VID.append(newpixs)
    pixs[:] = newpixs[:]
    return img


def update5(frameNum, img, pixs):
    newpixs = pixs.copy()
    rgb = [np.average(pixs[:, :, 0]), np.average(pixs[:, :, 1]), np.average(pixs[:, :, 2])]
    jib = int(rgb_to_h(rgb[0], rgb[1], rgb[2]))
    c, d = deg_to_ab(jib)
    for x in range(1, np.size(pixs, 0) - 1):
        for y in range(1, np.size(pixs, 1) - 1):
            r = np.average(pixs[x-1:x+1, y-1:y+1, 0])
            g = np.average(pixs[x-1:x+1, y-1:y+1, 1])
            b = np.average(pixs[x-1:x+1, y-1:y+1, 2])
            jab = int(rgb_to_h(r, g, b))
            e, f = deg_to_ab(jab)
            if r > g and r > b:
                if 120 < jib < 240:
                    newpixs[x, y] = pixs[x+e, y+f]
                else:
                    newpixs[x, y] = pixs[x+c, y+d]
            elif g > r and g > b:
                if jib < 240:
                    newpixs[x, y] = pixs[x+c, y+d]
                else:
                    newpixs[x, y] = pixs[x+e, y+f]
            else:
                if jib > 120:
                    newpixs[x, y] = pixs[x+c, y+d]
                else:
                    newpixs[x, y] = pixs[x+e, y+f]
    img.set_data(newpixs)
    VID.append(newpixs)
    pixs[:] = newpixs[:]
    return img


def rand_rgb(rred, rg, rb):
    rgb = [0, 0, 0]
    if isinstance(rred, list):
        rgb[0] = rred[rr(0, len(rred))]
    else:
        if rred == 1:
            rgb[0] = rr(0, 256)
        elif rred == 2:
            rgb[0] = rr(0, 128)
        elif rred == 3:
            rgb[0] = rr(0, 86)
        elif rred > 3:
            rgb[0] = rr(rred, 256)
    if isinstance(rg, list):
        rgb[1] = rg[rr(0, len(rg))]
    else:
        if rg == 1:
            rgb[1] = rr(0, 256)
        elif rg == 2:
            rgb[1] = rr(0, 128)
        elif rg == 3:
            rgb[1] = rr(128, 256)
        elif rg > 3:
            rgb[1] = rr(rg, 256)
    if isinstance(rb, list):
        rgb[2] = rg[rr(0, len(rg))]
    else:
        if rb == 1:
            rgb[2] = rr(0, 256)
        elif rb == 2:
            rgb[2] = rr(0, 128)
        elif rb == 3:
            rgb[2] = rr(128, 256)
        elif rb > 3:
            rgb[2] = rr(rb, 256)
    return rgb


def pixArray(r, g, b):
    p = []
    for x in range(0, WIDTH):
        w = []
        for y in range(0, WIDTH):
            w.append(rand_rgb(r, g, b))
        p.append(w)
    return p


if __name__ == '__main__':
    if len(sys.argv) > 2:
        if len(sys.argv) > 5:
            pixels = np.array(imread(sys.argv[5]))  # reads image file if provided
        else:
            pixels = np.array(pixArray(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))
    else:
        pixels = np.array(pixArray(1, 1, 1))
    VID.append(pixels)
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    img = ax.imshow(pixels, interpolation='nearest')
    if len(sys.argv) > 1:
        anime = FA(fig, globals()[f'update{sys.argv[1]}'], fargs=(img, pixels), frames=100, interval=100)
    else:
        anime = FA(fig, globals()[f'update{ARG}'], fargs=(img, pixels), frames=100, interval=100)
    plt.show()
    unsure = True
    while unsure:
        ans = input('Do you want to save? (y, n)')
        if ans == 'y':
            unsure = False
            now = DT.now().strftime('%b-%d-%H:%M:%S')
            md = {'title': f'{sys.argv[1]} {sys.argv[2]} {sys.argv[3]} {sys.argv[4]} {now}.mp4', 'artist': 'Me'}
            '''writer = IMW(fps=30, metadata=md)
            with writer.saving(fig, md['title'], 200):
                for frame in VID:
                    img.set_data(frame)
                    writer.grab_frame()'''
            VID[0].save(md['title'], save_all=True)
            print('saved')
        elif ans == 'n':
            ans = input('Are you sure? (y, n)')
            if ans == 'y':
                unsure = False
                print('deleted')

