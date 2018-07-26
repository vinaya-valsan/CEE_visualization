from __main__ import *
import yt
from yt import YTQuantity
import matplotlib.pyplot as plt
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
	PEGas = np.multiply( phiGas, massGas )

	vnormDM = np.linalg.norm( vDM - velCM, axis=1 )
	KEDM = 0.5 * np.multiply( np.multiply(vnormDM,vnormDM) , massDM )
	PEDM = np.multiply( phiDM, massDM )

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

plt.clf()
plt.plot(time, internaltot, c='r', label='internal')
plt.plot(time, KEtot, c='b', label='KE_tot')
plt.plot(time, KEtotDM, c='b', linestyle=':', label='KE_DM')
plt.plot(time, KEtotGas, c='b', linestyle='--', label='KE_Gas')
plt.plot(time, PEtot, c='g', label='PE_tot')
plt.plot(time, PEtotGas, c='g', linestyle='--', label='PE_Gas')
plt.plot(time, PEtotDM, c='g', linestyle=':', label='PE_DM')
plt.plot(time, Etot, c='k', label='E_tot')
plt.plot(time, EtotGas, c='y', linestyle='-', label = 'Gas_tot')
plt.plot(time, EtotDM, c='m', linestyle='-', label = 'DM_tot')
plt.legend()
	
plt.xlabel('Time (' + timelabel + ')' )
plt.ylabel('Energy Budget (ergs * 10^-47)')
plt.title(simname + ' Energies')
energies_saveas = writepath + 'energies_' + simname + '.pdf'
plt.savefig(energies_saveas)
print 'energies: Saved figure ' + energies_saveas
plt.clf()
