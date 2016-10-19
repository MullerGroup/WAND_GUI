import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

ecg = np.fromfile('ecg.bin', dtype=np.int32)
fs = 1000
ts = 1/fs
nyq = fs/2
bp_stop_Hz = np.array([54, 61])
b, a = signal.butter(4,bp_stop_Hz/(fs/2.0),'bandstop')
ecg1 = signal.lfilter(b,a,ecg)
# bp_stop_Hz = np.array([119, 121])
# b, a = signal.butter(2,bp_stop_Hz/(fs/2.0),'bandstop')
# ecg2 = signal.filtfilt(b,a,ecg1)
# bp_stop_Hz = np.array([179, 181])
# b, a = signal.butter(2,bp_stop_Hz/(fs/2.0),'bandstop')
# ecg3 = signal.filtfilt(b,a,ecg2)
b, a = signal.butter(5,40/(fs/2.0),'lowpass')
ecg4 = signal.lfilter(b,a,ecg1)
b, a = signal.butter(2,0.5/(fs/2.0),'highpass')
filt_ecg = signal.lfilter(b,a,ecg4)

# bp_stop_Hz = np.array([24, 26])
# b, a = signal.butter(2,bp_stop_Hz/(fs/2.0),'bandstop')
# filt_ecg = signal.filtfilt(b,a,ecg5)

n = ecg.size
t = np.arange(0, ts*(n), ts)
k = np.arange(n)
T = n/fs
frq = k/T
frq = frq[range(int(n/2))]

ecgY = np.fft.fft(ecg)/n
ecgY = ecgY[range(int(n/2))]
ecgY = 10*np.log10(ecgY**2)
filtY = np.fft.fft(filt_ecg)/n
filtY = filtY[range(int(n/2))]
filtY = 10*np.log10(filtY**2)

plt.figure(1)
plt.subplot(221)
plt.plot(t,ecg)
plt.subplot(222)
plt.plot(t,filt_ecg)
plt.subplot(223)
plt.plot(frq,ecgY)
# ax = plt.gca()
# ax.set_ylim([-5,5])
plt.subplot(224)
plt.plot(frq,filtY)
plt.show()