from __main__ import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
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

if plot_mesa :
	from mesastuff import *
	mesaT, mesamass, mesaR, mesarho, mesaP = getMesa(mesadata)
	mesaent, dm = getMesaEnt(mesadata)

fig = plt.figure()

def animate(i):
	plt.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'entprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()
	x = ad[('gas','x')]
	y = ad[('gas','y')]
	z = ad[('gas','z')]

	# g = ds.arr(1.0,'g')
	# mass = ad[('gas','cell_mass')]/g

	if corecorrect :
		corepos = ad[('DarkMatter','Coordinates')]
		corex = corepos[0,0]
		corey = corepos[0,1]
		corez = corepos[0,2]
		x = x - corex
		y = y - corey
		z = z - corez
	
	radius = norm(x,y,z)
	ent = ad[('gas','entropy')]
	# ent = ent.in_units("cm**2*erg") / G
	time[i] = getTime(ds)
	
	scat = plt.scatter(radius,ent,s= entprof_dotsize)
	plt.xscale('log')
	plt.yscale('log')
	plt.xticks( fontsize=20)
	plt.yticks( fontsize=20)
	plt.tight_layout()
	
	if entprof_fixaxes:
		plt.axis(entprof_axes)

	if plot_mesa :
		plt.scatter( mesaR, mesaent, s=entprof_dotsize )
	
	plt.xlabel('Radius (cm)', fontsize=25 )
	plt.ylabel('Entropy (code units?)', fontsize=25 )
	# plt.title('Radial Entropy Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )
	return scat
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
entprof_saveas = writepath + 'entprof_' + simname + sizingappend + '.mp4'
anim.save(entprof_saveas)
print 'entprof: Saved animation ' + entprof_saveas
