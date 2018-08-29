# https://stackoverflow.com/questions/25107806/estimate-formants-using-lpc-in-python# https://www.quora.com/How-do-I-create-a-real-time-plot-with-matplotlib-and-Tkinterimport tkinter as tkfrom random import randintimport numpy as npimport csv# these two imports are importantfrom matplotlib.backends.backend_tkagg import FigureCanvasTkAggfrom matplotlib.figure import Figureimport threadingfrom voystick import recording as rcfrom voystick import formant_predict as fpimport pyaudiocontinuePlotting = FalseCHUNK = 2**10RATE = 44100#p = pyaudio.PyAudio()stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,                 frames_per_buffer=CHUNK)# ear = rc.SWHear()window = 100def change_state():    global continuePlotting    if continuePlotting == True:        continuePlotting = False    else:        continuePlotting = Truedef data_initialize():    with open('f1.txt', mode='w') as data:        data_writer = csv.writer(data, delimiter=',')        data_writer.writerow(['F1', 'F2', 'F3', 'F4'])        for i in range(window):            data_writer.writerow([0, 0, 0, 0])def data_points():    # for i in range(10):    data = np.fromstring(stream.read(CHUNK,exception_on_overflow = False), dtype=np.int16)    if np.linalg.norm(data) > 10000:        formants = fp.get_formants(data)    else:        formants = 0    # peak = np.average(np.abs(data)) * 2    with open('f1.txt', mode='a') as f:        f        for i in range(window):            data_writer.writerow(formants)    l = []    tail = len(data)    for i in range(tail-window,tail):        l.append(float(data[i].rstrip("\n")))    return ldef app():    # initialise a window.    root = tk.Tk()    root.config(background='white')    root.geometry("500x500")    lab = tk.Label(root, text="Live Plotting", bg='white').pack()    fig = Figure(figsize=(5, 4))    ax = fig.add_subplot(111)    ax.set_xlabel("F1")    ax.set_ylabel("F2")    ax.grid()    graph = FigureCanvasTkAgg(fig, master=root)    graph.get_tk_widget().pack(side="top", fill='both', expand=True)    def plotter():        data_initialize()        while continuePlotting:            ax.cla()            # ax.set_ylim(-2**15,2**15)            ax.set_ylim(-100,10000)            ax.set_xlim(-100,10000)            dpts = data_points()            # ax.plot(range(len(dpts)), dpts,c=range(len(dpts)),cmap='Blues',linewidth=2)            # ax.semilogx(np.arange(0,44100),dpts[44100:],linewidth=2, markersize=12)            ax.plot(range(len(dpts)), dpts, linewidth=2, markersize=12)            graph.draw()            # time.sleep(.100)    def gui_handler():        change_state()        threading.Thread(target=plotter).start()    b = tk.Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")    b.pack(side="bottom")    root.mainloop()app()