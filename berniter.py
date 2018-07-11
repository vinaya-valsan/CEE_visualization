from __main__ import *
import yt
from yt import YTQuantity

def getCM( ds, threshold=0.001, maxiter=100 ) :

	gamma = 5.0/3.0
	G = 6.674e-8
	R = 8.314e7 / G
	Rsun = 7.0e10
	Msun = 2.0e33

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
	npcles = len(gasmass)
	posPrim = posDM[0,:]
	posComp = posDM[1,:]
	vPrim = velDM[0,:]
	vComp = velDM[1,:]
	mPrim = massDM[0]
	mComp = massDM[1]

	PE = ad[('Gas','Phi')]/cl
	enthalpy = gamma / (gamma-1.0) * R * ad[('Gas','Temperature')] / K
	vCM = np.zeros(3)

	CMerr = 1.
	i = 0
	didbreak = 0
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
		print 'nbound = ' + str(nbound)
		
		boundmass = np.multiply( bound, gasmass )
		boundmasstot = np.sum(boundmass)
		print 'bound mass = ' + str( boundmasstot/Msun )
		boundFM = np.zeros( (npcles, 3 ) )
		boundFM[:,0] = np.multiply( boundmass, gaspos[:,0] )
		boundFM[:,1] = np.multiply( boundmass, gaspos[:,1] )
		boundFM[:,2] = np.multiply( boundmass, gaspos[:,2] )
		boundFMv = np.zeros( (npcles, 3 ) )
		boundFMv[:,0] = np.multiply( boundmass, vRelx )
		boundFMv[:,1] = np.multiply( boundmass, vRely )
		boundFMv[:,2] = np.multiply( boundmass, vRelz )
		gasCM = np.sum(boundFM, axis=0) / boundmasstot
		gasCMv = np.sum(boundFMv, axis=0) / boundmasstot
		posCM = ( posPrim * mPrim + posComp * mComp + gasCM * boundmasstot ) \
			 / ( mPrim + mComp + boundmasstot )
		velCM = ( vPrim * mPrim + vComp * mComp + gasCMv * boundmasstot ) \
			 / ( mPrim + mComp + boundmasstot )
		velCMnorm = np.linalg.norm( velCM )
		vCMnorm = np.linalg.norm( vCM )

		CMerr = np.absolute( (velCMnorm - vCMnorm) / velCMnorm )
		print 'error = ' + str(CMerr)

		vCM = velCM
		i = i+1

		print 'CM velocity = ' + str( np.linalg.norm(vCM) * cv.in_units('km/s') )

	print '\nConverged after {0} iterations with {1} percent error\n'.format(i, CMerr*100.)

	return posCM, vCM

