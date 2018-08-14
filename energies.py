from __main__ import *
import yt
from yt import YTQuantity
import matplotlib
matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from berniter import *
from timestuff import *

energies_dotsize = 10

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
	print 'energies: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K = YTQuantity(1.0,'K')

	posCM, velCM = getCM(ds)

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

#################################################

plt.clf()
plt.plot(time, internaltot, c='r', label='internal')
plt.plot(time, KEtot, c='b', label='KE tot')
plt.plot(time, KEtotDM, c='b', linestyle=':', label='KE DM')
plt.plot(time, KEtotGas, c='b', linestyle='--', label='KE Gas')
plt.plot(time, PEtot, c='g', label='PE tot')
plt.plot(time, PEtotGas, c='g', linestyle='--', label='PE Gas')
plt.plot(time, PEtotDM, c='g', linestyle=':', label='PE DM')
plt.plot(time, Etot, c='k', label='E tot')
plt.plot(time, EtotGas, c='y', linestyle='-', label = 'Gas tot')
plt.plot(time, EtotDM, c='m', linestyle='-', label = 'DM tot')
plt.legend()
	
plt.xlabel('Time (' + timelabel + ')' )
plt.ylabel(r'Energy Budget (ergs $\times 10^{-47}$)')
plt.title(simname + ' Energies')
energies_saveas = writepath + 'energies_' + simname + '.pdf'
plt.savefig(energies_saveas)
print 'energies: Saved figure ' + energies_saveas
plt.clf()

fig = plt.figure()
plot = plt.plot( time, fracunbound )
plt.xlabel('Time (' + timelabel[0] + ')' )
plt.ylabel('Fraction of Mass Unbound')
plt.title('Unbound Mass ' + simname)
saveas = writepath + 'unbound_' + simname + '.pdf'
fig.savefig(saveas)
print 'energies: Saved plot ' + saveas
plt.clf()

########## PAPER MODE ##########################

# timemesa = time
# internaltotmesa = internaltot
# KEtotmesa = KEtot
# PEtotmesa = PEtot
# Etotmesa = Etot
# EtotGasmesa = EtotGas
# EtotDMmesa = EtotDM
# fracunboundmesa = fracunbound

# readpath = readpath_ad
# nframes = nframes_ad

# time = np.zeros(nframes)
# KEtot = np.zeros(nframes)
# enthalpytot = np.zeros(nframes)
# internaltot = np.zeros(nframes)
# PEtot = np.zeros(nframes)
# Etot = np.zeros(nframes)
# PEtotGas = np.zeros(nframes)
# PEtotDM = np.zeros(nframes)
# KEtotGas = np.zeros(nframes)
# KEtotDM = np.zeros(nframes)
# EtotGas = np.zeros(nframes)
# EtotDM = np.zeros(nframes)
# fracunbound = np.zeros(nframes)

# for i in range(0,nframes):
	
# 	num = i*frameskip + 1000000 + startingset
# 	numstr = str(num)
# 	cut = numstr[1:7]
# 	print 'energies: ' + simname + ' Data Set ' + cut
	
# 	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
# 	ad = ds.all_data()

# 	cl = ds.arr(1.0, 'code_length')
# 	cm = ds.arr(1.0, 'code_mass')
# 	cv = ds.arr(1.0, 'code_velocity')
# 	K = YTQuantity(1.0,'K')

# 	posCM, velCM = getCM(ds)

# 	phiGas = ad[('Gas','Phi')]/cl
# 	phiDM = ad[('DarkMatter','Phi')]/cl
# 	vGas = ad[('Gas','Velocities')]/cv
# 	vDM = ad[('DarkMatter','Velocities')]/cv
# 	massGas = ad[('Gas','Mass')]/cm
# 	massDM = ad[('DarkMatter','Mass')]/cm
# 	temp = ad[('Gas','Temperature')]/K

# 	vnormGas = np.linalg.norm( vGas - velCM, axis=1 )
# 	KEGas = 0.5 * np.multiply( np.multiply(vnormGas,vnormGas) , massGas )
# 	enthalpy = gamma / (gamma-1.0) * R * np.multiply( temp, massGas )
# 	internal = 3.0/2.0 * R * np.multiply( temp, massGas )
# 	# internal = np.multiply( ad[('Gas','ie')], massGas )
# 	PEGas = np.multiply( phiGas, massGas )

# 	vnormDM = np.linalg.norm( vDM - velCM, axis=1 )
# 	KEDM = 0.5 * np.multiply( np.multiply(vnormDM,vnormDM) , massDM )
# 	PEDM = np.multiply( phiDM, massDM )

# 	if useIE:
# 		bern_enthalpy = ad[('Gas','ie')]
# 	else:
# 		bern_enthalpy = gamma / (gamma-1.0) * R * temp
# 	bern = 0.5 * np.multiply(vnormGas,vnormGas) + phiGas + bern_enthalpy
# 	unbound = np.clip(bern, 0.0, 1.0)
# 	unboundmass = np.multiply( unbound, massGas )
# 	fracunbound[i] = unboundmass.sum() / ( massGas.sum() + massDM.sum() )

# 	KEtotGas[i] = KEGas.sum() / normalizer
# 	enthalpytot[i] = enthalpy.sum() / normalizer
# 	internaltot[i] = internal.sum() / normalizer
# 	PEtotGas[i] = PEGas.sum() / normalizer

# 	KEtotDM[i] = KEDM.sum() / normalizer
# 	PEtotDM[i] = PEDM.sum() / normalizer

# 	KEtot[i] = KEtotGas[i] + KEtotDM[i]
# 	PEtot[i] = PEtotGas[i] + PEtotDM[i]
# 	Etot[i] = KEtot[i] + PEtot[i] + internaltot[i]
# 	EtotGas[i] = KEtotGas[i] + PEtotGas[i] + internaltot[i]
# 	EtotDM[i] = KEtotDM[i] + PEtotDM[i]
	
# 	time[i], timelabel = getTime(ds, i)

# timead = time
# internaltotad = internaltot
# KEtotad = KEtot
# PEtotad = PEtot
# Etotad = Etot
# EtotGasad = EtotGas
# EtotDMad = EtotDM
# fracunboundad = fracunbound

# plt.clf()
# plt.plot(timemesa, internaltotmesa, c='r', label='Internal', lw=2)
# plt.plot(timemesa, KEtotmesa, c='b', label='Total Kinetic', lw=2)
# plt.plot(timemesa, PEtotmesa, c='g', label='Total Potential', lw=2)
# plt.plot(timemesa, Etotmesa, c='k', label='Total Energy', lw=2)
# plt.plot(timemesa, EtotGasmesa, c='y', label = 'Total Gas', lw=2)
# plt.plot(timemesa, EtotDMmesa, c='m', label = 'Total DM', lw=2)
# plt.plot(timead, internaltotad, c='r', linestyle='--', lw=2)
# plt.plot(timead, KEtotad, c='b', linestyle='--', lw=2)
# plt.plot(timead, PEtotad, c='g', linestyle='--', lw=2)
# plt.plot(timead, Etotad, c='k', linestyle='--', lw=2)
# plt.plot(timead, EtotGasad, c='y', linestyle='--', lw=2)
# plt.plot(timead, EtotDMad, c='m', linestyle='--', lw=2)
# plt.legend()

# plt.xlabel('Time (' + timelabel + ')' )
# plt.ylabel(r'Energy Budget (ergs \times 10^{-47})')
# plt.xticks( fontsize=20)
# plt.yticks( fontsize=20)
# # plt.title(simname + ' Energies')
# energies_saveas = writepath + 'energies_' + simname + '.pdf'
# plt.savefig(energies_saveas)
# print 'energies: Saved figure ' + energies_saveas
# plt.clf()

# fig = plt.figure()
# plot = plt.plot( timemesa, fracunboundmesa, c='r', label = 'MESA' )
# plot = plt.plot( timead, fracunboundad, c='b', label = 'Adiabatic' )
# plt.legend()
# plt.xlabel('Time (' + timelabel + ')' )
# plt.ylabel('Unbound Mass Fraction')
# # plt.title('Unbound Mass ' + simname)
# saveas = writepath + 'unbound_' + simname + '.pdf'
# fig.savefig(saveas)
# print 'energies: Saved plot ' + saveas
# plt.clf()
