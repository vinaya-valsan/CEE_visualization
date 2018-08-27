import numpy as np
import math
from template_config import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from yt import YTQuantity
from berniter import *
from timestuff import *

from config.test_config import *

bern_plotwidth = 4.0e13

lim = dPeriod / 2. * 1.0001
hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

userho = 0

time = np.zeros(nframes)

num = 1000000 + startingset
numstr = str(num)
cut = numstr[1:7]

ts = yt.load(readpath + outprefix + cut, bounding_box = hbox )

cl = ts.arr(1.0, 'code_length')
cm = ts.arr(1.0, 'code_mass')
cv = ts.arr(1.0, 'code_velocity')
K = YTQuantity(1.0,'K')

fig = plt.figure(figsize=(10,8))

def animate(i):
	plt.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'bernoulli: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()
	time[i], timelabel = getTime(ds, i)

	pos = ad[('Gas','Coordinates')]/cl
	x = pos[:,0]
	y = pos[:,1]
	z = pos[:,2]
	phi = ad[('Gas','Phi')]/cl

	boolArray = np.absolute(z) < dPeriod * 0.5 * bernslice
	x = x[boolArray]
	y = y[boolArray]
	phi = phi[boolArray]
	phi = np.clip( -phi, 1.0, None )
	logphi = np.log10(phi)

	scat = plt.scatter( x, y, c=logphi, s=0.5, vmin=20., cmap='jet' )
	halfwidth = bern_plotwidth/2.
	plt.axis([ -halfwidth, halfwidth, -halfwidth, halfwidth ])
	cb = plt.colorbar()
	cb.set_label('Phi', fontsize=25 )

	plt.xticks( fontsize=20)
	plt.yticks( fontsize=20)
	plt.xlabel('x (cm)', fontsize=25 )
	plt.ylabel('y (cm)', fontsize=25 )
	plt.tight_layout()
	# plt.title('Bernoulli Constant ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

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
		plt.scatter( xCM, yCM, c='k', marker='*' )
	
	return scat
	plt.clf()
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
saveas = writepath + 'phi_' + simname + '.mp4'
anim.save(saveas)
print 'phi: Saved animation ' + saveas
