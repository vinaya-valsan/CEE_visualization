from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

tempprof_dotsize = 1

if plot_mesa :
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)

pl.clf()
fig = pl.figure()

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

time, timelabel = getTime(ds, dataset-1)

ad = ds.all_data()
pos = ad[('Gas','Coordinates')]

if corecorrect :
	corepos = ad[('DarkMatter','Coordinates')]
	pos = pos - corepos

radius = np.linalg.norm(pos, axis=1)[::partskip]
temp = ad[('Gas','Temperature')][::partskip]

scat = pl.scatter( radius, temp, s=tempprof_dotsize )
pl.xscale('log')
pl.yscale('log')

if tempprof_fixaxes:
	pl.axis(tempprof_axes)

pl.xlabel('Radius (cm)')
pl.ylabel('Temperature (K)')
# pl.title('Radial Temperature Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if plot_mesa :
	pl.scatter( mesaR, mesaT, s=tempprof_dotsize )
	
saveas = writepath + 'tempprof_snap_' + simname + '.pdf'
fig.savefig(saveas)
print 'tempprof_snapshot: Saved image ' + saveas
pl.clf()
