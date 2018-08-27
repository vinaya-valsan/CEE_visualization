import numpy as np
import math
from template_config import *
import yt
latex = 0
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from yt import YTQuantity
from berniter import *
from timestuff import *

readpath1 = '/Users/ljprust/data/ce/ohlmann/mm_amr/'
readpath2 = '/Users/ljprust/data/ce/ohlmann/medium2/'
writepath = '/Users/ljprust/data/testplots/'
simname1 = 'mm_amr'
simname2 = 'medium2'
nframes1 = 2
nframes2 = 2
frameskip1 = 1
frameskip2 = 1
startingset1 = 1
startingset2 = 1
dPeriod1 = 3.5e14
dPeriod2 = 3.5e14
useIE1 = 1
useIE2 = 1

readpath = readpath1
simname = simname1
nframes = nframes1
frameskip = frameskip1
startingset = startingset1
dPeriod = dPeriod1
useIE = useIE1
lim = dPeriod / 2. * 1.0001
hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

#########################################################

dotsize = 10

normalizer = 1.0e47 / G

time = np.zeros(nframes)
KEtot = np.zeros(nframes)
enthalpytot = np.zeros(nframes)
internaltot = np.zeros(nframes)
PEtot = np.zeros(nframes)
Etot = np.zeros(nframes)
PEtotGas = np.zeros(nframes)
PEtotDM = np.zeros(nframes)
KEtotGas = np.zeros(nframes)
KEtotDM = np.zeros(nframes)
EtotGas = np.zeros(nframes)
EtotDM = np.zeros(nframes)
fracunbound = np.zeros(nframes)

for i in range(0,nframes):
	
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'unboundcomp: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K = YTQuantity(1.0,'K')

	posCM, velCM = getCM(ds, IE=useIE)

	phiGas = ad[('Gas','Phi')]/cl
	phiDM = ad[('DarkMatter','Phi')]/cl
	vGas = ad[('Gas','Velocities')]/cv
	vDM = ad[('DarkMatter','Velocities')]/cv
	massGas = ad[('Gas','Mass')]/cm
	massDM = ad[('DarkMatter','Mass')]/cm
	temp = ad[('Gas','Temperature')]/K

	vnormGas = np.linalg.norm( vGas - velCM, axis=1 )
	KEGas = 0.5 * np.multiply( np.multiply(vnormGas,vnormGas) , massGas )
	enthalpy = gamma / (gamma-1.0) * R * np.multiply( temp, massGas )
	internal = 3.0/2.0 * R * np.multiply( temp, massGas )
	# internal = np.multiply( ad[('Gas','ie')], massGas )
	# internal = ad[('Gas','ie')]
	PEGas = np.multiply( phiGas, massGas )

	vnormDM = np.linalg.norm( vDM - velCM, axis=1 )
	KEDM = 0.5 * np.multiply( np.multiply(vnormDM,vnormDM) , massDM )
	PEDM = np.multiply( phiDM, massDM )

	if useIE:
		bern_enthalpy = ad[('Gas','ie')]
	else:
		bern_enthalpy = gamma / (gamma-1.0) * R * temp
	bern = 0.5 * np.multiply(vnormGas,vnormGas) + phiGas + bern_enthalpy
	unbound = np.clip(bern, 0.0, 1.0)
	unboundmass = np.multiply( unbound, massGas )
	fracunbound[i] = unboundmass.sum() / ( massGas.sum() + massDM.sum() )

	print 'fracunbound = ' + str(fracunbound[i]) + '\n'

	KEtotGas[i] = KEGas.sum() / normalizer
	enthalpytot[i] = enthalpy.sum() / normalizer
	internaltot[i] = internal.sum() / normalizer
	PEtotGas[i] = PEGas.sum() / normalizer

	KEtotDM[i] = KEDM.sum() / normalizer
	PEtotDM[i] = PEDM.sum() / normalizer

	KEtot[i] = KEtotGas[i] + KEtotDM[i]
	PEtot[i] = PEtotGas[i] + PEtotDM[i]
	Etot[i] = KEtot[i] + PEtot[i] + internaltot[i]
	EtotGas[i] = KEtotGas[i] + PEtotGas[i] + internaltot[i]
	EtotDM[i] = KEtotDM[i] + PEtotDM[i]
	
	time[i], timelabel = getTime(ds, i)

#########################################################

time1 = time
fracunbound1 = fracunbound

readpath = readpath2
simname = simname2
nframes = nframes2
frameskip = frameskip2
startingset = startingset2
dPeriod = dPeriod2
useIE = useIE2
lim = dPeriod / 2. * 1.0001
hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

#########################################################

time = np.zeros(nframes)
KEtot = np.zeros(nframes)
enthalpytot = np.zeros(nframes)
internaltot = np.zeros(nframes)
PEtot = np.zeros(nframes)
Etot = np.zeros(nframes)
PEtotGas = np.zeros(nframes)
PEtotDM = np.zeros(nframes)
KEtotGas = np.zeros(nframes)
KEtotDM = np.zeros(nframes)
EtotGas = np.zeros(nframes)
EtotDM = np.zeros(nframes)
fracunbound = np.zeros(nframes)

for i in range(0,nframes):
	
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'unboundcomp: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K = YTQuantity(1.0,'K')

	posCM, velCM = getCM(ds, IE=useIE)

	phiGas = ad[('Gas','Phi')]/cl
	phiDM = ad[('DarkMatter','Phi')]/cl
	vGas = ad[('Gas','Velocities')]/cv
	vDM = ad[('DarkMatter','Velocities')]/cv
	massGas = ad[('Gas','Mass')]/cm
	massDM = ad[('DarkMatter','Mass')]/cm
	temp = ad[('Gas','Temperature')]/K

	vnormGas = np.linalg.norm( vGas - velCM, axis=1 )
	KEGas = 0.5 * np.multiply( np.multiply(vnormGas,vnormGas) , massGas )
	enthalpy = gamma / (gamma-1.0) * R * np.multiply( temp, massGas )
	internal = 3.0/2.0 * R * np.multiply( temp, massGas )
	# internal = np.multiply( ad[('Gas','ie')], massGas )
	# internal = ad[('Gas','ie')]
	PEGas = np.multiply( phiGas, massGas )

	vnormDM = np.linalg.norm( vDM - velCM, axis=1 )
	KEDM = 0.5 * np.multiply( np.multiply(vnormDM,vnormDM) , massDM )
	PEDM = np.multiply( phiDM, massDM )

	if useIE:
		bern_enthalpy = ad[('Gas','ie')]
	else:
		bern_enthalpy = gamma / (gamma-1.0) * R * temp
	bern = 0.5 * np.multiply(vnormGas,vnormGas) + phiGas + bern_enthalpy
	unbound = np.clip(bern, 0.0, 1.0)
	unboundmass = np.multiply( unbound, massGas )
	fracunbound[i] = unboundmass.sum() / ( massGas.sum() + massDM.sum() )

	print 'fracunbound = ' + str(fracunbound[i]) + '\n'

	KEtotGas[i] = KEGas.sum() / normalizer
	enthalpytot[i] = enthalpy.sum() / normalizer
	internaltot[i] = internal.sum() / normalizer
	PEtotGas[i] = PEGas.sum() / normalizer

	KEtotDM[i] = KEDM.sum() / normalizer
	PEtotDM[i] = PEDM.sum() / normalizer

	KEtot[i] = KEtotGas[i] + KEtotDM[i]
	PEtot[i] = PEtotGas[i] + PEtotDM[i]
	Etot[i] = KEtot[i] + PEtot[i] + internaltot[i]
	EtotGas[i] = KEtotGas[i] + PEtotGas[i] + internaltot[i]
	EtotDM[i] = KEtotDM[i] + PEtotDM[i]
	
	time[i], timelabel = getTime(ds, i)

#####################################################

time2 = time
fracunbound2 = fracunbound

plt.clf()
fig = plt.figure()
plot = plt.scatter( time1, fracunbound1, c='r', s=dotsize, label = simname1 )
plot = plt.scatter( time2, fracunbound2, c='b', s=dotsize, label = simname2 )
plt.legend()
plt.xlabel('Time (' + timelabel + ')', fontsize=25 )
plt.ylabel('Unbound Mass Fraction', fontsize=25 )
plt.xticks( fontsize=20)
plt.yticks( fontsize=20)
plt.tight_layout()
# plt.title('Unbound Mass ' + simname)
saveas = writepath + 'compunbound_' + simname1 + '_' + simname2 + '.pdf'
fig.savefig(saveas)
print 'unboundcomp: Saved plot ' + saveas
plt.clf()

if nframes1 == nframes2 :
	fig2 = plt.figure()
	delta = fracunbound2 - fracunbound1
	plot = plt.scatter( time1, delta, s=dotsize )
	plt.xlabel('Time (' + timelabel + ')', fontsize=25 )
	plt.ylabel('Unbound Delta', fontsize=25 )
	plt.xticks( fontsize=20)
	plt.yticks( fontsize=20)
	plt.tight_layout()
	# plt.title('Unbound Mass ' + simname)
	saveas = writepath + 'deltaunbound_' + simname1 + '_' + simname2 + '.pdf'
	fig2.savefig(saveas)
	print 'unboundcomp: Saved plot ' + saveas
	plt.clf()
