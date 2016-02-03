import vxi11
import time
from bitarray import bitarray
import struct
import serial
import os
import numpy as np



dirPrefix = "c:/chipdata/fib5/600mV_bode/"
filePrefix = "freq"

print("Script launched")
s = None
s = serial.Serial('COM3') #function generator

# change for next sweeps later
filedir = dirPrefix
savename = filedir + filePrefix
try:
    os.mkdir(filedir)
except:
    pass

#number of frequency points
N = 50
freq_vals = np.round(np.logspace(1,4,N))


for freq in freq_vals:
        print("Enable FG output at {:0.3f}".format(freq))
        s.write(b"AMPL 0.050VP\n")
        time.sleep(0.1)
        s.write("FREQ {:0.3f}\n".format(freq).encode())
        time.sleep(0.5)
        ctrl.getAdc(1000)
        ctrl.saveMat("{}_{:05.0f}Hz.mat".format(savename, freq))
        print("Completed {:0.3f} Hz".format(freq))


s.close()
print("Done")