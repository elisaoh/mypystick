import pyaudio
import numpy as np

CHUNK = 2**11
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK)
f = open("data.txt", "a")
for i in range(10):
    dpts = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    f.write(str(dpts) + '\n')
f.close()
stream.stop_stream()
stream.close()
p.terminate()