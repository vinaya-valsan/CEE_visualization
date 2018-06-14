from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation

tempprof_dotsize = 1
time = np.zeros(nframes)

if tempprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

# create figure
fig = pl.figure()

# define norm
def norm(a) :
	return np.sqrt(a[:,0]*a[:,0] + a[:,1]*a[:,1] + a[:,2]*a[:,2])

# create each frame
def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'tempprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()
	pos = ad[('Gas','Coordinates')]
	
	radius = norm(pos)
	temp = ad[('Gas','Temperature')]
	time[i] = dDelta * frameskip * (i+1.0)
	
	scat = pl.scatter(radius,temp,s= tempprof_dotsize)
	pl.xscale('log')
	pl.yscale('log')
	
	if tempprof_fixaxes:
		pl.axis(tempprof_axes)
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Temperature (K)')
	pl.title('Radial Temperature Profile ' + cut + ' Time: ' + str(time[i])[0:5] )
	return scat
	
# create animation object
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
tempprof_saveas = writepath + 'tempprof_' + simname + sizingappend + '.mp4'
anim.save(tempprof_saveas)
print 'tempprof: Saved animation ' + tempprof_saveas
