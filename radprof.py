from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

corecorrect = 1
plot_mesa = 1
radprof_dotsize = 1
time = np.zeros(nframes)

if radprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

if plot_mesa :
	mesaT, mesamass, mesaR, mesarho = getMesa('profile17.data')

# create figure
fig = pl.figure()

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

	if corecorrect :
		corepos = ad[('DarkMatter','Coordinates')]
		pos = pos - corepos
	
	radius = np.linalg.norm(pos, axis=1)
	density = ad[('Gas','rho')]
	time[i], timelabel = getTime(ds, i)
	
	scat = pl.scatter( radius, density, s=radprof_dotsize )
	pl.xscale('log')
	pl.yscale('log')
	
	if radprof_fixaxes:
		pl.axis(radprof_axes)
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Density (g/cm^3)')
	pl.title('Radial Density Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

	if plot_mesa :
		pl.scatter( mesaR, mesarho, s=radprof_dotsize )

	return scat
	pl.clf()
	
# create animation object
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
radprof_saveas = writepath + 'radprof_' + simname + sizingappend + '.mp4'
anim.save(radprof_saveas)
print 'radprof: Saved animation ' + radprof_saveas
