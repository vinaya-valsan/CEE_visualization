from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

tempprof_dotsize = 1
time = np.zeros(nframes)

if tempprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

if plot_mesa :
	mesaT, mesamass, mesaR, mesarho = getMesa(mesadata)

fig = pl.figure()

def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'tempprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()
	pos = ad[('Gas','Coordinates')]

	if corecorrect :
		corepos = ad[('DarkMatter','Coordinates')]
		pos = pos - corepos
	
	radius = np.linalg.norm(pos, axis=1)
	temp = ad[('Gas','Temperature')]
	time[i], timelabel = getTime(ds, i)
	
	scat = pl.scatter(radius,temp,s= tempprof_dotsize)
	pl.xscale('log')
	pl.yscale('log')
	
	if tempprof_fixaxes:
		pl.axis(tempprof_axes)
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Temperature (K)')
	pl.title('Radial Temperature Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

	if plot_mesa :
		pl.scatter( mesaR, mesaT, s=tempprof_dotsize )

	return scat
	pl.clf()
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
tempprof_saveas = writepath + 'tempprof_' + simname + sizingappend + '.mp4'
anim.save(tempprof_saveas)
print 'tempprof: Saved animation ' + tempprof_saveas
