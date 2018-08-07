# https://www.quora.com/How-do-I-create-a-real-time-plot-with-matplotlib-and-Tkinter
import tkinter as tk
from random import randint

# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading

continuePlotting = False


def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True


def data_points():
    f = open("data.txt", "w")
    for i in range(10):
        f.write(str(randint(0, 10)) + '\n')
    f.close()

    f = open("data.txt", "r")
    data = f.readlines()
    f.close()

    l = []
    for i in range(len(data)):
        l.append(int(data[i].rstrip("\n")))
    return l


def app():
    # initialise a window.
    root = tk.Tk()
    root.config(background='white')
    root.geometry("500x350")

    lab = tk.Label(root, text="Live Plotting", bg='white').pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            dpts = data_points()
            ax.plot(range(10), dpts, marker='o', color='orange')
            graph.draw()
            time.sleep(1)

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

    b = tk.Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack(side="top")

    root.mainloop()


app()
