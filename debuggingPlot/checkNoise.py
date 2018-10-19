import pyaudio
import matplotlib.pyplot as plt
import numpy as np

CHUNK = 2**14
# CHUNK = 120
# RATE = 44100
RATE = 11025

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK)

for i in range(3):
    dpts = np.fromstring(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    plt.figure()
    plt.subplot(111)
    plt.plot(range(CHUNK), dpts)
    plt.show()
