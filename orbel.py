from __main__ import *
import yt
import matplotlib.pyplot as pl
from yt import YTQuantity
from berniter import *
from timestuff import *

orbel_dotsize = 10

num = 1000000 + startingset
numstr = str(num)
cut = numstr[1:7]

ts = yt.load( readpath + outprefix + cut )

cl = ts.arr(1.0, 'code_length')
cm = ts.arr(1.0, 'code_mass')
cv = ts.arr(1.0, 'code_velocity')
K = YTQuantity(1.0,'K')
kmps = YTQuantity(1.0,'km/s')

time = np.zeros(nframes)
ecc = np.zeros(nframes)
sep = np.zeros(nframes)
is_peri = np.full(nframes, False, dtype = bool)
is_apo = np.full(nframes, False, dtype = bool)
periapse = np.zeros(nframes)
apoapse = np.zeros(nframes)
peridomain = np.zeros(nframes)
apodomain = np.zeros(nframes)
posCM = np.zeros((nframes,3))
velCM = np.zeros((nframes,3))
velCMnorm = np.zeros(nframes)
a = np.zeros(nframes)
posPrim = np.zeros((nframes,3))
posComp = np.zeros((nframes,3))

for i in range(0,nframes):
	
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'orbel: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')

	pos = ad[('DarkMatter','Coordinates')]/cl
	posPrim[i,:] = pos[0,:]
	posComp[i,:] = pos[1,:]

	r = posComp[i,:] - posPrim[i,:]
	rScalar = np.linalg.norm(r)
	sep[i] = rScalar / Rsun
	
	time[i], timelabel = getTime(ds, i)
	posCM[i,:], velCM[i,:] = getCM(ds)

velCMnorm = np.linalg.norm(velCM, axis=1) * cv.in_units('km/s')

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
boolArray = np.zeros( nframes, dtype=bool )
for m in range(1,nframes):
	apoapse[m] = np.interp(m, [apodomain[apocount], apodomain[apocount+1]], 
		[sep[int(apodomain[apocount])], sep[int(apodomain[apocount+1])]])
	periapse[m] = np.interp(m, [peridomain[pericount], peridomain[pericount+1]], 
		[sep[int(peridomain[pericount])], sep[int(peridomain[pericount+1])]])
	if (apodomain[apocount+1] == nframes-1) or (peridomain[pericount+1] == nframes-1) :
		a[m] = 0.
		ecc[m] = 0.
	elif (apodomain[apocount] == 0 or peridomain[pericount] == 0) :
		a[m] = 0.
		ecc[m] = 0.
	else :
		a[m] = (apoapse[m] + periapse[m]) / 2.0
		ecc[m] = (apoapse[m] - periapse[m]) / (apoapse[m] + periapse[m])
		boolArray[m] = True
	if is_apo[m]:
		apocount = apocount + 1
	if is_peri[m]:
		pericount = pericount + 1

pl.clf()
fig = pl.figure(figsize=(9,9))

pl.subplot(2,2,1)
pl.plot(time, sep, c='b')
# pl.plot(time, periapse, c='g')
# pl.plot(time, apoapse, c='c')
pl.plot(time[boolArray], a[boolArray], c='r')
pl.xlabel('Time (' + timelabel + ')' )
pl.ylabel('Distance (Solar Radii)')
pl.title(simname + ' Separation')

pl.subplot(2,2,3)
pl.plot( posPrim[:,0], posPrim[:,1], c='g', label='primary' )
pl.plot( posComp[:,0], posComp[:,1], c='b', label='comp' )
pl.plot( posCM[:,0], posCM[:,1], c='r', label='CM' )
pl.legend()
pl.xlabel('x (cm)')
pl.ylabel('y (cm)')
pl.title('Positions')

pl.subplot(2,2,4)
pl.plot(time, velCMnorm)
pl.xlabel('Time (' + timelabel + ')' )
pl.ylabel('CM Velocity (km/s)')
pl.title('CM Velocity')

pl.subplot(2,2,2)
pl.plot(time[boolArray], ecc[boolArray])
pl.xlabel('Time (' + timelabel + ')' )
pl.ylabel('Eccentricity')
pl.title('Eccentricity')

saveas = writepath + 'orbel_' + simname + '.pdf'
fig.savefig(saveas)
print 'orbel: Saved figure ' + saveas

pl.clf()
