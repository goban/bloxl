try:
    from .jeff import *
except Exception: #ImportError
    from jeff import *

try:
    from .Images2Blox import *
except Exception: #ImportError
    from Images2Blox import *

while True:

    b = blank_bloxl()

    for i in range(10):
        test_func()

    b = blank_bloxl()

    BlockImages4(3)
    BlockImages3(5)
