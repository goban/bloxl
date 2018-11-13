#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time, random

numLEDs = 800
client = opc.Client('localhost:7890')
pixels = [ (0,0,0) ] * numLEDs

remap = [761, 764, 765, 768, 769, 
#remap = [0] * 801
#remap2 = [0] * 801
#for i in range(1, 801):
#	j = i / 40
#	if i % 4 == 1:
#		remap[i] = ((i / 4) * 2) + 1 + (j * 20)
#	elif i % 4 == 0:
#		remap[i] = ((i % 40) / 2) + (j * 40)
#	elif i % 4 == 2:
#		remap[i] = ((i / 4) * 2) + 21 + (j * 20)
#	elif i % 4 == 3:
#		remap[i] = (((i / 4) + 1) * 2) + ((j + 1) * 20)
#	print "remap[", i, "] = ", remap[i]
#	print "remap2[", remap[i], "] = ", remap2[remap[i]]
#	print ""

#	remap2[remap[i]] = i
#for i in range(0, 800):
#	pixels = [ (0,0,0) ] * 800
#	pixels[remap2[i]] = (255,255,255)
#	client.put_pixels(pixels)
#	time.sleep(0.5)


#while True:
#        start = random.randrange(0,20)
#        start = ((start - 1) * 4) + (((start + 1) % 2) * 3)
#        remap[start + 760] = (0,0,0)

        
##	for i in range(numLEDs):
##		pixels = [ (0,0,0) ] * numLEDs
##		pixels[i] = (255, 255, 255)
##		client.put_pixels(pixels)
##		time.sleep(0.02)
##	
        

