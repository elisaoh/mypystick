
# references
# https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python
# https://www.quora.com/How-do-I-create-a-real-time-plot-with-matplotlib-and-Tkinter

import tkinter as tk
from random import randint
import numpy as np
import pyaudio


# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from debugTools import current
from debugTools import formant_predict as fp
import matplotlib.pyplot as plt

continuePlotting = False
# CHUNK = 2**14
CHUNK = 120 # window size
# RATE = 44100
RATE = 11025
state = current.currentState(fp=[400,2500,4000])

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK)

lightbox = 100 # most 100 recent formants predicted
frame = 1 # how many points predicted at one time
tape = np.zeros(3)

f1 = np.zeros(lightbox)
f2 = np.zeros(lightbox)
f3 = np.zeros(lightbox)



def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True

def data_initialize():
    with open('f1.txt', mode='w') as f:
        f.write(str(0)+'\n')
    with open('f2.txt', mode='w') as f:
        f.write(str(0) + '\n')
    with open('f3.txt', mode='w') as f:
        f.write(str(0) + '\n')

def vowel_detection(dpts):
    # this function is not used
    peak = np.average(np.abs(dpts))*2
    tape[:-1] = tape[1:]
    tape[-1:] = peak
    if ((tape >= 1000).sum() == tape.size).astype(np.int):
        return True
    else:
        return False

def data_points(dpts):
    # whether continuous change or not

    peak = np.average(np.abs(dpts)) * 2
    tape[:-1] = tape[1:]
    tape[-1:] = peak
    if ((np.abs(tape) >= 300).sum() == tape.size).astype(np.int):
        formants = fp.get_formants(dpts, RATE)  # formants pool with lpc
        formants = state.formants_smooth(formants, dpts[-1] ** 2)
    else:
        formants = np.zeros(3)


    with open('f1.txt', mode='a') as f:
        f.write(str(formants[0]) + '\n')

    with open('f2.txt', mode='a') as f:
        f.write(str(formants[1]) + '\n')

    with open('f3.txt', mode='a') as f:
        f.write(str(formants[2]) + '\n')

    f1[:-frame] = f1[frame:]
    f1[-frame:] = formants[0]

    f2[:-frame] = f2[frame:]
    f2[-frame:] = formants[1]

    f3[:-frame] = f3[frame:]
    f3[-frame:] = formants[2]

    return f1, f2, f3

def app():
    # initialise a window.
    root = tk.Tk()
    root.config(background='white')
    root.geometry("1000x1000")

    lab = tk.Label(root, text="Live Plotting", bg='white').pack()

    fig = Figure(figsize=(5, 4))

    # first thing you will see when you open the app
    ax1 = fig.add_subplot(311)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("F1")
    ax1.grid()

    ax2 = fig.add_subplot(312)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("F2")
    ax2.grid()

    ax3 = fig.add_subplot(313)
    ax3.set_xlabel("Time")
    ax3.set_ylabel("F3")
    ax3.grid()



    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)


    def plotter():
        while continuePlotting:  # start/stop



            dpts = np.fromstring(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            f1,f2,f3 = data_points(dpts)

            ax1.cla()
            ax2.cla()
            ax3.cla()
            ax1.scatter(range(lightbox), f1, c=range(lightbox), cmap='Blues', linewidth=1)
            ax2.scatter(range(lightbox), f2, c=range(lightbox), cmap='Blues', linewidth=1)
            ax3.scatter(range(lightbox), f3, c=range(lightbox), cmap='Blues', linewidth=1)

            graph.draw()



    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()


    b = tk.Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack(side="bottom")

    root.mainloop()

if __name__ == '__main__':
    data_initialize()
    app()
    stream.stop_stream()
    stream.close()
    p.terminate()
