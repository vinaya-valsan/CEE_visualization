from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

radprof_dotsize = 1

if plot_mesa :
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)

pl.clf()
fig = pl.figure()

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut)

time, timelabel = getTime(ds, dataset-1)

ad = ds.all_data()
pos = ad[('Gas','Coordinates')]

if corecorrect :
	corepos = ad[('DarkMatter','Coordinates')]
	pos = pos - corepos

radius = np.linalg.norm(pos, axis=1)[::partskip]
density = ad[('Gas','rho')][::partskip]

scat = pl.scatter( radius, density, s=radprof_dotsize )
pl.xscale('log')
pl.yscale('log')

if radprof_fixaxes:
	pl.axis(radprof_axes)

pl.xlabel('Radius (cm)')
pl.ylabel('Density (g/cm^3)')
# pl.title('Radial Density Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if plot_mesa :
	pl.scatter( mesaR, mesarho, s=radprof_dotsize )

if plot_cutoff :
	pl.hlines( cutoffRho, 1.0, 1.0e16 )
	
saveas = writepath + 'radprof_snap_' + simname + '.pdf'
fig.savefig(saveas)
print 'radprof_snapshot: Saved image ' + saveas
pl.clf()
