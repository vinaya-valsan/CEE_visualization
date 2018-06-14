from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation

radprof_dotsize = 1
time = np.zeros(nframes)

if radprof_fixaxes:
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
	print 'radprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()
	pos = ad[('Gas','Coordinates')]
	
	radius = norm(pos)
# 	density = ad[('Gas','density')]
	density = ad[('Gas','Density')]
	time[i] = dDelta * frameskip * (i+1.0)
	
	scat = pl.scatter(radius,density,s= radprof_dotsize)
	pl.xscale('log')
	pl.yscale('log')
	
	if radprof_fixaxes:
		pl.axis(radprof_axes)
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Density (g/cm^3)')
	pl.title('Radial Density Profile ' + cut + ' Time: ' + str(time[i])[0:5] )
	return scat
	pl.clf()
	
# create animation object
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
radprof_saveas = writepath + 'radprof_' + simname + sizingappend + '.mp4'
anim.save(radprof_saveas)
print 'radprof: Saved animation ' + radprof_saveas
