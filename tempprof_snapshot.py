from __main__ import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *

tempprof_dotsize = 1

if plot_mesa :
	from mesastuff import *
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)

plt.clf()
fig = plt.figure()

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

scat = plt.scatter( radius, temp, s=tempprof_dotsize )
plt.xscale('log')
plt.yscale('log')
plt.xticks( fontsize=20)
plt.yticks( fontsize=20)
plt.tight_layout()

if tempprof_fixaxes:
	plt.axis(tempprof_axes)

plt.xlabel('Radius (cm)', fontsize=25 )
plt.ylabel('Temperature (K)', fontsize=25 )
# plt.title('Radial Temperature Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if plot_mesa :
	plt.scatter( mesaR, mesaT, s=tempprof_dotsize )
	
saveas = writepath + 'tempprof_snap_' + simname + '_ds' + str(dataset) + '.pdf'
fig.savefig(saveas)
print 'tempprof_snapshot: Saved image ' + saveas
plt.clf()
