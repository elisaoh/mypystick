# VoyStick (ongoing)

VoyStick is a real-time formant tracking program based on python. The project is still ongoing.

# Features / Purposes
  - Real-time formant tracking (input audio, output formants)
  - Real-time ploting (plot formants)
  - Pronunciation checking (check if the subject hits the right formants/vowels)

# Current Status

  - Input audio, output formants (however, formants inaccurate)
  - Show plot (refining needed)


You may want to:
  - Tune parameters (window size, LPC order,bandwidth, weights,...)
  - Add calibration (fundemental frequency, initial formants, ...)
  - Change GUI (stop the curser when there is not a vowel,..)
  - Improve algorithm (voting, ...)

# Code Details
## Structures 
| Folders | Files | Comments |
| ------ | ------ | ------ |
| **debugTools** | | |
| |checkNoise | record a short duration and ouput a plot of signal |
|| current | a class used in formant prediction, core of the algorithm, **tune parameters** here|
||debugging | take in whether a sample voice file from UCLA lab or a record from the file *record*, output time vs formants plots for f1, f2, f3 and other related plots|
|| formant_predict | a formant predict algorithm (LPC) adapted from demo of MATLAB |
|| record | just a recorder, output test.wav|
|| *test.wav*| generated by *record* |
|**realtimePlotting**| | |
|| f1f2f3plotting | realtime time vs formants plotting, as 3 subplots of f1, f2, f3|
|| voystick | main program, plotting a dot instead of time vs formants|
|**volumnplotting**| | |
||recording  | create a tape, not used in main part |
|| volumnplot | my first demo of realtime audio plotting |
|**references** | | some might be useful code |


## Package Used
| Packages | Comments |
| ------ | ------ |
| tkinter | comes with python3, no need to install |
| numpy | standard package |
| matplotlib | used in plotting |
| scipy | signal processing |
| pyaudio | recording |
| audiolazy | an efficient audio processsing package, more for realtime usage (only used LPC in this case)|

More details in comments.


# References
## Algorithm
- MATLAB LPC demo: http://www.mathworks.com/help/signal/ug/formant-estimation-with-lpc-coefficients.html
- M. Marc, *The nature of planned acoustic trajectories*
 
## Programming
- https://www.quora.com/How-do-I-create-a-real-time-plot-with-matplotlib-and-Tkinter
- https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
- https://github.com/blab-lab/pitch-mouse-py

## Dataset
- UCLA Linguistics 103 https://linguistics.ucla.edu/people/hayes/103/Charts/VChart/#FormantMeasurements




  
