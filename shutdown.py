#!/usr/bin/env python3
from gpiozero import Button
import os
proccess=526
process = str(proccess)
Button(21).wait_for_press()
os.system("kill -9 "+process)
os.system('python /home/pi/src/bloxl/off.py')
os.system("sudo poweroff")

