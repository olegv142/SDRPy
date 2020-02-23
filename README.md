# SDRPy
## Python scripts for RTL-SDR

Using standard SDR software you sometimes can't utilize full potential of the receiver.
If you need to observe relatively fast changing signal its just impossible to do with waterfall
since the computer needs some time to process the next data portion.

The waterfal_shot.py reads the bunch of data once and then process it and display result.
You can read next frame of data by pressing space. Pressing + and - keys zoom in and out
the time scale. Once zoomed in you can slide the displayed time range by pressing up and down keys.
Other parameters like central frequency, FFT points, frequency scale zoom can be changed in the script.

The script is using https://github.com/roger-/pyrtlsdr - great library.

## Author

Oleg Volkov (olegv142@gmail.com)
