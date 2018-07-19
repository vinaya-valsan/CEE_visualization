from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from berniter import *
from timestuff import *

nbins = 20
enercomp_dotsize = 1
time = np.zeros(nframes)
fracunbound = np.zeros(nframes)

fig_x = 15
fig_y = 9
bindist = np.linspace( np.log10(bern_low), np.log10(bern_high), nbins+1 )

fig = pl.figure(figsize=(fig_x,fig_y))
timelabel = np.chararray(nframes, itemsize = 10)

def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'enercomp: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut

	ds = yt.load(readpath + outprefix + cut)
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
	enthalpy = gamma / (gamma-1.0) * R * temp
	# enthalpy = R * temp + ad[('Gas','ie')]
	minusPE = -phi
	bern = KE + enthalpy + phi

	minusPE = np.clip(minusPE, 1.0, None)

	unbound = np.clip(bern, 0.0, 1.0)
	unboundmass = np.multiply( unbound, mass )
	gasmass = mass.sum()
	fracunbound[i] = unboundmass.sum() / ( gasmass + massDM.sum() )

	axes = [np.log10(bern_low), np.log10(bern_high), 0, len(x)]

	pl.subplot( 2, 4, 1 )
	pl.scatter( x, minusPE, s= enercomp_dotsize, c='b' )
	pl.xlabel('x (cm)')
	pl.ylabel('Energy (code units)')
	pl.yscale('log')
	pl.ylim( bern_low, bern_high )
	pl.title('Potential ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel[i] )

	pl.subplot( 2, 4, 2 )
	pl.scatter( x, KE, s= enercomp_dotsize, c='g' )
	pl.xlabel('x (cm)')
	pl.yscale('log')
	pl.ylim( bern_low, bern_high )
	pl.title('Kinetic')

	pl.subplot( 2, 4, 3 )
	pl.scatter( x, enthalpy, s= enercomp_dotsize, c='r' )
	pl.xlabel('x (cm)')
	pl.yscale('log')
	pl.ylim( bern_low, bern_high )
	pl.title('Enthalpy')

	pl.subplot( 2, 4, 4 )
	pl.scatter( x, bern, s= enercomp_dotsize, c='k' )
	pl.xlabel('x (cm)')
	pl.ylim(-bernlim, 2.0*bernlim)
	pl.title('Bernoulli')

	pl.subplot( 2, 4, 5 )
	pl.hist( np.log10(minusPE), bins = bindist, facecolor='b' )
	pl.xlabel('Log Energy')
	pl.ylabel('Number of Particles')
	pl.axis(axes)

	pl.subplot( 2, 4, 6 )
	pl.hist( np.log10(KE), bins = bindist, facecolor='g' )
	pl.xlabel('Log Energy')
	pl.axis(axes)

	pl.subplot( 2, 4, 7 )
	pl.hist( np.log10(enthalpy), bins = bindist, facecolor='r' )
	pl.xlabel('Log Energy')
	pl.axis(axes)

	pl.subplot( 2, 4, 8 )
	pl.hist( bern, bins = np.linspace(-bernlim,bernlim,nbins+1), facecolor='k' )
	pl.xlabel('Log Energy')
	pl.axis([-bernlim, bernlim, 0, len(x)])
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
enercomp_saveas = writepath + 'enercomp_' + simname + '.mp4'
anim.save(enercomp_saveas)
print 'enercomp: Saved animation ' + enercomp_saveas

pl.clf()
fig = pl.figure()
plot = pl.plot( time, fracunbound )
pl.xlabel('Time (' + timelabel[0] + ')' )
pl.ylabel('Fraction of Mass Unbound')
pl.title('Unbound Mass')
saveas = writepath + 'unbound_' + simname + '.pdf'
fig.savefig(saveas)
print 'enercomp: Saved plot ' + saveas
pl.clf()
