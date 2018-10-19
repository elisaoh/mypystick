import sys
import numpy
import wave
import math
from scipy.signal import lfilter
# from scipy.signal import hamming
from audiolazy import lpc

"""
Estimate formants using LPC.
"""


def get_formants(x,Fs):

    formants = numpy.zeros(3)

    # Get Hamming window.
    N = len(x)
    w = numpy.hamming(N)

    # Apply window and high pass filter.
    x1 = x * w
    x1 = lfilter([1], [1., 0.63], x1)

    # Get LPC.
    # Fs = spf.getframerate()
    # Fs = 11025
    # ncoeff = int(2 + Fs / 1000)
    # A, e, k = lpc(x1, ncoeff)
    A, k = lpc(x1, order=12)

    list1 = [float(v) for k, v in A.items()]

    # Get roots.
    rts = numpy.roots(list1)
    rts = [r for r in rts if numpy.imag(r) >= 0]

    # Get angles.
    angz = numpy.arctan2(numpy.imag(rts), numpy.real(rts))

    # Get frequencies.
    frqs = sorted(angz * (Fs / (2 * math.pi)))
    frqs = [f for f in frqs if f > 100]

    # frqs.extend([0, 0, 0])

    # formant range
    range_min = [100,500,1000]
    range_max = [1500,3500,4500]



    return frqs

