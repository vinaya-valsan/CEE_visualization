from __main__ import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
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
	
	time[i] = getTime(ds)
	posCM[i,:], velCM[i,:] = getCM(ds, IE=useIE)

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

##############################################

plt.clf()
fig = plt.figure(figsize=(9,9))

plt.subplot(2,2,1)
plt.plot(time, sep, c='b', lw=2)
# plt.plot(time, periapse, c='g')
# plt.plot(time, apoapse, c='c')
plt.plot(time[boolArray], a[boolArray], c='r', lw=2)
plt.xlabel('Time (' + timelabel + ')' )
plt.ylabel('Distance (Solar Radii)')
plt.title(simname + ' Separation')

plt.subplot(2,2,3)
plt.plot( posPrim[:,0], posPrim[:,1], c='g', lw=2, label='primary' )
plt.plot( posComp[:,0], posComp[:,1], c='b', lw=2, label='comp' )
plt.plot( posCM[:,0], posCM[:,1], c='r', lw=2, label='CM' )
plt.legend()
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Positions')

plt.subplot(2,2,4)
plt.plot(time, velCMnorm, lw=2)
plt.xlabel('Time (' + timelabel + ')' )
plt.ylabel('CM Velocity (km/s)')
plt.title('CM Velocity')

plt.subplot(2,2,2)
plt.plot(time[boolArray], ecc[boolArray], lw=2)
plt.xlabel('Time (' + timelabel + ')' )
plt.ylabel('Eccentricity')
plt.title('Eccentricity')

plt.tight_layout()

saveas = writepath + 'orbel_' + simname + '.pdf'
fig.savefig(saveas)
print 'orbel: Saved figure ' + saveas

plt.clf()

############### PAPER MODE ###################

# plt.clf()

# # plt.subplot(2,2,1)
# plt.plot(time, sep, c='b', lw=2 )
# # plt.plot(time, periapse, c='g')
# # plt.plot(time, apoapse, c='c')
# plt.plot(time[boolArray], a[boolArray], c='r', lw=2 )
# plt.axis([0., 120., 0., 54.])
# plt.xlabel('Time (' + timelabel + ')', fontsize=25 )
# plt.ylabel(r'Distance ($R_{\odot}$)', fontsize=25)
# plt.xticks( fontsize=20)
# plt.yticks( fontsize=20)
# saveas = writepath + 'separation_' + simname + '.pdf'
# plt.tight_layout()
# plt.savefig(saveas)
# print 'orbel: Saved figure ' + saveas

# plt.clf()

# plt.plot(time[boolArray], ecc[boolArray], lw=2)
# plt.xlabel('Time (' + timelabel + ')', fontsize=25 )
# plt.ylabel('Eccentricity', fontsize=25)
# plt.xticks( fontsize=20)
# plt.yticks( fontsize=20)
# plt.tight_layout()
# saveas = writepath + 'ecc_' + simname + '.pdf'
# plt.savefig(saveas)
# print 'orbel: Saved figure ' + saveas

# plt.clf()
