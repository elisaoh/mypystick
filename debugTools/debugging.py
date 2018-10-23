import sys
import numpy as np
import wave
import pyaudio
import math
from scipy.signal import lfilter,butter
# from scipy.signal import hamming
from audiolazy import lpc
from itertools import islice
from debugTools import formant_predict as fp
import matplotlib
import matplotlib.pyplot as plt
from debugTools import current
import scipy


# recording


"""
Estimate formants using LPC.
"""


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield list(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield list(result)
#
sig = "UCLA"
folder_path = "/Users/elisa/Documents/2018Summer/VoiStick/mypystick/VChart/"
vowel_path = "a_Front"
file_path = folder_path+vowel_path+".wav"

# testing
sig = "my_a"
file_path = "test.wav"

# Read from file.
spf = wave.open(file_path, 'r') # http://www.linguistics.ucla.edu/people/hayes/103/Charts/VChart/ae.wav
#
# Get file as numpy array.
x = spf.readframes(-1)
x = np.fromstring(x, 'Int16')

x = x[1000:10000]

# normalized
# base = min(x)
# range = max(x) - base
# normalized = [(xi-base)/range for xi in x]

x = np.array([int(xi*0.8) for xi in x])

Fs = spf.getframerate()
F0 = 162
window_len = int(2 / F0 * Fs)
#window_len = 500

w = window(x,window_len)
f1 = []
f2 = []
f3 = []
state = current.currentState(fp=[700,2500,4000])
# formants = [100,500,1000,0,0,0]
# rms = 200**2
# fs = state.formant_smooth(formants,rms)
# print(fs)


for win in w:
    if np.linalg.norm(win) > 2*10**4:
        formants = fp.get_formants(win,Fs) # formants pool with lpc
        rms = win[-1] ** 2
        fn = state.formants_smooth(formants,rms)
    else:
        fn = np.zeros(3)
    f1.append(fn[0])
    f2.append(fn[1])
    f3.append(fn[2])

win_num = len(f1)
win_array = np.arange(win_num)
#
plt.figure(1)
plt.subplot(411)
plt.plot(win_array, f1)
plt.ylabel("F1")


plt.subplot(412)
plt.plot(win_array, f2)
plt.ylabel("F2")

plt.subplot(413)
plt.plot(win_array, f3)
plt.ylabel("F3")

plt.subplot(414)
plt.plot(np.arange(x.size), x)
plt.ylabel("Signal")
plt.title(sig+' audio')
plt.show()
plt.savefig(sig+"_fmt.jpg")

N = len(x)
w = np.hamming(N)

# Apply window and high pass filter.
x1 = x * w
x1 = lfilter([1], [1., 0.63], x)
# order = 10
# cutoff = 250
# normal_cutoff = cutoff/Fs *2
# b,a = butter(order, normal_cutoff, btype='high')
# x1 = lfilter(b,a,x1)

f, t, Sxx = scipy.signal.spectrogram(x1,Fs,nfft=128,nperseg=100, noverlap=90,scaling='spectrum')
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
plt.figure(2)

f, Pxx_den = scipy.signal.periodogram(x, Fs)
f2, Pxx_den2 = scipy.signal.periodogram(x1, Fs)
plt.semilogy(f, Pxx_den)
plt.semilogy(f2, Pxx_den2)
plt.ylim([1e-7, 1e6])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.title(sig+' audio')
plt.show()
plt.savefig(sig+"_prdg.jpg")


# t = np.arange(len(x))
#
# fig, (ax1, ax2) = plt.subplots(111)
# ax1.plot(t, x)
# NFFT = 128
# Pxx, freqs, bins, im = ax2.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900)
# # The `specgram` method returns 4 objects. They are:
# # - Pxx: the periodogram
# # - freqs: the frequency vector
# # - bins: the centers of the time bins
# # - im: the matplotlib.image.AxesImage instance representing the data in the plot
plt.show()

# plt.show()


