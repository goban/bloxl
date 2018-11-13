#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs = 800
client = opc.Client('localhost:7890')
pixels = [ (0,0,0) ] * numLEDs
sem = 0

while True:
        pixels2 = [ (0,0,0) ] * numLEDs
        for i in range(numLEDs):
                if sem == i % 4:
                        pixels2[i] = (((i+1)%2 * 140)%255, (i % 2 * 140)%255, (i % 3 * 210)%255)

        client.put_pixels(pixels2)
        sem += 1
        sem %= 4
        time.sleep(0.3)
	

