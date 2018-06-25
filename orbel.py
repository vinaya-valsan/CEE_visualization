from __main__ import *
import yt
import matplotlib.pyplot as pl

orbel_dotsize = 10

# define norm
def norm(a) :
	return np.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])

# preallocate
time = np.zeros(nframes)
ecc = np.zeros(nframes)
a_norm = np.zeros(nframes)
sep = np.zeros(nframes)

G = 6.674e-8
Rsun = 7.0e10
timeconv = np.sqrt(G) # codetime / second

# calculate
for i in range(0,nframes):
	
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'orbel: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')

	pos = ad[('DarkMatter','Coordinates')]/cl
	vel = ad[('DarkMatter','Velocities')]/cv
	mass = ad[('DarkMatter','particle_mass')]/cm
	posPrim = pos[0,:]
	posComp = pos[1,:]
	vPrim = vel[0,:]
	vComp = vel[1,:]
	mPrim = mass[0]
	mComp = mass[1]
	vRel = vComp - vPrim
	mTot = mPrim + mComp
	mRed = mPrim*mComp/(mPrim+mComp)
	r = posComp - posPrim
	rScalar = norm(r)
	vScalar = norm(vRel)
	Em = vScalar*vScalar/2.0 - mTot/rScalar
	a = -mTot/2.0/Em
	Hm = np.cross(r,vRel)
	HmScalar = norm(Hm)
	p = HmScalar*HmScalar/mTot
	ecc[i] = np.sqrt(1.0-p/a)
	sep[i] = rScalar / Rsun
	a_norm[i] = a / Rsun
	
	time[i] = dDelta * frameskip * (i+1.0)

# plot
pl.clf()

pl.scatter(time, sep, s= orbel_dotsize )
pl.xlabel('Time')
pl.ylabel('Separation (Solar Radii)')
pl.title(simname + ' Separation')
sep_saveas = writepath + 'sep_' + simname + '.pdf'
pl.savefig(sep_saveas)
print 'orbel: Saved figure ' + sep_saveas

pl.clf()

pl.scatter(time, a_norm, s= orbel_dotsize )
pl.xlabel('Time')
pl.ylabel('Semi-Major Axis (Solar Radii)')
pl.title(simname + ' Semi-Major Axis')
sma_saveas = writepath + 'sma_' + simname + '.pdf'
pl.savefig(sma_saveas)
print 'orbel: Saved figure ' + sma_saveas

pl.clf()

pl.scatter(time, ecc, s= orbel_dotsize )
pl.xlabel('Time')
pl.ylabel('Eccentricity')
pl.title(simname + ' Eccentricity')
ecc_saveas = writepath + 'ecc_' + simname + '.pdf'
pl.savefig(ecc_saveas)
print 'orbel: Saved figure ' + ecc_saveas

pl.clf()
