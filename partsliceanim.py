from __main__ import *
import yt
import matplotlib
matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *

if partslice_fixlimits:
	sizingappend = ''
else:
	sizingappend = '_sizing'

num = 1000000 + startingset
numstr = str(num)
cut = numstr[1:7]

ts = yt.load(readpath + outprefix + cut, bounding_box = hbox, n_ref=nref )
plot = yt.SlicePlot(ts, partslice_direction, ('gas', partslice_parttype + '_nuclei_density'), width = partslice_plotwidth, fontsize=35 )

time, timelabel = getTime(ts, 0)

plot.annotate_timestamp(time_unit = timelabel)

if partslice_fixlimits:
	plot.set_zlim('all',partslice_lowlim,partslice_highlim)
	
fig = plot.plots[partslice_parttype + '_nuclei_density'].figure

def animate(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'partslice: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	
	plot._switch_ds(ds)
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
partslice_saveas = writepath + partslice_direction + '_' + partslice_parttype + '_slice_' + simname + sizingappend + '.mp4'
anim.save(partslice_saveas)
print 'partslice: Saved animation ' + partslice_saveas
