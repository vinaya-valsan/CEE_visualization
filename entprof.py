from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

def norm(a,b,c) :
	return np.sqrt( np.multiply(a,a) + np.multiply(b,b) + np.multiply(c,c) )

entprof_dotsize = 1
time = np.zeros(nframes)

if entprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

fig = pl.figure()

def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'entprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()
	x = ad[('gas','x')]
	y = ad[('gas','y')]
	z = ad[('gas','z')]
	
	radius = norm(x,y,z)
	ent = ad[('gas','entropy')]
	time[i], timelabel = getTime(ds, i)
	
	scat = pl.scatter(radius,ent,s= entprof_dotsize)
	pl.xscale('log')
	pl.yscale('log')
	
	if entprof_fixaxes:
		pl.axis(entprof_axes)
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Entropy ()')
	pl.title('Radial Entropy Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )
	return scat
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
entprof_saveas = writepath + 'entprof_' + simname + sizingappend + '.mp4'
anim.save(entprof_saveas)
print 'entprof: Saved animation ' + entprof_saveas
