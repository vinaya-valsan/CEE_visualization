import math
gamma = 5.0/3.0
G = 6.674e-8
R = 8.314e7 / G
Rsun = 7.0e10
Msun = 2.0e33
k = 1.381e-16 / G
h = 6.626e-27 / math.sqrt(G)
mpart = 1.6606e-24

class Dataset(object):

    def __init__(self, name, hbox ):
        import yt
        from yt import YTQuantity
        self.ds = yt.load( name, bounding_box = hbox )
        self.cl = self.ds.arr(1.0, 'code_length')
        self.cm = self.ds.arr(1.0, 'code_mass')
        self.cv = self.ds.arr(1.0, 'code_velocity')
        self.K = YTQuantity(1.0,'K')
        self.cm3 = self.ds.arr(1.0, 'cm**(-3)')

    def readData(self):
        ad = self.ds.all_data()
        self.phiGas = ad[('Gas','Phi')]/self.cl
        self.phiDM = ad[('DarkMatter','Phi')]/self.cl
        self.posGas = ad[('Gas','Coordinates')]/self.cl
        self.vGas = ad[('Gas','Velocities')]/self.cv
        self.vDM = ad[('DarkMatter','Velocities')]/self.cv
        self.massGas = ad[('Gas','Mass')]/self.cm
        self.massGasTot = self.massGas.sum()
        self.massDM = ad[('DarkMatter','Mass')]/self.cm
        self.temp = ad[('Gas','Temperature')]/self.K
        self.posDM = ad[('DarkMatter','Coordinates')]/self.cl
        self.Hdens = ad[('Gas','H_nuclei_density')]/self.cm3
        try:
        	self.ie = ad[('Gas','ie')] * self.massGas
            self.ietot = self.ie.sum()
        except:
            import numpy as np
            self.ie = np.zeros( len(self.temp) )
            self.ietot = 0.0
        self.ie_ideal = 1.0 / (gamma-1.0) * R * self.temp * self.massGas
        self.ie_idealtot = self.ie_ideal.sum()

    def getEnergies(self):

        import numpy as np
        self.gasKE = 0.5 * self.massGas * np.linalg.norm(self.vGas-self.vCM, axis=1) * np.linalg.norm(self.vGas-self.vCM, axis=1)
        self.gasKEtot = self.gasKE.sum()
        self.gasPE = np.multiply( self.phiGas, self.massGas )
        self.gasPEtot = self.gasPE.sum()
        self.DMKE = 0.5 * self.massDM * np.linalg.norm(self.vDM-self.vCM, axis=1) * np.linalg.norm(self.vDM-self.vCM, axis=1)
        self.DMKEtot = self.DMKE.sum()
        self.DMPE = np.multiply( self.phiDM, self.massDM )
        self.DMPEtot = self.DMPE.sum()

    def findCM(self, threshold=0.0001, smoothing=5, maxiter=1000 ):
        import numpy as np
        xGas = self.posGas[:,0]
        yGas = self.posGas[:,1]
        zGas = self.posGas[:,2]
        vxGas = self.vGas[:,0]
        vyGas = self.vGas[:,1]
        vzGas = self.vGas[:,2]
        posPrim = self.posDM[0,:]
        posComp = self.posDM[1,:]
        vPrim = self.vDM[0,:]
        vComp = self.vDM[1,:]
        mPrim = self.massDM[0]
        mComp = self.massDM[1]
        npcles = len(xGas)
        vCM = np.zeros(3)
        vCheck = np.zeros(maxiter)

        CMerr = 1.
        i = 0
        while CMerr > threshold :

            if i == maxiter :
            	print('Terminating: hit max iterations (' + str(i) + ')')
            	import sys
            	sys.exit(0)

            vRel = self.vGas - vCM
            vRelx = vRel[:,0]
            vRely = vRel[:,1]
            vRelz = vRel[:,2]
            vRelNorm = np.linalg.norm( vRel, axis=1 )
            KE = 0.5*np.multiply(vRelNorm,vRelNorm)
            bern = self.phiGas + KE + self.ie
            bound = np.clip(-bern, 0.0, 1.0)
            nbound = np.sum(bound)
            boundmass = np.multiply( bound, self.massGas )
            boundmasstot = np.sum(boundmass)
            boundFM = np.zeros( (npcles, 3 ) )
            boundFM[:,0] = np.multiply( boundmass, xGas )
            boundFM[:,1] = np.multiply( boundmass, yGas )
            boundFM[:,2] = np.multiply( boundmass, zGas )
            boundFMv = np.zeros( (npcles, 3 ) )
            boundFMv[:,0] = np.multiply( boundmass, vxGas )
            boundFMv[:,1] = np.multiply( boundmass, vyGas )
            boundFMv[:,2] = np.multiply( boundmass, vzGas )
            gasCM = np.sum(boundFM, axis=0) / boundmasstot
            gasCMv = np.sum(boundFMv, axis=0) / boundmasstot
            posCM = ( posPrim * mPrim + posComp * mComp + gasCM * boundmasstot ) \
            	 / ( mPrim + mComp + boundmasstot )
            velCM = ( vPrim * mPrim + vComp * mComp + gasCMv * boundmasstot ) \
            	 / ( mPrim + mComp + boundmasstot )
            velCMnorm = np.linalg.norm( velCM )

            vCheck[i] = velCMnorm
            if i > smoothing-1 :
            	vCut = vCheck[i-smoothing:i]
            	CMerr = np.absolute( (vCut.max() - vCut.min()) / vCut.min() )

            vCM = velCM
            i = i+1

        # print('getCM: Converged after {0} iterations with {1} percent error'.format(i, CMerr*100.))
        self.posCM = posCM
        self.vCM = vCM

    def getTime(self):

        from yt import YTQuantity
        ct = self.ds.arr( math.sqrt(G), 'code_time' )
        time = self.ds.current_time / ct
        sec = YTQuantity(1.0,'s')
        self.time = time * sec.in_units('day')

    def getUnbound(self):

        import numpy as np
        bern = self.gasKE + self.gasPE + self.ie
        bern_i = self.gasKE + self.gasPE + self.ie_ideal
        unbound = np.clip(bern, 0.0, 1.0)
        unbound_i = np.clip(bern_i, 0.0, 1.0)
        unboundmass = np.multiply( unbound, self.massGas )
        unboundmass_i = np.multiply( unbound_i, self.massGas )
        self.fracunbound = unboundmass.sum() / ( self.massGas.sum() + self.massDM.sum() )
        self.fracunbound_i = unboundmass_i.sum() / ( self.massGas.sum() + self.massDM.sum() )
        self.ejeceff = unboundmass.sum() / self.massGas.sum()
        self.ejeceff_i = unboundmass_i.sum() / self.massGas.sum()

    def getOrbit(self):

        import numpy as np
        posPrim = self.posDM[0,:]
        posComp = self.posDM[1,:]
        r = posComp - posPrim
        rScalar = np.linalg.norm(r)
        self.sep = rScalar / Rsun
        self.velCMnorm = np.linalg.norm(self.vCM, axis=0) * self.cv.in_units('km/s')
