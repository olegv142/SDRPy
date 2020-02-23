from matplotlib.mlab import psd
import pylab as pyl
import numpy as np
from rtlsdr import RtlSdr

sdr = RtlSdr()

# configure device
sdr.sample_rate = 3.2e6
sdr.center_freq = 433e6

NFFT = 1024
NUM_ROWS = 1024
SKIP_ROWS = 8 # let AGC to settle
MIN_ROWS = 64
ZOOM_STEP = .9
SCROLL_STEP = .1
FREQ_ZOOM = 4
SAMPLES_PER_ROW = NFFT / FREQ_ZOOM


image_buffer = -100*np.ones((NUM_ROWS, SAMPLES_PER_ROW))
fig = pyl.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Current frequency (MHz)')
ax.set_ylabel('Time (sec)')
top_row = 0
num_row = NUM_ROWS

def read_buffer():
	samples = sdr.read_samples((SKIP_ROWS+NUM_ROWS)*NFFT)
	margin = (NFFT - SAMPLES_PER_ROW) / 2
	for row in range(NUM_ROWS):
		psd_scan, f = psd(samples[(SKIP_ROWS+row)*NFFT:(SKIP_ROWS+row+1)*NFFT], NFFT=NFFT)
		image_buffer[row] = 10*np.log10(psd_scan[margin:margin+SAMPLES_PER_ROW])

def show_buffer():
	image = ax.imshow(image_buffer[top_row:top_row+num_row], aspect='auto', interpolation='nearest', vmin=-50, vmax=10)
	time_scale = NFFT / sdr.rs
	image.set_extent((
			(sdr.fc - sdr.rs/(2*FREQ_ZOOM))/1e6,
			(sdr.fc + sdr.rs/(2*FREQ_ZOOM))/1e6,
			time_scale * (top_row + num_row),
			time_scale * top_row
		))
	fig.canvas.draw()

def show_data():
	global top_row, num_row
	top_row, num_row = 0, NUM_ROWS
	read_buffer()
	show_buffer()

def zoom_data(zoom_in):
	global top_row, num_row
	center = top_row + num_row / 2
	if zoom_in:
		num_row = int(num_row * ZOOM_STEP)
	else:
		num_row = int(num_row / ZOOM_STEP)
	num_row = min(num_row, NUM_ROWS)
	num_row = max(num_row, MIN_ROWS)
	top_row = center - num_row / 2
	if top_row < 0:
		top_row = 0
	elif top_row + num_row > NUM_ROWS:
		top_row = NUM_ROWS - num_row
	show_buffer()

def scroll_data(up):
	global top_row, num_row
	if up:
		top_row -= int(num_row * SCROLL_STEP)
	else:
		top_row += int(num_row * SCROLL_STEP)
	if top_row < 0:
		top_row = 0
	elif top_row + num_row > NUM_ROWS:
		top_row = NUM_ROWS - num_row
	show_buffer()	

def on_key_press(event):
        if event.key == ' ':
		show_data()
	elif event.key == '+':
		zoom_data(True)
	elif event.key == '-':
		zoom_data(False)
	elif event.key == 'up':
		scroll_data(True)
	elif event.key == 'down':
		scroll_data(False)

show_data()
fig.canvas.mpl_connect('key_press_event', on_key_press)
pyl.show()

