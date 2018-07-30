from __main__ import *
import yt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from berniter import *
from timestuff import *

nbins = 20
enercomp_dotsize = 1
time = np.zeros(nframes)

fig_x = 15
fig_y = 9
bindist = np.linspace( np.log10(ener_low), np.log10(ener_high), nbins+1 )

fig = plt.figure(figsize=(fig_x,fig_y))
timelabel = np.chararray(nframes, itemsize = 10)

def animate(i):
	plt.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'enercomp: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut

	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()

	time[i], timelabel[i] = getTime(ds, i)

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K  = ds.arr(1.0, 'K')

	pos = ad[('Gas','Coordinates')]/cl
	phi = ad[('Gas','Phi')]/cl
	v = ad[('Gas','Velocities')]/cv
	mass = ad[('Gas','Mass')]/cm
	temp = ad[('Gas','Temperature')]/K
	massDM = ad[('DarkMatter','Mass')]/cm

	x = pos[:,0]
	posCM, velCM = getCM(ds)
	vnorm = np.linalg.norm( v - velCM, axis=1 )
	KE = 0.5 * np.multiply(vnorm,vnorm)

	if useIE:
		enthalpy = ad[('Gas','ie')]
	else:
		enthalpy = gamma / (gamma-1.0) * R * temp

	minusPE = -phi
	bern = KE + enthalpy + phi

	minusPE = np.clip(minusPE, 1.0, None)

	axes = [np.log10(ener_low), np.log10(ener_high), 0, mass.sum()]

	plt.subplot( 2, 4, 1 )
	plt.scatter( x, minusPE, s= enercomp_dotsize, c='b' )
	plt.xlabel('x (cm)')
	plt.ylabel('Energy (code units)')
	plt.yscale('log')
	plt.ylim( ener_low, ener_high )
	plt.title('Potential ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel[i] )

	plt.subplot( 2, 4, 2 )
	plt.scatter( x, KE, s= enercomp_dotsize, c='g' )
	plt.xlabel('x (cm)')
	plt.yscale('log')
	plt.ylim( ener_low, ener_high )
	plt.title('Kinetic')

	plt.subplot( 2, 4, 3 )
	plt.scatter( x, enthalpy, s= enercomp_dotsize, c='r' )
	plt.xlabel('x (cm)')
	plt.yscale('log')
	plt.ylim( ener_low, ener_high )
	plt.title('Enthalpy')

	plt.subplot( 2, 4, 4 )
	plt.scatter( x, bern, s= enercomp_dotsize, c='k' )
	plt.xlabel('x (cm)')
	plt.ylim(-bernlim, 2.0*bernlim)
	plt.title('Bernoulli')

	plt.subplot( 2, 4, 5 )
	plt.hist( np.log10(minusPE), bins = bindist, facecolor='b', weights = mass )
	plt.xlabel('Log Energy')
	plt.ylabel('Mass')
	plt.axis(axes)

	plt.subplot( 2, 4, 6 )
	plt.hist( np.log10(KE), bins = bindist, facecolor='g', weights = mass )
	plt.xlabel('Log Energy')
	plt.axis(axes)

	plt.subplot( 2, 4, 7 )
	plt.hist( np.log10(enthalpy), bins = bindist, facecolor='r', weights = mass )
	plt.xlabel('Log Energy')
	plt.axis(axes)

	plt.subplot( 2, 4, 8 )
	plt.hist( bern, bins = np.linspace(-bernlim,bernlim,nbins+1), facecolor='k', weights = mass )
	plt.xlabel('Energy')
	plt.axis([-bernlim, bernlim, 0, mass.sum()])
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
enercomp_saveas = writepath + 'enercomp_' + simname + '.mp4'
anim.save(enercomp_saveas)
print 'enercomp: Saved animation ' + enercomp_saveas

plt.clf()
