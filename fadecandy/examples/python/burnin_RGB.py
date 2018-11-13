#!/usr/bin/env python

# Burn-in test: Alternate RGB full brightness most of the time, but dim periodically
# so it's clear when there's a problem.

import opc, time, math

numLEDs = 800
client = opc.Client('localhost:7890')

t = 0
c = 1
b2 = 0
sem = 0

while True:
    t += 0.4
    brightness = int(min(1, 1.25 + math.sin(t)) * 255)
    if brightness < 69:
        c += 1
        c = ((c - 1) % 3) + 1
    if c == 1:
        frame = [ (brightness, 0, 0) ] * numLEDs
    elif c == 2:
        frame = [ (0, brightness, 0) ] * numLEDs
    elif c == 3:
        frame = [ (0, 0, brightness) ] * numLEDs
        
    
    client.put_pixels(frame)
    time.sleep(0.05) 

