from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from berniter import *
from timestuff import *

enercomp_dotsize = 1
time = np.zeros(nframes)
fracunbound = np.zeros(nframes)

enercomp_fixylim = 1
ylow  = 1.0e19
yhigh = 1.0e24

gamma = 5.0/3.0
G = 6.674e-8
R = 8.314e7 / G

fig_x = 15
fig_y = 9
bindist = np.linspace(19,24,20)

# create figure
fig = pl.figure(figsize=(fig_x,fig_y))

# create each frame
def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'enercomp: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	time[i], timelabel = getTime(ds, i)

	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K  = ds.arr(1.0, 'K')

	pos = ad[('Gas','Coordinates')]/cl
	phi = ad[('Gas','Phi')]/cl
	v = ad[('Gas','Velocities')]/cv
	mass = ad[('Gas','Mass')]/cm
	temp = ad[('Gas','Temperature')]/K

	x = pos[:,0]
	posCM, velCM = getCM(ds)
	vnorm = np.linalg.norm( v - velCM, axis=1 )
	KE = 0.5 * np.multiply(vnorm,vnorm)
	enthalpy = gamma / (gamma-1.0) * R * temp
	minusPE = -phi
	bern = KE + enthalpy + phi

	minusPE = np.clip(minusPE, 1.0, None)

	unbound = np.clip(bern, 0.0, 1.0)
	unboundmass = np.multiply( unbound, mass )
	gasmass = mass.sum()
	fracunbound[i] = unboundmass.sum() / gasmass

	axes = [19, 24, 0, len(x)]
	bernlim = 0.5e22

	pl.subplot( 2, 4, 1 )
	pl.scatter( x, minusPE, s= enercomp_dotsize, c='b' )
	pl.yscale('log')
	if enercomp_fixylim :
		pl.ylim(ylow,yhigh)
	pl.title('Potential ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

	pl.subplot( 2, 4, 2 )
	pl.scatter( x, KE, s= enercomp_dotsize, c='g' )
	pl.yscale('log')
	if enercomp_fixylim :
		pl.ylim(ylow,yhigh)
	pl.title('kinetic')

	pl.subplot( 2, 4, 3 )
	pl.scatter( x, enthalpy, s= enercomp_dotsize, c='r' )
	pl.yscale('log')
	if enercomp_fixylim :
		pl.ylim(ylow,yhigh)
	pl.title('enthalpy')

	pl.subplot( 2, 4, 4 )
	pl.scatter( x, bern, s= enercomp_dotsize, c='k' )
	# pl.yscale('log')
	if enercomp_fixylim :
		pl.ylim(-bernlim, 2.0*bernlim)
	pl.title('bernoulli')

	pl.subplot( 2, 4, 5 )
	pl.hist( np.log10(minusPE), bins = bindist, facecolor='b' )
	pl.xlabel('x (cm)')
	pl.axis(axes)

	pl.subplot( 2, 4, 6 )
	pl.hist( np.log10(KE), bins = bindist, facecolor='g' )
	pl.xlabel('x (cm)')
	pl.axis(axes)

	pl.subplot( 2, 4, 7 )
	pl.hist( np.log10(enthalpy), bins = bindist, facecolor='r' )
	pl.xlabel('x (cm)')
	pl.axis(axes)

	pl.subplot( 2, 4, 8 )
	pl.hist( bern, bins = np.linspace(-bernlim,bernlim,20), facecolor='k' )
	pl.xlabel('x (cm)')
	pl.axis([-bernlim, bernlim, 0, len(x)])
	
# create animation object
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
enercomp_saveas = writepath + 'enercomp_' + simname + '.mp4'
anim.save(enercomp_saveas)
print 'enercomp: Saved animation ' + enercomp_saveas

pl.clf()
fig = pl.figure()
plot = pl.plot( time, fracunbound )
pl.xlabel('Time (' + timelabel + ')' )
pl.ylabel('Fraction of Mass Unbound')
pl.title('Unbound Mass')
saveas = writepath + 'unbound_' + simname + '.pdf'
fig.savefig(saveas)
print 'enercomp: Saved plot ' + saveas
pl.clf()
