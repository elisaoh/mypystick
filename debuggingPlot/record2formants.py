import sys
import numpy as np
import wave
import math
from scipy.signal import lfilter
# from scipy.signal import hamming
from audiolazy import lpc
from itertools import islice
from debuggingPlot import formant_predict as fp
import matplotlib
import matplotlib.pyplot as plt
from debuggingPlot import current

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

file_path = "a_Front.wav"
# Read from file.
spf = wave.open(file_path, 'r') # http://www.linguistics.ucla.edu/people/hayes/103/Charts/VChart/ae.wav

# Get file as numpy array.
x = spf.readframes(-1)
x = np.fromstring(x, 'Int16')

Fs = spf.getframerate()
F0 = 162

window_len = int(2 / F0 * Fs)
window_len = 500

w = window(x,window_len)
f1 = []
f2 = []
f3 = []
state = current.currentState()
# formants = [100,500,1000,0,0,0]
# rms = 200**2
# fs = state.formant_smooth(formants,rms)
# print(fs)


for win in w:
    if np.linalg.norm(win) > 2*10**4:
        formants = fp.get_formants(win,Fs) # formants pool with lpc
        fn = state.formants_smooth(formants,win[-1]**2)
        # fn = state.formants_pick(formants)
    else:
        fn = np.zeros(3)
    f1.append(fn[0])
    f2.append(fn[1])
    f3.append(fn[2])

win_num = len(f1)

plt.figure(1)
plt.subplot(411)
plt.plot(range(win_num), f1)

plt.subplot(412)
plt.plot(range(win_num), f2)

plt.subplot(413)
plt.plot(range(win_num), f3)

plt.subplot(414)
plt.plot(range(x.size), x)

plt.show()