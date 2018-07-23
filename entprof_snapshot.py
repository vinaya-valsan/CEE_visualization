from __main__ import *

import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from timestuff import *

def norm(a,b,c) :
	return np.sqrt( np.multiply(a,a) + np.multiply(b,b) + np.multiply(c,c) )

entprof_dotsize = 1

if plot_mesa :
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)
	mesaent = getMesaEnt2(mesadata)

pl.clf()
fig = pl.figure()

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

time, timelabel = getTime(ds, dataset-1)

ad = ds.all_data()

# x = ad[('gas','x')]
# y = ad[('gas','y')]
# z = ad[('gas','z')]
# mass = ad[('gas','cell_mass')]
# mass = mass[::partskip]

# if corecorrect :
# 	corepos = ad[('DarkMatter','Coordinates')]
# 	corex = corepos[0,0]
# 	corey = corepos[0,1]
# 	corez = corepos[0,2]
# 	x = x - corex
# 	y = y - corey
# 	z = z - corez

pos = ad[('Gas','Coordinates')]
x = pos[:,0]
y = pos[:,1]
z = pos[:,2]
mass = ad[('Gas','Mass')]

mcore = 0.
if corecorrect :
	corepos = ad[('DarkMatter','Coordinates')]
	corex = corepos[0,0]
	corey = corepos[0,1]
	corez = corepos[0,2]
	x = x - corex
	y = y - corey
	z = z - corez
	massDM = ad[('DarkMatter','Mass')]
	mcore = massDM[0]

radius = norm(x,y,z)
ent = getEnt3(ds)

sort = np.argsort(radius)
masscoord = np.cumsum( mass[sort] ) + mcore
entcoord = ent[sort]

radius = radius[::partskip]
ent = ent[::partskip]
masscoord = masscoord[::partskip]
entcoord = entcoord[::partskip]

scat = pl.scatter( radius, ent, s=entprof_dotsize )
pl.xscale('log')
pl.yscale('log')

if entprof_fixaxes:
	pl.axis(entprof_axes)

pl.xlabel('Radius (cm)')
pl.ylabel('Entropy')
# pl.title('Radial Entropy Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if plot_mesa :
	pl.scatter( mesaR, mesaent, s=entprof_dotsize )
	
saveas = writepath + 'entprof_snap_' + simname + '.pdf'
fig.savefig(saveas)
print 'entprof_snapshot: Saved image ' + saveas
pl.clf()

fig2 = pl.figure()

scat = pl.scatter( masscoord, entcoord, s=entprof_dotsize )
if plot_mesa :
	pl.scatter( mesamass, mesaent, s=entprof_dotsize )
pl.xscale('log')
pl.yscale('log')
pl.xlabel('Mass (g)')
pl.ylabel('Entropy')
# pl.title('Entropy vs Mass Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

pl.axis( [7.0e32, 4.0e33, 1.0e23, 1.0e25] )

saveas = writepath + 'entvsm_snap_' + simname + '.pdf'
fig2.savefig(saveas)
print 'entvsm_snapshot: Saved image ' + saveas
pl.clf()
