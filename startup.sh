#!/bin/bash
cd /home/pi/src/bloxl
source venv3/bin/activate
python turnon.py > /dev/null &
sed -i "s/proccess=.*/proccess="$!"/g" shutdown.py
