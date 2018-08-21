from __main__ import *
import yt
from yt import YTQuantity

def getCM( ds, threshold=0.0001, smoothing=5, maxiter=1000 ) :

	ad = ds.all_data()

	cl = ds.arr(1.0, 'code_length')
	cm = ds.arr(1.0, 'code_mass')
	cv = ds.arr(1.0, 'code_velocity')
	K = YTQuantity(1.0,'K')
	kmps = YTQuantity(1.0,'km/s')

	posDM = ad[('DarkMatter','Coordinates')]/cl
	velDM = ad[('DarkMatter','Velocities')]/cv
	massDM = ad[('DarkMatter','Mass')]/cm
	gasmass = ad[('Gas','Mass')]/cm
	gaspos = ad[('Gas','Coordinates')]/cl
	v = ad[('Gas','Velocities')]/cv
	vx = v[:,0]
	vy = v[:,1]
	vz = v[:,2]
	npcles = len(gasmass)
	posPrim = posDM[0,:]
	posComp = posDM[1,:]
	vPrim = velDM[0,:]
	vComp = velDM[1,:]
	mPrim = massDM[0]
	mComp = massDM[1]

	PE = ad[('Gas','Phi')]/cl
	
	if useIE:
		enthalpy = ad[('Gas','ie')]
	else:
		enthalpy = gamma / (gamma-1.0) * R * ad[('Gas','Temperature')] / K

	vCM = np.zeros(3)
	vCheck = np.zeros(maxiter)

	CMerr = 1.
	i = 0
	while CMerr > threshold :
		print 'iteration ' + str(i)

		if i == maxiter :
			print 'Terminating: hit max iterations (' + str(i) + ')'
			import sys
			sys.exit(0)

		vRel = v - vCM
		vRelx = vRel[:,0]
		vRely = vRel[:,1]
		vRelz = vRel[:,2]
		vRelNorm = np.linalg.norm( vRel, axis=1 )
		KE = 0.5*np.multiply(vRelNorm,vRelNorm)
		bern = PE + KE + enthalpy

		bound = np.clip(-bern, 0.0, 1.0)
		nbound = np.sum(bound)
		# print 'nbound = ' + str(nbound)
		
		boundmass = np.multiply( bound, gasmass )
		boundmasstot = np.sum(boundmass)
		# print 'bound mass = ' + str( boundmasstot/Msun )
		boundFM = np.zeros( (npcles, 3 ) )
		boundFM[:,0] = np.multiply( boundmass, gaspos[:,0] )
		boundFM[:,1] = np.multiply( boundmass, gaspos[:,1] )
		boundFM[:,2] = np.multiply( boundmass, gaspos[:,2] )
		boundFMv = np.zeros( (npcles, 3 ) )
		boundFMv[:,0] = np.multiply( boundmass, vx )
		boundFMv[:,1] = np.multiply( boundmass, vy )
		boundFMv[:,2] = np.multiply( boundmass, vz )
		gasCM = np.sum(boundFM, axis=0) / boundmasstot
		gasCMv = np.sum(boundFMv, axis=0) / boundmasstot
		posCM = ( posPrim * mPrim + posComp * mComp + gasCM * boundmasstot ) \
			 / ( mPrim + mComp + boundmasstot )
		velCM = ( vPrim * mPrim + vComp * mComp + gasCMv * boundmasstot ) \
			 / ( mPrim + mComp + boundmasstot )
		velCMnorm = np.linalg.norm( velCM )
		# vCMnorm = np.linalg.norm( vCM )

		vCheck[i] = velCMnorm
		if i > smoothing-1 :
			vCut = vCheck[i-smoothing:i]
			CMerr = np.absolute( (vCut.max() - vCut.min()) / vCut.min() )
			print 'error = ' + str(CMerr)

		vCM = velCM # new one becomes old one
		i = i+1

		print 'CM velocity = ' + str( np.linalg.norm(vCM) * cv.in_units('km/s') )

	print '\ngetCM: Converged after {0} iterations with {1} percent error\n'.format(i, CMerr*100.)

	return posCM, vCM

