import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .jeff import *
from .Images2Blox import *

while True:

    b = blank_bloxl()

    for i in range(10):
        test_func()

    b = blank_bloxl()

    BlockImages4(3)
    BlockImages3(5)
