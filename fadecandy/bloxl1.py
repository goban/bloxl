#!/usr/bin/python

import opc, time, random, PIL, numpy, os, os.path
from PIL import Image
from numpy import array
numLEDs = 800
client = opc.Client('localhost:7890')



front = [[667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686],
                        [706,705,704,703,702,701,700,699,698,697,696,695,694,693,692,691,690,689,688,687],
                        [707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726],
                        [746,745,744,743,742,741,740,739,738,737,736,735,734,733,732,731,730,729,728,727],
                        [747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766],
                        [786,785,784,783,782,781,780,779,778,777,776,775,774,773,772,771,770,769,768,767],
                        [787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806],
                        [826,825,824,823,822,821,820,819,818,817,816,815,814,813,812,811,810,809,808,807],
                        [827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846],
                        [866,865,864,863,862,861,860,859,858,857,856,855,854,853,852,851,850,849,848,847],
                        [867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886],
                        [906,905,904,903,902,901,900,899,898,897,896,895,894,893,892,891,890,889,888,887],
                        [907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926],
                        [946,945,944,943,942,941,940,939,938,937,936,935,934,933,932,931,930,929,928,927],
                        [947,948,949,950,951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966],
                        [986,985,984,983,982,981,980,979,978,977,976,975,974,973,972,971,970,969,968,967]]
trinket = [[796,797,817,816,838,854,775,759,778,754,835,859],
           [796,797,817,816,815,814,776,757,795,794,836,857],
           [796,797,817,816,798,799,777,756,818,819,837,856]]
w, h = 4,200 ;
bloxes = [[0 for x in range(w)] for y in range(h)]
tree = [0,10,20,30,40,60,70,80,110,120,130,150,160,170,21,61,81,111,151,22,62,72,112,122,152,162,23,63,83,113,153,24,64,94,114,124,134,154,164,174]
stone = [199,189,179,159,129,99,59,19,9,178,158,148,128,108,88,58,28,187,177,157,137,127,107,87,57,17,176,156,126,106,86,56,6,195,185,175,155,125,95,65,55,45,25,15]

narrr = [3,4,5,6,14,25,33,34,35,36,54,55,56,63,65,74,75,76,93,94,95,96,103,105,113,114,116,133,134,135,136,143,145,153,154,156,173,174,175,176,183,185,193,194,196]
altnarr = [0,1,10,11,20,21,30,31,40,41,50,51,60,61,70,71,80,81,90,91,100,101,110,111,120,121,130,131,140,141,150,151,160,161,170,171,180,181,190,191,199,198,189,188,179,178,169,168,159,158,149,148,139,138,129,128,119,118,109,108,99,98,89,88,79,78,69,68,59,58,49,48,39,38,29,28,19,18,9,8]
hearts = [782,791,822,741,752,781,792,821,832,861,713,740,753,780,793,820,833,860,873,900,674,699,714,739,754,779,794,819,834,859,874,899,914,675,698,715,738,755,778,795,818,835,858,875,898,915,938,716,737,756,777,796,817,836,857,876,897,916,937,956,757,776,797,816,837,856,877,896,917,936,957,976,758,775,798,815,838,855,878,895,918,935,958,975,719,734,759,774,799,814,839,854,879,894,919,934,959,680,693,720,6733,760,773,800,813,840,853,880,893,920,933,681,692,721,732,761,772,801,812,841,852,881,892,921,722,731,762,771,802,811,842,851,882,891,730,763,770,803,8810,843,850,769,804,809]
FrontCircle = [697,696,718,734,760,772,801,812,841,853,879,895,917,916,898,874,860,832,821,781,792,753,739,739,715]
FrontSparkle = [907,889,730,705,711,960,684,749,851,948,685,827,800,943,671,883,675,910,805,785,963,744,704,880,700,986,730,784,945,728,677,784,965,908,889,750,966]

clearall = [ (0, 0, 0)] * numLEDs





pixels = [ (0,0,0) ] * numLEDs * 2

def BlockImages(loopcount):

	for q in range(loopcount):
		MorphImages = []
		NumFiles = len([name for name in os.listdir('./morph') if os.path.isfile(name)])
		print(NumFiles)
		for i in range(48):
			MorphImages.append("./morph/morph"+str(i)+".jpg")
		print(MorphImages)
		for picture in range(len(MorphImages)):
			img = Image.open(MorphImages[picture])
			arr = array(img)
			pixels = [ (0,0,0) ] * numLEDs

			for t in range(10):
				for u in range(20):
					pixels[bloxes[t][u]] = arr[t][u]
					print(pixels)
				
			
			client.put_pixels(pixels)
			time.sleep(2)


def Narrrloop2(loopcount):
    j = 0
    w = 0
    for q in range(200):
        for e in range(4):
            bloxes[q][e] = w
            w += 1
            print bloxes[q][e]
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
                    pixels[bloxes[narrr[y]+ max(0, (190 - ((j / 10) * 10)))][e] ] = wheel(color)
            for u in range(len(altnarr)):
                if ( u == t):
                    pixels[bloxes[altnarr[u]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u -1)]][e]]= wheel(color2)
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
            print bloxes[q][e]
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
                if ( u == t):
                    pixels[bloxes[altnarr[u]][e]] = wheel(color2)
                    pixels[bloxes[altnarr[(u -1)]][e]]= wheel(color2)
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
            print bloxes[q][e]
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
					if ( u == t):
						pixels[bloxes[altnarr[u]][e]] = wheel(color2)
						pixels[bloxes[altnarr[(u -1)]][e]]= wheel(color2)
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
        pixels = [ (0,0,0) ] * numLEDs
        color  = random.randint(33, 255)
        color2  = random.randint(33, 255)
        for i in range(loopcount):
                pixels = [(0, 0, 0)] * numLEDs

                for e in range(4):
                    pixels[y + e] = wheel(color)
                    if r == 0:
                        if (z - 40 > 0):
                            pixels[(z - 40) + e] = wheel(color)
                    if r == 1:
                        if ((z - 40) + 4 > 0):
                            pixels[((z - 40)+4) + e] = wheel(color)
                    if r == 2:
                        if((z + 4) < 799):
                            pixels[(z + 4) + e] = wheel(color)
                    if r == 3:
                        if ((z + 40)+4 < 799):
                            pixels[(z +40) + 4] = wheel(color)
                    if r == 4:
                        if (z + 40 < 799):
                            pixels[(z + 40)] = wheel(color)
                    if r == 5:
                        if((z + 40) - 4 > 0):
                            pixels[(z - 40) - 4] = wheel(color)
                    if r == 6:
                        if(z - 4 > 0):
                            pixels[z - 4] = wheel(color)
                    if r == 7:
                        if((z - 40) - 4 > 0):
                            pixels[(z - 40) - 4] = wheel(color)
                    pixels[z + e] = wheel(color2)
                    if (y - 1 > 0):
                        pixels[(y-1) + e] = wheel(color2)


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



def tank3(loopcount):
    print loopcount
    z = 0
    p = 0
    n = 0
    j  = 0
    b = 0
    direction1 = 1
    direction2 = 1
    color4 = random.randint(0,255)
    color3 = 0
    color = random.randint(33, 255)
    for i in range(loopcount):

        pixels = [(0, 0, 0)] * numLEDs
        for k in range(0, 16):
            for u in range(20):
                if k == p:
                    pixels[front[k][u]] = wheel(color3)

        for k in range(7):
            for u in range(45):
                if n == k:
                    pixels[sideLeft[k][u]] = wheel(color3)
        for k in range(7):
            for u in range(43):
                if n == k:
                    pixels[sideRight[k][u]] = wheel(color3)
        for k in range(45):
                if j == k:
                    pixels[sideLeft[2][k]] = wheel(color4)
        for k in range(43):
                if b == k:
                    pixels[sideRight[2][k]] = wheel(color4)

        for q in range(len(track1)):
            if q % 5 == 0:
                pixels[track1[q - z]] = wheel(color)
                pixels[track1[q - (z - 1)]] = wheel(color - 20)
        for q in range(len(track2)):
            if q % 5 == 0:
                pixels[track2[q - z]] = wheel(color)
                pixels[track2[q - (z - 1)]] = wheel(color - 20)

        client.put_pixels(pixels)
        time.sleep(.1)
        z += 1
        if z > 4:
            z = 0
        p += 1
        if p > 15:
            p = 0
        n += 1
        if n > 7:
            n = 0
        j += direction1
        if j > 44:
            direction1 = -1
        elif j == 0:
            direction1 = 1
        b += direction2
        if b > 43:
            direction2 = -1
        elif b == 0:
            direction2 = 1
def pewpew(loopcount):
    pew = [333,332,331,330,329,328,327,334,338,60,57,48,49,50,73,76,101,104,248,251,276,72,71,70,105,106,275,274,273,68,95,241,268,232,239,266,237,89,229,339,398,397,396,395,394,393,400,404,413,410,415,416,417,441,440,439,438,437,436,435,524,521,518,525,528,531,538,532,552,555,562,472,473,477,476,486,487,490,497,508]
    eyeoutline = [671,703,709,745,748,785,788,825,828,865,868,905,908,944,950,982,981,953,939,915,898,875,858,835,818,795,778,755,738,714,700,672,681,693,719,735,758,775,798,815,838,855,878,895,918,934,960,972,971,963,929,925,888,885,848,845,808,805,768,765,728,724,690,682]
    eyemovement = [[791,792,822,821,801,802,812,811],    #middle
                    [790,823,791,822,800,813,801,812],  #half left
                    [789,824,823,790,799,814,800,813],  #left
                    [792,793,821,820,802,811,803,810], #half right
                    [793,820,794,819,803,810,804,809]]  #right
    eyeball = [744,749,784,789,824,829,864,869,904,909,710,743,750,783,790,823,830,863,870,903,943,910,702,711,742,751,782,791,822,831,862,871,902,911,942,951,701,712,741,752,781,792,821,832,861,872,901,912,941,952,713,740,753,780,793,820,833,860,873,900,913,940,739,754,779,794,819,834,859,874,899,914,734,759,774,799,814,839,854,879,894,919,720,733,760,773,800,813,840,853,880,893,920,933,692,721,732,761,772,801,812,841,852,881,892,921,932,961,691,722,731,762,771,802,811,842,851,882,891,922,931,962,723,730,763,770,803,810,843,850,883,890,923,930,729,764,769,804,809,844,849,884,889,924]
    blink = [[341,341,702,701,341,341,341,341,691,692,341,341],
             [341,710,711,712,713,341,341,720,721,722,723,341],
             [744,743,742,741,740,739,734,733,732,731,730,729],
             [749,750,751,752,753,754,759,760,761,762,763,764],
             [784,783,782,781,780,779,774,773,772,771,770,769],
             [789,790,791,792,793,794,799,800,801,802,803,804],
             [824,823,822,821,820,819,814,813,812,811,810,809],
             [829,830,831,832,833,834,839,840,841,842,843,844],
             [864,863,862,861,860,859,854,853,852,851,850,849],
             [869,870,871,872,873,874,879,880,881,882,883,884],
             [904,903,902,901,900,899,894,893,892,891,890,889],
             [909,910,911,912,913,914,919,920,921,922,923,924],
             [341,943,942,941,940,933,932,931,930,341,341,341],
             [341,341,951,952,341,341,341,341,961,962,341,341]]
    colors = [random.randint(20,255),random.randint(0,255),random.randint(0,150),random.randint(150,255),random.randint(0,255),random.randint(0,255)]
    z = 0
    bullet1 = 43
    bullet2 = random.randint(0,43)
    bullet3 = 0
    bullet4 = random.randint(0,43)
    n = 0
    o = 4
    p = 0
    t = 4
    eyelid = 0
    direction = 1
    for stop in range(loopcount):

        for i in range(1000):
            pixels = [(0, 0, 0)] * numLEDs
            for a in range(45):
                if bullet4 == a:
                      pixels[sideLeft[n][a]] = wheel(colors[5])

            for a in range(45):

                if bullet1 == a:
                      pixels[sideLeft[o][a]] = wheel(colors[2])

            for a in range(43):
                if bullet2 == a:
                      pixels[sideRight[p][a]] = wheel(colors[2])

            for a in range(43):
                if bullet3 == a:
                      pixels[sideRight[t][a]] = wheel(colors[5])

            if i % 10 == 0:
                for a in range(len(pew)):
                    pixels[pew[a]] = [0, 0, 0]
            else:
                for a in range(len(pew)):
                    pixels[pew[a]] = wheel(colors[1])
            for i2 in range(len(eyeoutline)):
                 pixels[eyeoutline[i2]] = wheel(colors[1])

            for a in range(len(eyeball)):
                pixels[eyeball[a]] = wheel(colors[3])
            for i2 in range(8):
                pixels[eyemovement[0][i2]] = wheel(colors[4])



            if (((i > 200) and (i < 220)) or (((i > 400) and (i < 420)))):
                for a in range(len(eyeball)):
                    pixels[eyeball[a]] = wheel(colors[3])
                for i2 in range(8):
                    pixels[eyemovement[1][i2]] = wheel(colors[4])


            elif ((i > 218) and ( i < 400)):
                for a in range(len(eyeball)):
                    pixels[eyeball[a]] = wheel(colors[3])
                for i2 in range(8):
                     pixels[eyemovement[2][i2]] = wheel(colors[4])
            elif (((i > 600) and (i < 620)) or (((i > 800) and (i < 820)))):
                for a in range(len(eyeball)):
                    pixels[eyeball[a]] = wheel(colors[3])
                for i2 in range(8):
                     pixels[eyemovement[3][i2]] = wheel(colors[4])
            elif ((i > 618) and ( i < 800)):
                for a in range(len(eyeball)):
                    pixels[eyeball[a]] = wheel(colors[3])
                for i2 in range(8):
                     pixels[eyemovement[4][i2]] = wheel(colors[4])
            elif ((i > 100) and ( i < 125)):

                for i2 in range(12):
                    for i3 in range(eyelid):
                        pixels[blink[i3][i2]] = [0, 0, 0]


                eyelid += direction
                if eyelid > 11:
                    direction = -1
                if eyelid <= 0:
                    direction = 1

            elif ((i > 500) and ( i < 525)):

                for i2 in range(12):
                    for i3 in range(eyelid):
                        pixels[blink[i3][i2]] = [0, 0, 0]
                eyelid += direction

                if eyelid > 11:
                    direction = -1
                if eyelid <= 0:
                    direction = 1
            elif ((i > 900) and ( i < 925)):

                for i2 in range(12):
                    for i3 in range(eyelid):
                        pixels[blink[i3][i2]] = [0, 0, 0]
                eyelid += direction

                if eyelid > 11:
                    direction = -1
                if eyelid <= 0:
                    direction = 1




            for q in range(len(track1)):
                if q % 5 == 0:
                    pixels[track1[q - z]] = wheel(colors[0])
                    pixels[track1[q - (z - 1)]] = wheel(colors[0] - 20)
            for q in range(len(track2)):
                if q % 5 == 0:
                    pixels[track2[q - z]] = wheel(colors[0])
                    pixels[track2[q - (z - 1)]] = wheel(colors[0] - 20)
            client.put_pixels(pixels)
            time.sleep(.06)
            z += 1
            if z > 4:
                z = 0
            for i2 in range(len(colors)):
                colors[i2] += 1
                if colors[i2] > 255:
                    colors[i2] = 0
            bullet4 += -1
            if bullet4 == 0:
                bullet4 = 45
                n = random.randint(0,6)
            bullet1 += -1
            if bullet1 == 0:
                bullet1 = 45
                o = random.randint(0,6)
            bullet2 +=1
            if bullet2 == 43:
                bullet2 = 0
                p = random.randint(0,6)
            bullet3 +=1
            if bullet3 > 43:
                bullet3 = 0
                t = random.randint(0,6)



def tank4(loopcount):
    print loopcount
    z = 0
    p = 0
    n = 0
    j  = 0
    b = 0
    c = 0
    g = 0
    doonce = 0
    flare=[0,0,0,0,0,0,0]
    color3 = random.randint(0,255)
    direction1 = 1
    direction2 = 1
    color5 = random.randint(20, 255)
    color4 = random.randint(20,255)
    color3 = random.randint(0,255)
    color = random.randint(33, 255)
    for i in range(loopcount):

        pixels = [(0, 0, 0)] * numLEDs

        for k in range(25):
                pixels[FrontCircle[k]] = wheel(color)
        for k in range(25):
            if c == k:
                pixels[FrontCircle[c]] = wheel(color3)

        for k in range(3):
                if k == n:
                    for t in range(12):
                         pixels[trinket[k][t]] = wheel(color4)

        for k in range(7):
            for y in range(55):
                if flare[k] == y:
                    pixels[FrontRight[k][y]] = wheel(color5)
                    pixels[FrontRight[k][y-1]] = wheel(color5-5)
                    pixels[FrontRight[k][y-2]] = wheel(color5-5)
                    pixels[FrontRight[k][y-3]] = wheel(color5-10)
                    pixels[FrontRight[k][y-4]] = wheel(color5-10)
                    pixels[FrontRight[k][y-5]] = wheel(color5-15)
                    pixels[FrontRight[k][y-6]] = wheel(color5-15)
                    pixels[FrontRight[k][y-7]] = wheel(color5-20)
                    pixels[FrontRight[k][y-8]] = wheel(color5-20)
        for k in range(7):
            for y in range(55):
                if flare[k] == y:
                    pixels[FrontLeft[k][y]] = wheel(color5)
                    pixels[FrontLeft[k][y-1]] = wheel(color5-5)
                    pixels[FrontLeft[k][y-2]] = wheel(color5-5)
                    pixels[FrontLeft[k][y-3]] = wheel(color5-10)
                    pixels[FrontLeft[k][y-4]] = wheel(color5-10)
                    pixels[FrontLeft[k][y-5]] = wheel(color5-15)
                    pixels[FrontLeft[k][y-6]] = wheel(color5-15)
                    pixels[FrontLeft[k][y-7]] = wheel(color5-20)
                    pixels[FrontLeft[k][y-8]] = wheel(color5-20)


        for q in range(len(track1)):
            if q % 5 == 0:
                pixels[track1[q - z]] = wheel(color)
                pixels[track1[q - (z - 1)]] = wheel(color - 20)
        for q in range(len(track2)):
            if q % 5 == 0:
                pixels[track2[q - z]] = wheel(color)
                pixels[track2[q - (z - 1)]] = wheel(color - 20)

        client.put_pixels(pixels)
        time.sleep(.1)
        z += 1
        if z > 4:
            z = 0
        p += 1
        if p > 15:
            p = 0
        n += 1
        if n > 3:
            n = 0
        j += direction1
        if j > 44:
            direction1 = -1
        elif j == 0:
            direction1 = 1
        b += direction2
        if b > 43:
            direction2 = -1
        elif b == 0:
            direction2 = 1
        color4 += 1
        if color4 > 255:
            color4 = 20
        color5 += 1
        if color5 > 255:
            color5 = 20
        c +=1
        if c > 21:
            c = 0
        g +=1
        if g > 37:
            g = 0
        for x in range(7):
            flare[x] += 1
            if flare[x] > 55:
                flare[x] = 0
        if ((i > 800 ) and (doonce == 0)):
            flare = [0, 16, 32, 8, 24, 42, 0, 0, 16, 32, 8, 24, 42, 0]
            doonce = 1



        
def wheel(WheelPos):
        if WheelPos < 85:
		color =  ((WheelPos * 3), (255 - WheelPos * 3 ), 0)
		return color
        else:
                if WheelPos < 170:
                        WheelPos -= 85
                        color =  ((255-WheelPos * 3), 0, (WheelPos * 3))
			return color
                else:
                        WheelPos -= 170
			color = (0, (WheelPos *3), (255 - WheelPos * 3))
			return color


for i in range(0,10000):
			#BlockImages(5)
			Treeloop(1000)
			Narrrloop2(1000)
			Narrrloop(1000)
			blox0(1000)


