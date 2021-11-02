from __main__ import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *

radprof_dotsize = 1

if plot_mesa :
	from mesastuff import *
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)

plt.clf()
fig = plt.figure(figsize=(9,9))

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

time = getTime(ds)

ad = ds.all_data()
pos = ad[('Gas','Coordinates')]

if corecorrect :
	corepos = ad[('DarkMatter','Coordinates')]
	pos = pos - corepos

radius = np.linalg.norm(pos, axis=1)[::partskip]
density = ad[('Gas','rho')][::partskip]

scat = plt.scatter( radius, density, s=2*radprof_dotsize )
plt.xscale('log')
plt.yscale('log')
plt.xticks( fontsize=30)
plt.yticks( fontsize=30)

if radprof_fixaxes:
	plt.axis(radprof_axes)

# plt.xlabel('Radius ($cm$)', fontsize=25 )
# plt.ylabel('Density ($g/cm^3$)', fontsize=25 )
plt.xlabel(r'$r~/~\rm{cm}$', fontsize=35 )
plt.ylabel(r'$\rho~/~\rm{g~cm^{-3}}$', fontsize=35 )
# plt.title('Radial Density Profile ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if plot_mesa :
	plt.scatter( mesaR, mesarho, s=2*radprof_dotsize )

if plot_cutoff :
	plt.hlines( cutoffRho, 1.0, 1.0e16 )

plt.tight_layout()

saveas = writepath + 'radprof_snap_' + simname + '_ds' + str(dataset) + '.pdf'
fig.savefig(saveas)
print 'radprof_snapshot: Saved image ' + saveas
plt.clf()
