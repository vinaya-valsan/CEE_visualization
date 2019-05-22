import math
import numpy as np
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
        self.massDM = ad[('DarkMatter','Mass')]/self.cm
        self.softLen = ad[('DarkMatter','Epsilon')]/self.cl
        self.temp = ad[('Gas','Temperature')]/self.K
        self.posDM = ad[('DarkMatter','Coordinates')]/self.cl
        self.dens = ad[('Gas','density')]/self.cm * self.cl * self.cl * self.cl
        self.Hdens = ad[('Gas','H_nuclei_density')]/self.cm3
        try:
            self.ie = ad[('Gas','ie')] * self.massGas
        except:
            self.ie = 1.0 / (gamma-1.0) * R * self.temp * self.massGas

    def cutVacuum(self):
        rhoExt = 1.0e-13
        densThresh = 100.0 * rhoExt
        notVacuum = (self.dens > densThresh)
        self.numVacPcles = len(self.dens) - notVacuum.sum()

        self.phiGas = self.phiGas[notVacuum]
        self.posGas = self.posGas[notVacuum,:]
        self.vGas = self.vGas[notVacuum,:]
        self.massGas = self.massGas[notVacuum]
        self.temp = self.temp[notVacuum]
        self.dens = self.dens[notVacuum]
        self.Hdens = self.Hdens[notVacuum]
        self.ie = self.ie[notVacuum]

    def getIE(self):
        self.ietot = self.ie.sum()
        self.ie_ideal = 1.0 / (gamma-1.0) * R * self.temp * self.massGas
        self.ie_idealtot = self.ie_ideal.sum()

    def getPE(self):
        self.gasPE = np.multiply( self.phiGas, self.massGas )
        self.gasPEtot_init = self.gasPE.sum()
        self.DMPE = np.multiply( self.phiDM, self.massDM )
        self.DMPEtot_init = self.DMPE.sum()

    def getKE(self):
        self.gasKE = 0.5 * self.massGas * np.linalg.norm(self.vGas-self.vCM, axis=1) * np.linalg.norm(self.vGas-self.vCM, axis=1)
        self.gasKEtot = self.gasKE.sum()
        self.DMKE = 0.5 * self.massDM * np.linalg.norm(self.vDM-self.vCM, axis=1) * np.linalg.norm(self.vDM-self.vCM, axis=1)
        self.DMKEtot = self.DMKE.sum()

    def findCMDM(self):
        vCMDM = ( self.mPrim * self.vPrim + self.mComp * self.vComp ) / (self.mPrim+self.mComp)
        self.velCMDMnorm = np.linalg.norm(vCMDM, axis=0) * self.cv.in_units('km/s')

    def findCM(self, threshold=0.0001, smoothing=5, maxiter=1000 ):
        xGas = self.posGas[:,0]
        yGas = self.posGas[:,1]
        zGas = self.posGas[:,2]
        vxGas = self.vGas[:,0]
        vyGas = self.vGas[:,1]
        vzGas = self.vGas[:,2]
        self.posPrim = self.posDM[0,:]
        self.posComp = self.posDM[1,:]
        self.vPrim = self.vDM[0,:]
        self.vComp = self.vDM[1,:]
        self.mPrim = self.massDM[0]
        self.mComp = self.massDM[1]
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
            KE = 0.5*np.multiply(vRelNorm,vRelNorm) * self.massGas
            bern = self.gasPE + KE + self.ie
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
            posCM = ( self.posPrim * self.mPrim + self.posComp * self.mComp + gasCM * boundmasstot ) \
            	 / ( self.mPrim + self.mComp + boundmasstot )
            velCM = ( self.vPrim * self.mPrim + self.vComp * self.mComp + gasCMv * boundmasstot ) \
            	 / ( self.mPrim + self.mComp + boundmasstot )
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
        # print(vCM)

        self.velCMnorm = np.linalg.norm(self.vCM, axis=0) * self.cv.in_units('km/s')

    def getTime(self):

        from yt import YTQuantity
        ct = self.ds.arr( math.sqrt(G), 'code_time' )
        time = self.ds.current_time / ct
        sec = YTQuantity(1.0,'s')
        self.time = time * sec.in_units('day')

    def getEjecta(self):

        self.massGasTot = self.massGas.sum()
        bern = self.gasKE + self.gasPE + self.ie
        bern_i = self.gasKE + self.gasPE + self.ie_ideal
        bern_noIe = self.gasKE + self.gasPE
        self.unbound = np.clip(bern, 0.0, 1.0)
        self.unboundBool = np.array( self.unbound == 1.0, dtype=bool )
        self.boundBool = np.logical_not(self.unboundBool)
        unbound_i = np.clip(bern_i, 0.0, 1.0)
        unbound_noIe = np.clip(bern_noIe, 0.0, 1.0)
        unboundmass = np.multiply( self.unbound, self.massGas )
        unboundmass_i = np.multiply( unbound_i, self.massGas )
        unboundmass_noIe = np.multiply( unbound_noIe, self.massGas )
        self.fracunbound = unboundmass.sum() / ( self.massGasTot + self.massDM.sum() )
        self.fracunbound_i = unboundmass_i.sum() / ( self.massGasTot + self.massDM.sum() )
        self.fracunbound_noIe = unboundmass_noIe.sum() / ( self.massGasTot + self.massDM.sum() )
        self.ejeceff = unboundmass.sum() / self.massGasTot
        self.ejeceff_i = unboundmass_i.sum() / self.massGasTot
        self.ejeceff_noIe = unboundmass_noIe.sum() / self.massGasTot

    def getBoundUnbound(self):

        self.gasKEunbound = self.gasKE[self.unboundBool]
        self.gasKEbound = self.gasKE[self.boundBool]
        self.gasIEunbound = self.ie[self.unboundBool]
        self.gasIEbound = self.ie[self.boundBool]
        self.gasPEunbound = self.gasPE[self.unboundBool]
        self.gasPEbound = self.gasPE[self.boundBool]

        self.gasKEunboundTot = self.gasKEunbound.sum()
        self.gasKEboundTot = self.gasKEbound.sum()
        self.gasIEunboundTot = self.gasIEunbound.sum()
        self.gasIEboundTot = self.gasIEbound.sum()
        self.gasPEunboundTot_init = self.gasPEunbound.sum()
        self.gasPEboundTot_init = self.gasPEbound.sum()

        self.PECoreGasUnboundCore = self.PECoreGas(self.softLen[0],self.unboundBool,self.posPrim,self.mPrim)
        self.PECoreGasBoundCore = self.PECoreGas(self.softLen[0],self.boundBool,self.posPrim,self.mPrim)
        self.PECoreGasUnboundComp = self.PECoreGas(self.softLen[1],self.unboundBool,self.posComp,self.mComp)
        self.PECoreGasBoundComp = self.PECoreGas(self.softLen[1],self.boundBool,self.posComp,self.mComp)

    def PEstuff(self):

        self.PECoreCore = -self.massDM[0] * self.massDM[1] / self.rScalar

        self.PECoreGasUnbound = self.PECoreGasUnboundCore + self.PECoreGasUnboundComp
        self.PECoreGasBound = self.PECoreGasBoundCore + self.PECoreGasBoundComp
        self.PECoreGas = self.PECoreGasUnbound + self.PECoreGasBound

        self.PEGasGasUnbound = ( self.gasPEunboundTot_init - self.PECoreGasUnbound ) / 2.0
        self.PEGasGasBound = ( self.gasPEboundTot_init - self.PECoreGasBound ) / 2.0
        self.PEGasGas = ( self.gasPEtot_init - self.PECoreGas ) / 2.0

    def PECoreGas(self,h,boolArray,DMpos,DMmass):

        massGasCut = self.massGas[boolArray]
        posGasCut = self.posGas[boolArray,:] - DMpos
        radius = np.linalg.norm(posGasCut,axis=1)
        u = radius / h
        boolArray1 = u < 0.5
        boolArray2 = u < 1.0
        boolArrayIn = np.array( boolArray1, dtype=bool )
        boolArrayMid = np.logical_and( boolArray2, np.logical_not(boolArray1) )
        boolArrayOut = np.logical_not( boolArray2 )

        radiusIn = radius[boolArrayIn]
        radiusMid = radius[boolArrayMid]
        radiusOut = radius[boolArrayOut]
        massIn = massGasCut[boolArrayIn]
        massMid = massGasCut[boolArrayMid]
        massOut = massGasCut[boolArrayOut]
        uIn = u[boolArrayIn]
        uMid = u[boolArrayMid]
        uOut = u[boolArrayOut]

        phiIn = -1.0/radiusIn*( 14./5.*uIn-16./3.*np.power(uIn,3.)+48./5.*np.power(uIn,5.)-32./5.*np.power(uIn,6.) )
        phiMid = -1.0/radiusMid*( -1./15.+16./5.*uMid-32./3.*np.power(uMid,3.)+16.*np.power(uMid,4.)-48./5.*np.power(uMid,5.)+32./15.*np.power(uMid,6.) )
        phiOut = -1.0/radiusOut

        PEIn = phiIn * massIn
        PEMid = phiMid * massMid
        PEOut = phiOut * massOut

        PEcoregas = ( PEIn.sum() + PEMid.sum() + PEOut.sum() ) * DMmass
        return PEcoregas

    def getOrbit(self):

        r = self.posComp - self.posPrim
        self.rScalar = np.linalg.norm(r)
        self.sep = self.rScalar / Rsun

    def doEverything(self):

        self.readData()
        # self.cutVacuum()
        self.getIE()
        self.getPE()
        self.findCM()
        self.findCMDM()
        self.getKE()
        self.getTime()
        self.getEjecta()
        self.getOrbit()
        self.getBoundUnbound()
        self.PEstuff()
