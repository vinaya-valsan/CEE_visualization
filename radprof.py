from __main__ import *
import yt
import matplotlib
matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *

radprof_dotsize = 1
time = np.zeros(nframes)

if radprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

if plot_mesa :
	from mesastuff import *
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)

fig = plt.figure()

def animate(i):
	plt.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'radprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()
	pos = ad[('Gas','Coordinates')]

	if corecorrect :
		corepos = ad[('DarkMatter','Coordinates')]
		pos = pos - corepos
	
	radius = np.linalg.norm(pos, axis=1)
	density = ad[('Gas','rho')]
	time[i], timelabel = getTime(ds, i)
	
	scat = plt.scatter( radius, density, s=radprof_dotsize )
	plt.xscale('log')
	plt.yscale('log')
	
	if radprof_fixaxes:
		plt.axis(radprof_axes)
	
	plt.xlabel('Radius ($cm$)', fontsize=25 )
	plt.ylabel('Density ($g/cm^{3}$)', fontsize=25 )
	plt.xticks( fontsize=20)
	plt.yticks( fontsize=20)
	plt.tight_layout()
	# plt.title('Radial Density Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

	if plot_mesa :
		plt.scatter( mesaR, mesarho, s=radprof_dotsize )

	if plot_cutoff :
		plt.hlines( cutoffRho, 1.0, 1.0e16 )

	return scat
	plt.clf()
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
radprof_saveas = writepath + 'radprof_' + simname + sizingappend + '.mp4'
anim.save(radprof_saveas)
print 'radprof: Saved animation ' + radprof_saveas
