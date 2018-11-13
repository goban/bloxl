#!/usr/bin/env python

# Burn-in test: Keep LEDs at full brightness most of the time, but dim periodically
# so it's clear when there's a problem.

import opc, time, math

numLEDs = 800
client = opc.Client('localhost:7890')



while True:
	frame =  [ (0,0,0) ] * 800
	frame[772] = (255,255,255)
	client.put_pixels(frame)
	frame[772] = (0,0,0)
	client.put_pixels(frame) 
	time.sleep(0.01)
