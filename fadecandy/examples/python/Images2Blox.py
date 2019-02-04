#!/usr/bin/python

import opc, time, random, PIL, numpy, os, os.path
from PIL import Image
from numpy import array
numLEDs = 800
client = opc.Client('localhost:7890')





w, h = 4,200 ;
bloxes = [[0 for x in range(w)] for y in range(h)]
tree = [0,10,20,30,40,60,70,80,110,120,130,150,160,170,21,61,81,111,151,22,62,72,112,122,152,162,23,63,83,113,153,24,64,94,114,124,134,154,164,174]
stone = [199,189,179,159,129,99,59,19,9,178,158,148,128,108,88,58,28,187,177,157,137,127,107,87,57,17,176,156,126,106,86,56,6,195,185,175,155,125,95,65,55,45,25,15]

narrr = [3,4,5,6,14,25,33,34,35,36,54,55,56,63,65,74,75,76,93,94,95,96,103,105,113,114,116,133,134,135,136,143,145,153,154,156,173,174,175,176,183,185,193,194,196]
altnarr = [0,1,10,11,20,21,30,31,40,41,50,51,60,61,70,71,80,81,90,91,100,101,110,111,120,121,130,131,140,141,150,151,160,161,170,171,180,181,190,191,199,198,189,188,179,178,169,168,159,158,149,148,139,138,129,128,119,118,109,108,99,98,89,88,79,78,69,68,59,58,49,48,39,38,29,28,19,18,9,8]
hearts = [782,791,822,741,752,781,792,821,832,861,713,740,753,780,793,820,833,860,873,900,674,699,714,739,754,779,794,819,834,859,874,899,914,675,698,715,738,755,778,795,818,835,858,875,898,915,938,716,737,756,777,796,817,836,857,876,897,916,937,956,757,776,797,816,837,856,877,896,917,936,957,976,758,775,798,815,838,855,878,895,918,935,958,975,719,734,759,774,799,814,839,854,879,894,919,934,959,680,693,720,6733,760,773,800,813,840,853,880,893,920,933,681,692,721,732,761,772,801,812,841,852,881,892,921,722,731,762,771,802,811,842,851,882,891,730,763,770,803,8810,843,850,769,804,809]
grid =	[[0,1,40,41,80,81,120,121,160,161,200,201,240,241,280,281,320,321,360,361,400,401,440,441,480,481,520,521,560,561,600,601,640,641,680,681,720,721,760,761],
		[3,2,43,42,83,82,123,122,163,162,203,202,243,242,283,282,323,322,363,362,403,402,443,442,483,482,523,522,563,562,603,602,643,642,683,682,723,722,763,762],
		[4,5,44,45,84,85,124,125,164,165,204,205,244,245,284,285,324,325,364,365,404,405,444,445,484,485,524,525,564,565,604,605,644,645,684,685,724,725,764,765],
		[7,6,47,46,87,86,127,126,167,166,207,206,247,246,287,286,327,326,367,366,407,406,447,446,487,486,527,526,567,566,607,606,647,646,687,686,727,726,767,766],
		[8,9,48,49,88,89,128,129,168,169,208,209,248,249,288,289,328,329,368,369,408,409,448,449,488,489,528,529,568,569,608,609,648,649,688,689,728,729,768,769],
		[11,10,51,50,91,90,131,130,171,170,211,210,251,250,291,290,331,330,371,370,411,410,451,450,491,490,531,530,571,570,611,610,651,650,691,690,731,730,771,770],
		[12,13,52,53,92,93,132,133,172,173,212,213,252,253,292,293,332,333,372,373,412,413,452,453,492,493,532,533,572,573,612,613,652,653,692,693,732,733,772,773],
		[15,14,55,54,95,94,135,134,175,174,215,214,255,254,295,294,335,334,375,374,415,414,455,454,495,494,535,534,575,574,615,614,655,654,695,694,735,734,775,774],
		[16,17,56,57,96,97,136,137,176,177,216,217,256,257,296,297,336,337,376,377,416,417,456,457,496,497,536,537,576,577,616,617,656,657,696,697,736,737,776,777],
		[19,18,59,58,99,98,139,138,179,178,219,218,259,258,299,298,339,338,379,378,419,418,459,458,499,498,539,538,579,578,619,618,659,658,699,698,739,738,779,778],
		[20,21,60,61,100,101,140,139,180,181,220,221,260,261,300,301,340,341,380,381,420,421,460,461,500,501,540,541,580,581,620,621,660,661,700,701,740,741,780,781],
		[23,22,63,62,103,102,143,144,183,182,223,222,263,262,303,302,343,342,383,382,423,422,463,462,503,502,543,542,583,582,623,622,663,662,703,702,743,742,783,782],
		[24,25,64,65,104,105,144,145,184,185,224,225,264,265,304,305,344,345,384,385,424,425,464,465,504,505,544,545,584,585,624,625,664,665,704,705,744,745,784,785],
		[27,26,67,66,107,106,147,146,187,186,227,226,267,266,307,306,347,346,387,386,427,426,467,466,507,506,547,546,587,586,627,626,667,666,707,706,747,746,787,786],
		[28,29,68,69,108,109,148,149,188,189,228,229,268,269,308,309,348,349,388,389,428,429,468,469,508,509,548,549,588,589,628,629,668,669,708,709,748,749,788,789],
		[31,30,71,70,111,110,151,150,191,190,231,230,271,270,311,310,351,350,391,390,431,430,471,470,511,510,551,550,591,590,631,630,671,670,711,710,751,750,791,790],
		[32,33,72,73,112,113,152,153,192,193,232,233,272,273,312,313,352,353,392,393,432,433,472,473,512,513,552,553,592,593,632,633,672,673,712,713,752,753,792,793],
		[35,34,75,74,115,114,155,156,195,194,235,234,275,274,315,314,355,354,395,394,435,434,475,474,515,514,555,554,595,594,635,634,675,674,715,714,755,754,795,794],
		[36,37,76,77,116,117,156,157,196,197,236,237,276,277,316,317,356,357,396,397,436,437,476,477,516,517,556,557,596,597,636,637,676,677,716,717,756,757,796,797],
		[39,38,79,78,119,118,159,158,199,198,239,238,279,278,319,318,359,358,399,398,439,438,479,478,519,518,559,558,599,598,639,638,679,678,719,718,759,758,799,798]]

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
			img = img.resize((40, 20), PIL.Image.ANTIALIAS)
			arr = array(img)
			rgb_arry = arr.convert('RGB')
			print('arr')
			print(arr)
			print()
			print('grid')
			print(grid)
			print()

			print()
			pixels = [ (0,0,0) ] * numLEDs
			for t in range(20):
				for u in range(40):
					pixels[grid[t][u]] = arr[t][u]
			
			print(pixels)

			print('###########################')
			client.put_pixels(pixels)
			time.sleep(.5)
def BlockImages2(loopcount):

	for q in range(loopcount):
		MorphImages = []
		NumFiles = len([name for name in os.listdir('./tree') if os.path.isfile(name)])
		print(NumFiles)
		for i in range(71):
			MorphImages.append("./tree/Trees"+str(i)+".jpg")
		print(MorphImages)
		for picture in range(len(MorphImages)):
			img = Image.open(MorphImages[picture])
			#img = img.resize((40, 20), PIL.Image.ANTIALIAS)
			arr = array(img)
			print('arr')
			print(arr)
			print()
			print('grid')
			print(grid)
			print()

			print()
			pixels = [ (0,0,0) ] * numLEDs
			for t in range(20):
				for u in range(40):
					pixels[grid[t][u]] = arr[t][u]
			
			print(pixels)

			print('###########################')
			client.put_pixels(pixels)
			time.sleep(.5)

def BlockImages3(loopcount):

	for q in range(loopcount):
		MorphImages = []
		NumFiles = len([name for name in os.listdir('./monday') if os.path.isfile(name)])
		print(NumFiles)
		for i in range(220):
				if i < 100:
					MorphImages.append("./monday/monday0"+str(i)+".png")
				else:
					MorphImages.append("./monday/monday"+str(i)+".png")
		print(MorphImages)
		for picture in range(len(MorphImages)):
			img = Image.open(MorphImages[picture])
			img = img.convert('RGB')
			img = img.resize((40, 20), PIL.Image.ANTIALIAS)
			arr = array(img)
			
			print('arr')
			print(arr)
			print()
			print('grid')
			print(grid)
			print()

			print()
			pixels = [ (0,0,0) ] * numLEDs
			for t in range(20):
				for u in range(40):
					pixels[grid[t][u]] = arr[t][u]
			
			print(pixels)

			print('###########################')
			client.put_pixels(pixels)
			time.sleep(.2)
def BlockImages4(loopcount):

	for q in range(loopcount):
		MorphImages = []
		NumFiles = len([name for name in os.listdir('./monday2') if os.path.isfile(name)])
		print(NumFiles)
		for i in range(38):
				if i < 10:
					MorphImages.append("./monday2/monday20"+str(i)+".png")
				else:
					MorphImages.append("./monday2/monday2"+str(i)+".png")
		print(MorphImages)
		for picture in range(len(MorphImages)):
			img = Image.open(MorphImages[picture])
			img = img.convert('RGB')
			img = img.resize((40, 20), PIL.Image.ANTIALIAS)
			arr = array(img)
			
			print('arr')
			print(arr)
			print()
			print('grid')
			print(grid)
			print()

			print()
			pixels = [ (0,0,0) ] * numLEDs
			for t in range(20):
				for u in range(40):
					pixels[grid[t][u]] = arr[t][u]
			
			print(pixels)

			print('###########################')
			client.put_pixels(pixels)
			time.sleep(.2)
			
			
			

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







        
def wheel(WheelPos):
	if WheelPos < 85:
		color =  ((WheelPos * 3), (255 - WheelPos * 3 ), 0)
	else:
		if WheelPos < 170:
				WheelPos -= 85
				color =  ((255-WheelPos * 3), 0, (WheelPos * 3))
				return color
		else:
			WheelPos -= 170
			color = (0, (WheelPos *3), (255 - WheelPos * 3))
			return color

def run_pattern():
	for i in range(0,10000):
				BlockImages4(3)
				BlockImages3(5)
				#BlockImages(5)
				#Treeloop(1000)
				#Narrrloop2(1000)
				#Narrrloop(1000)
				#blox0(1000)


