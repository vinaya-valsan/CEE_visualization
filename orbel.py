from __main__ import *
import yt
import matplotlib.pyplot as pl

Rsun = 7.0e10
shellPrim = 10.0 * Rsun
shellComp = 10.0 * Rsun

orbel_dotsize = 10

# define norm
def norm(a) :
	return np.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])

# preallocate
time = np.zeros(nframes)
ecc = np.zeros(nframes)
sep = np.zeros(nframes)
xRel = np.zeros(nframes)
yRel = np.zeros(nframes)
is_peri = np.full(nframes, False, dtype = bool)
is_apo = np.full(nframes, False, dtype = bool)
periapse = np.zeros(nframes)
apoapse = np.zeros(nframes)
peridomain = np.zeros(nframes)
apodomain = np.zeros(nframes)
a = np.zeros(nframes)

G = 6.674e-8
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
	gasmass = ad[('Gas','Mass')]/cm
	gaspos = ad[('Gas','Coordinates')]/cl
	npcles = len(gasmass)
	posPrim = pos[0,:]
	posComp = pos[1,:]
	vPrim = vel[0,:]
	vComp = vel[1,:]
	mPrim = mass[0]
	mComp = mass[1]

	mGasPrim = 0.0
	mGasComp = 0.0

	mPrimTot = mPrim + mGasPrim
	mCompTot = mComp + mGasComp

	r = posComp - posPrim
	rScalar = norm(r)

	sep[i] = rScalar / Rsun
	
	time[i] = dDelta * frameskip * (i+1.0)
	xRel[i] = posComp[0] - posPrim[0]
	yRel[i] = posComp[1] - posPrim[1]

periapse[0] = sep[0]
apoapse[0] = sep[0]
a[0] = sep[0]
pericount = 0
apocount = 0
peridomain[0] = 0
apodomain[0] = 0
is_peri[0] = True
is_apo[0] = True
is_peri[nframes-1] = True
is_apo[nframes-1] = True
for k in range(1,nframes-1):
	if( sep[k] > sep[k-1] and sep[k] > sep[k+1]):
		is_apo[k] = True
		apocount = apocount + 1
		apodomain[apocount] = k
	if( sep[k] < sep[k-1] and sep[k] < sep[k+1]):
		is_peri[k] = True
		pericount = pericount + 1
		peridomain[pericount] = k
apodomain[apocount+1] = nframes-1
peridomain[pericount+1] = nframes-1

apocount = 0
pericount = 0
for m in range(1,nframes):
	apoapse[m] = np.interp(m, [apodomain[apocount], apodomain[apocount+1]], [sep[int(apodomain[apocount])], sep[int(apodomain[apocount+1])]])
	periapse[m] = np.interp(m, [peridomain[pericount], peridomain[pericount+1]], [sep[int(peridomain[pericount])], sep[int(peridomain[pericount+1])]])
	a[m] = (apoapse[m] + periapse[m]) / 2.0
	ecc[m] = (apoapse[m] - periapse[m]) / (apoapse[m] + periapse[m])
	if is_apo[m]:
		apocount = apocount + 1
	if is_peri[m]:
		pericount = pericount + 1

print "peridomain = ",peridomain
print "apodomain = ",apodomain
print "pericount = ",pericount
print "apocount = ",apocount

# plot
pl.clf()

pl.plot(time, sep, c='b')
# pl.plot(time, periapse, c='g')
# pl.plot(time, apoapse, c='c')
pl.plot(time, a, c='r')
pl.xlabel('Time')
pl.ylabel('Distance (Solar Radii)')
pl.title(simname + ' Separation')
sep_saveas = writepath + 'sep_' + simname + '.pdf'
pl.savefig(sep_saveas)
print 'orbel: Saved figure ' + sep_saveas

pl.clf()

pl.plot(xRel, yRel )
pl.xlabel('x')
pl.ylabel('y')
pl.title(simname + ' Relative Position')
relpos_saveas = writepath + 'relpos_' + simname + '.pdf'
pl.savefig(relpos_saveas)
print 'orbel: Saved figure ' + relpos_saveas

pl.clf()

pl.plot(time, ecc)
pl.xlabel('Time')
pl.ylabel('Eccentricity')
pl.title(simname + ' Eccentricity')
ecc_saveas = writepath + 'ecc_' + simname + '.pdf'
pl.savefig(ecc_saveas)
print 'orbel: Saved figure ' + ecc_saveas

pl.clf()
