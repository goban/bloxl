
#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time, sys


numLEDs = 800
client = opc.Client('localhost:7890')
pixels = [ [0,0,0] ] * numLEDs
sem = 0
wpix = [0,0,0]
cursor = [0,0]
draw = True


remap = [[((2 * x) + 1 + ((x + (1 - ((39 - y) % 2))) % 2) + 40 * ((39 - y) // 2)) - 1 for y in range(40)] for x in range(20)]

def remapcursor():
	return remap[cursor[0]][cursor[1]]

def block():
	x = cursor[0] - (cursor[0] % 2)
	y = cursor[1] - (cursor[1] % 2)

	l = [remap[x][y] + n for n in range(4)]
	return l

def writepix(w):
	client.put_pixels(w)

def anchorpix():
	l = block()

	for i in range(4):
		pixels[l[i]] = list(wpix)
	client.put_pixels(pixels)

#	wpix[0] = 0
#	wpix[1] = 0
#	wpix[2] = 0


def fColor(n):
	l = block()

	wpix[n] += 64
	wpix[n] %= 320

	p2 = [list(p) for p in pixels]
	print list(wpix)
	for i in range(4):
		p2[l[i]] = list(wpix)
		print p2[l[i]]
	anchorpix()
	writepix(p2)

def fCursor(i, j):
	global wpix

	cursor[0] += i
	cursor[1] += j

	cursor[0] = max(min(cursor[0], 18), 0)
	cursor[1] = max(min(cursor[1], 38), 0)

	if draw:
		l = block()
		p2 = [list(p) for p in pixels]
		for i in range(4):
			p2[l[i]] = list(wpix)
		anchorpix()
		writepix(pixels)
	else:
		wpix = list( pixels[block()[0]] )

while True:
#        time.sleep(0.3)

	input = raw_input("enter command r, g, b, w, s, a, d, anchor, del:")
	if input == 'r':
		fColor(0)
	elif input == 'g':
		fColor(1)
	elif input == 'b':
		fColor(2)
	elif input == 'w':
		fCursor(0, -2)
	elif input == 's':
		fCursor(0, 2)
	elif input == 'a':
		fCursor(-2, 0)
	elif input == 'd':
		fCursor(2, 0)
	elif input == ('z' or 'anchor' or ''):
		anchorpix()
	elif input == 'q':
		draw = True
	elif input == 'e':
		draw = False
	elif input == 'del':
		wpix = [0,0,0]
		anchorpix()
	elif input == 'wpix':
		print wpix
	elif input == 'pixels':
		print [[pixels[remap[x][y]] for y in range(40)] for x in range(20)]
	else:
		print 'bad command or pile shame'

	input = ''
