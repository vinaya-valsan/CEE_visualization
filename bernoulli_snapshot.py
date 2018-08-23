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

userho = 0

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]

ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

cl = ds.arr(1.0, 'code_length')
cm = ds.arr(1.0, 'code_mass')
cv = ds.arr(1.0, 'code_velocity')
K = YTQuantity(1.0,'K')

def _bern(field, data) :
	PE = data[('Gas','Phi')]/cl
	posCM, velCM = getCM(data.ds, IE=useIE)
	v = np.linalg.norm( data[('Gas','Velocities')]/cv - velCM, axis=1 )
	KE = 0.5*np.multiply(v,v)
	if useIE:
		enthalpy = data[('Gas','ie')]
	else:
		enthalpy = gamma / (gamma-1.0) * R * data[('Gas','Temperature')] / K
	bern = PE + KE + enthalpy
	if userho :
		rho = data[('Gas','rho')]
		bern = np.multiply( bern, rho )
	return bern

yt.add_field(('Gas','bernoulli'), function = _bern, particle_type = True )

plt.clf()
fig = plt.figure(figsize=(10,8))

ad = ds.all_data()
time, timelabel = getTime(ds, dataset-1)

pos = ad[('Gas','Coordinates')]/cl
x = pos[:,0]
y = pos[:,1]
z = pos[:,2]
bern = ad[('Gas','bernoulli')]

boolArray = np.absolute(z) < dPeriod * 0.5 * bernslice
x = x[boolArray]
y = y[boolArray]
bern = bern[boolArray]

scat = plt.scatter( x, y, c=bern, s=0.5, vmin = -bern_limit, vmax = bern_limit, cmap='jet' )
halfwidth = bern_plotwidth/2.
plt.axis([ -halfwidth, halfwidth, -halfwidth, halfwidth ])
cb = plt.colorbar()
cb.set_label('Bernoulli Constant', fontsize=25 )

plt.xticks( fontsize=20)
plt.yticks( fontsize=20)
plt.xlabel('x (cm)', fontsize=25 )
plt.ylabel('y (cm)', fontsize=25 )
plt.tight_layout()
# plt.title('Bernoulli Constant ' + cut + ' Time: ' + str(time)[0:5] + ' ' + timelabel )

if do_marks :
	ad = ds.all_data()
	dm_pos = ad[('DarkMatter','Coordinates')]/cl
	core = dm_pos[0][:]
	xcore = core[0]
	ycore = core[1]
	comp = dm_pos[1][:]
	xcomp = comp[0]
	ycomp = comp[1]
	posCM, velCM = getCM(ds, IE=useIE)
	xCM = posCM[0]
	yCM = posCM[1]
	plt.scatter( xcore, ycore, c='k', marker='+' )
	plt.scatter( xcomp, ycomp, c='k', marker='x' )
	plt.scatter( xCM,   yCM,   c='k', marker='*' )
	
bern_saveas = writepath + 'bern_snap_' + simname + '_ds' + str(dataset) + '.png'
fig.savefig(bern_saveas)
print 'bernoulli_snapshot: Saved image ' + bern_saveas
plt.clf()
