#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs = 800
client = opc.Client('localhost:7890')

while True:
        z  = 0
	for n in range(200):
		pixels = [ (0,0,0) ] * numLEDs
       	        pixels[z] = (255, 255, 255)
		pixels[z-1] = (255, 255, 255)
		pixels[z-2] = (255, 255, 255)
		pixels[z-3] = (255, 255, 255)
		pixels[z-4] = (255, 255, 255)
		client.put_pixels(pixels)
		time.sleep(.1)
		z = z + 4
		if z > 800:
                   z = 0
