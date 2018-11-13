import numpy as np
import time
#import opc
import socket, struct

class Client(object):
    def __init__(self, address, port):
        self.socket = socket.create_connection((address, port))

    def put_pixels(self, pixels, channel=0):
        pixels = np.clip(pixels, 0, 255).astype('ubyte')
        len_hi_byte = pixels.size // 256
        len_lo_byte = pixels.size % 256
        command = 0  # set pixel colors from openpixelcontrol.org

        header = struct.pack("BBBB", channel, command, len_hi_byte, len_lo_byte)
        message = header + pixels.tostring()
        self.socket.send(message)



client = Client('192.168.0.200', 7890)

pix = np.zeros((20, 10, 3), dtype='ubyte')

order = []
for row in range(19,-1,-1):
    for col in range(10):
        order.extend([[row,col]]*4)
order = np.array(order)

pix[0, 0] = [255,255,255]   

def show(pix):
    client.put_pixels(pix[order[:,0], order[:,1]])
       
def noise():
    while True:
        pix = np.random.randint(0, 255, size=(20, 10, 3))
        show(pix)
        time.sleep(0.03)

def fps():
    row = 0
    pix = np.zeros((20, 10, 3), dtype='ubyte')
    t = time.time()
    while True:
        pix[row] = [0, 0, 0]
        row = (row+1) % 20
        pix[row] = [255,255,255]
        show(pix)
        time.sleep(0.016)
        t2 = time.time()
        print(1.0 / (t2-t))
        t = t2

def image():
    import PIL.Image
    img = np.asarray(PIL.Image.open('face.jpg'))
    i = 0
    while True:
        scale = 1 + int(20*(np.sin(i*0.02)+1))
        #pix = img[::scale, ::scale][:20, :10, :3]
        pix = downsample(downsample(img, scale, 0), scale, 1)[:20, :10, :3]
        show(pix)
        i += 1
        time.sleep(0.016)


def downsample(data, n, axis=0, xvals='subsample'):
    """Downsample by averaging points together across axis.
    If multiple axes are specified, runs once per axis.
    If a metaArray is given, then the axis values can be either subsampled
    or downsampled to match.
    """
    if hasattr(axis, '__len__'):
        if not hasattr(n, '__len__'):
            n = [n]*len(axis)
        for i in range(len(axis)):
            data = downsample(data, n[i], axis[i])
        return data
    
    if n <= 1:
        return data
    nPts = int(data.shape[axis] / n)
    s = list(data.shape)
    s[axis] = nPts
    s.insert(axis+1, n)
    sl = [slice(None)] * data.ndim
    sl[axis] = slice(0, nPts*n)
    d1 = data[tuple(sl)]
    d1.shape = tuple(s)
    d2 = d1.mean(axis+1)

    return d2


def cam():
    import cv2
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        pix = img[::20, ::20][:,::-1][:20, :10, :3]
        show(pix)


def spec():
    import sounddevice
    import pyqtgraph as pg
    app = pg.mkQApp()
    plt = pg.plot()
    cmap = np.zeros((20, 3), dtype='ubyte')
    cmap[:,0] = np.clip(np.linspace(0, 1000, 20), 0, 255)
    cmap[:,1] = np.clip(np.linspace(-255, 500, 20), 0, 255)
    cmap[:,2] = np.clip(np.linspace(-500, 255, 20), 0, 255)
    while True:
        rec = sounddevice.rec(2048, samplerate=44100, channels=1, blocking=True)
        fft = np.abs(np.fft.rfft(rec[:,0]))
        ds = fft[2**np.arange(10)]
        log = 2 * (np.log(ds + 0.5) + 2)
        plt.plot(log, clear=True)
        app.processEvents()
        time.sleep(0.016)
        pix = np.zeros((20, 10, 3))
        for i in range(10):
            h = int(log[i])
            if h == 0:
                continue
            pix[-h:, i] = cmap[:h]
        show(pix)