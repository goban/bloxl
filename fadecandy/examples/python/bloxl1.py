#!/usr/bin/python

import opc, time, random, PIL, numpy, os, os.path
import glob
from PIL import Image
from numpy import array

numLEDs = 800
client = opc.Client('localhost:7890')

w, h = 4, 200;
bloxes = [[0 for x in range(w)] for y in range(h)]
tree = [0, 10, 20, 30, 40, 60, 70, 80, 110, 120, 130, 150, 160, 170, 21, 61, 81, 111, 151, 22, 62, 72, 112, 122, 152,
        162, 23, 63, 83, 113, 153, 24, 64, 94, 114, 124, 134, 154, 164, 174]
stone = [199, 189, 179, 159, 129, 99, 59, 19, 9, 178, 158, 148, 128, 108, 88, 58, 28, 187, 177, 157, 137, 127, 107, 87,
         57, 17, 176, 156, 126, 106, 86, 56, 6, 195, 185, 175, 155, 125, 95, 65, 55, 45, 25, 15]

narrr = [3, 4, 5, 6, 14, 25, 33, 34, 35, 36, 54, 55, 56, 63, 65, 74, 75, 76, 93, 94, 95, 96, 103, 105, 113, 114, 116,
         133, 134, 135, 136, 143, 145, 153, 154, 156, 173, 174, 175, 176, 183, 185, 193, 194, 196]
altnarr = [0, 1, 10, 11, 20, 21, 30, 31, 40, 41, 50, 51, 60, 61, 70, 71, 80, 81, 90, 91, 100, 101, 110, 111, 120, 121,
           130, 131, 140, 141, 150, 151, 160, 161, 170, 171, 180, 181, 190, 191, 199, 198, 189, 188, 179, 178, 169, 168,
           159, 158, 149, 148, 139, 138, 129, 128, 119, 118, 109, 108, 99, 98, 89, 88, 79, 78, 69, 68, 59, 58, 49, 48,
           39, 38, 29, 28, 19, 18, 9, 8]
hearts = [782, 791, 822, 741, 752, 781, 792, 821, 832, 861, 713, 740, 753, 780, 793, 820, 833, 860, 873, 900, 674, 699,
          714, 739, 754, 779, 794, 819, 834, 859, 874, 899, 914, 675, 698, 715, 738, 755, 778, 795, 818, 835, 858, 875,
          898, 915, 938, 716, 737, 756, 777, 796, 817, 836, 857, 876, 897, 916, 937, 956, 757, 776, 797, 816, 837, 856,
          877, 896, 917, 936, 957, 976, 758, 775, 798, 815, 838, 855, 878, 895, 918, 935, 958, 975, 719, 734, 759, 774,
          799, 814, 839, 854, 879, 894, 919, 934, 959, 680, 693, 720, 6733, 760, 773, 800, 813, 840, 853, 880, 893, 920,
          933, 681, 692, 721, 732, 761, 772, 801, 812, 841, 852, 881, 892, 921, 722, 731, 762, 771, 802, 811, 842, 851,
          882, 891, 730, 763, 770, 803, 8810, 843, 850, 769, 804, 809]
grid = [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
        [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191],
        [2, 12, 22, 32, 42, 52, 62, 72, 82, 92, 102, 112, 122, 132, 142, 152, 162, 172, 182, 192],
        [3, 13, 23, 33, 43, 53, 63, 73, 83, 93, 103, 113, 123, 133, 143, 153, 163, 173, 183, 193],
        [4, 14, 24, 34, 44, 54, 64, 74, 84, 94, 104, 114, 124, 134, 144, 154, 164, 174, 184, 194],
        [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175, 185, 195],
        [6, 16, 26, 36, 46, 56, 66, 76, 86, 96, 106, 116, 126, 136, 146, 156, 166, 176, 186, 196],
        [7, 17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117, 127, 137, 147, 157, 167, 177, 187, 197],
        [8, 18, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198],
        [9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119, 129, 139, 149, 159, 169, 179, 189, 199]]

clearall = [(0, 0, 0)] * numLEDs

pixels = [(0, 0, 0)] * numLEDs * 2


def BlockImages(loopcount):
    for q in range(loopcount):
        for filepath in glob.iglob('morph/*.jpg'):
            img = Image.open(filepath)
            arr = array(img)

            print('arr')
            print(arr)
            print()
            print('grid')
            print(grid)
            print()
            print('bloxes')
            print(bloxes)
            print()
            pixels = [(0, 0, 0)] * numLEDs
            for e in range(4):
                for t in range(10):
                    for u in range(20):
                        # print('t: {0}'.format(t))
                        # print('u: {0}'.format(u))
                        # print('e: {0}'.format(e))

                        # print('gridpos: {0}'.format(gridpos))
                        # print('bloxespos: {0}'.format(bloxespos))
                        gridpos = grid[t][u]
                        bloxespos = bloxes[gridpos][e]
                        pixels[bloxespos] = arr[t][u]

            print('pixels')
            print(bloxes)
            print('###########################')
            client.put_pixels(pixels)
            time.sleep(2)


def Narrrloop2(loopcount):
    j = 0
    w = 0
    for q in range(200):
        for e in range(4):
            bloxes[q][e] = w
            w += 1
            print(bloxes[q][e])
    pixels = [(0, 0, 0)] * numLEDs * 2
    t = 0
    color = 0
    color2 = 180
    for i in range(loopcount):
        j += 1
        pixels = [(0, 0, 0)] * numLEDs * 2
        for e in range(4):
            for y in range(len(narrr)):
                if narrr[y] + max(0, (190 - ((j / 10) * 10))) <= 199:
                    pixels[bloxes[narrr[y] + max(0, (190 - ((j / 10) * 10)))][e]] = wheel(color)
            for u in range(len(altnarr)):
                if (u == t):
                    pixels[bloxes[altnarr[u]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 1)]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 3)]][e]] = wheel(color2)

        client.put_pixels(pixels[:numLEDs])
        time.sleep(.1)
        color += 1
        color2 += 1
        t += 1
        if (t > len(altnarr)):
            t = 0

        if color > 255:
            color = 0
        if color2 > 255:
            color2 = 0


def Narrrloop(loopcount):
    w = 0
    for q in range(200):
        for e in range(4):
            bloxes[q][e] = w
            w += 1
            print(bloxes[q][e])
    pixels = [(0, 0, 0)] * numLEDs
    t = 0
    color = 0
    color2 = 180
    for i in range(loopcount):
        pixels = [(0, 0, 0)] * numLEDs
        for e in range(4):
            for y in range(len(narrr)):
                pixels[bloxes[narrr[y]][e]] = wheel(color)
            for u in range(len(altnarr)):
                if (u == t):
                    pixels[bloxes[altnarr[u]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 1)]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 3)]][e]] = wheel(color2)

        client.put_pixels(pixels)
        time.sleep(.1)
        color += 1
        color2 += 1
        t += 1
        if (t > len(altnarr)):
            t = 0

        if color > 255:
            color = 0
        if color2 > 255:
            color2 = 0


def Treeloop(loopcount):
    w = 0
    for q in range(200):
        for e in range(4):
            bloxes[q][e] = w
            w += 1
            print(bloxes[q][e])
    pixels = [(0, 0, 0)] * numLEDs
    t = 0
    color = 0
    color2 = 180
    for i in range(loopcount):
        pixels = [(0, 0, 0)] * numLEDs
        for e in range(4):
            for y in range(len(tree)):
                pixels[bloxes[tree[y]][e]] = wheel(color)
            for y in range(len(stone)):
                pixels[bloxes[stone[y]][e]] = wheel(color2)
            for u in range(len(altnarr)):
                if (u == t):
                    pixels[bloxes[altnarr[u]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 1)]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u - 3)]][e]] = wheel(color2)

        client.put_pixels(pixels)
        time.sleep(.1)
        color += 1
        color2 += 1
        t += 1
        if (t > len(altnarr)):
            t = 0

        if color > 255:
            color = 0
        if color2 > 255:
            color2 = 0


def blox0(loopcount):
    z = 0
    y = 0
    q = 0
    g = 0
    r = 0
    pixels = [(0, 0, 0)] * numLEDs
    color = random.randint(33, 255)
    color2 = random.randint(33, 255)
    for i in range(loopcount):
        pixels = [(0, 0, 0)] * numLEDs

        for e in range(4):
            pixels[y + e] = wheel(color)
            if r == 0:
                if (z - 40 > 0):
                    pixels[(z - 40) + e] = wheel(color)
            if r == 1:
                if ((z - 40) + 4 > 0):
                    pixels[((z - 40) + 4) + e] = wheel(color)
            if r == 2:
                if ((z + 4) < 799):
                    pixels[(z + 4) + e] = wheel(color)
            if r == 3:
                if ((z + 40) + 4 < 799):
                    pixels[(z + 40) + 4] = wheel(color)
            if r == 4:
                if (z + 40 < 799):
                    pixels[(z + 40)] = wheel(color)
            if r == 5:
                if ((z + 40) - 4 > 0):
                    pixels[(z - 40) - 4] = wheel(color)
            if r == 6:
                if (z - 4 > 0):
                    pixels[z - 4] = wheel(color)
            if r == 7:
                if ((z - 40) - 4 > 0):
                    pixels[(z - 40) - 4] = wheel(color)
            pixels[z + e] = wheel(color2)
            if (y - 1 > 0):
                pixels[(y - 1) + e] = wheel(color2)

        client.put_pixels(pixels)
        time.sleep(.1)
        r += 1
        if r > 7:
            r = 0
        z += 40
        y += 4

        if y > 799:
            y = 0
        if z > 799:
            z = g + 4
            g = g + 4
        if g > 39:
            g = 0
            t = 0
            for s in range(40):
                for q in range(numLEDs):
                    if q % 4 == 0:
                        pixels[q - t] = wheel(color)
                        pixels[q - (t - 1)] = wheel(color - 20)

                client.put_pixels(pixels)
                time.sleep(.2)
                pixels = [(0, 0, 0)] * numLEDs
                t += 1
                if t > 4:
                    t = 0
        color += 2
        if color > 255:
            color = 20
        if color2 > 255:
            color = 0


def wheel(WheelPos):
    if WheelPos < 85:
        color = ((WheelPos * 3), (255 - WheelPos * 3), 0)
    else:
        if WheelPos < 170:
            WheelPos -= 85
            color = ((255 - WheelPos * 3), 0, (WheelPos * 3))
            return color
        else:
            WheelPos -= 170
            color = (0, (WheelPos * 3), (255 - WheelPos * 3))
            return color


def run_pattern():
    for i in range(0, 10000):
        BlockImages(500)
        Treeloop(1000)
        Narrrloop2(1000)
        Narrrloop(1000)
        blox0(1000)


run_pattern()
