import sys
import numpy
import wave
import math
from scipy.signal import lfilter
# from scipy.signal import hamming
from audiolazy import lpc
from itertools import islice

"""
Estimate formants using LPC.
"""


def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

file_path = "ae.wav"
# Read from file.
spf = wave.open(file_path, 'r') # http://www.linguistics.ucla.edu/people/hayes/103/Charts/VChart/ae.wav

# Get file as numpy array.
x = spf.readframes(-1)
x = numpy.fromstring(x, 'Int16')

Fs = spf.getframerate()
F0 = 162

window_len = 2 / F0 * Fs

# # Get Hamming window.
# N = len(x)
# w = numpy.hamming(N)
#
# # Apply window and high pass filter.
# x1 = x * w
# x1 = lfilter([1], [1., 0.63], x1)
#
# # Get LPC.
#
# ncoeff = int(2 + Fs / 1000)
# # A, e, k = lpc(x1, ncoeff)
# A, k = lpc(x1, order=8)
#
# list1 = [float(v) for k, v in A.items()]
#
# # Get roots.
# rts = numpy.roots(list1)
# rts = [r for r in rts if numpy.imag(r) >= 0]
#
# # Get angles.
# angz = numpy.arctan2(numpy.imag(rts), numpy.real(rts))
#
# # Get frequencies.
# frqs = sorted(angz * (Fs / (2 * math.pi)))
#
# frqs.extend([0,0,0])
#
# print(frqs)
