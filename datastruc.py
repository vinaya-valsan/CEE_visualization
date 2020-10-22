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

movingBC = True

def changehTest(name1, name2) :

    from crawler import parseParams
    parseParams()
    from params import dPeriod
    lim = dPeriod / 2. * 1.0001
    hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

    dataset1 = Dataset(name1, hbox)
    dataset2 = Dataset(name2, hbox)

    dataset1.doEverything()
    dataset2.doEverything()

    cgup1 = dataset1.PECoreGasUnboundCore
    cgbp1 = dataset1.PECoreGasBoundCore
    cguc1 = dataset1.PECoreGasUnboundComp
    cgbc1 = dataset1.PECoreGasBoundComp

    cgup2 = dataset2.PECoreGasUnboundCore
    cgbp2 = dataset2.PECoreGasBoundCore
    cguc2 = dataset2.PECoreGasUnboundComp
    cgbc2 = dataset2.PECoreGasBoundComp

    cgp1 = cgup1 + cgbp1
    cgc1 = cguc1 + cgbc1
    cgp2 = cgup2 + cgbp2
    cgc2 = cguc2 + cgbc2

    h1 = dataset1.softLen
    h2 = dataset2.softLen
    h1prim = h1[0]
    h1comp = h1[1]
    h2prim = h2[0]
    h2comp = h2[1]

    cgp_diff = abs( ( cgp1 - cgp2 ) / cgp1 )
    cgc_diff = abs( ( cgc1 - cgc2 ) / cgc1 )

    print('softening lengths: --------')
    print('before:', h1prim, h1comp)
    print('after:', h2prim, h2comp)
    print('core-gas PE comparions: --------')
    print('primary:', cgp1, cgp2, cgp_diff)
    print('comp:', cgc1, cgc2, cgc_diff)

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

        self.name = name
        namelength = len(name)
        self.setnum = float(name[namelength-6:namelength])

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

        self.reflectiveCount = 0.
        self.edgeCount       = 0.
        self.mirrorLeft      = 0.
        self.mirrorRight     = 0.
        self.mirrorRadius    = 0.
        self.mirrorCenter    = np.array([0., 0., 0.])
        self.mirrorMass      = 0.
        self.mirrorVel       = np.array([0., 0., 0.])
        self.mirrorForce     = np.array([0., 0., 0.])
        self.mirrorGrav      = np.array([0., 0., 0.])

        if movingBC :
            mirrorFile = self.name[0:len(self.name)-6] + 'bc.' + self.name[len(self.name)-6:len(self.name)]
            mirrorData = np.loadtxt(mirrorFile)

            self.reflectiveCount = mirrorData[0]
            self.edgeCount       = mirrorData[1]
            self.mirrorLeft      = mirrorData[2]
            self.mirrorRight     = mirrorData[3]
            self.mirrorRadius    = mirrorData[4]
            self.mirrorCenter    = np.array([mirrorData[5], mirrorData[6], mirrorData[7]])
            self.mirrorMass      = mirrorData[8]
            self.mirrorVel       = np.array([mirrorData[9], mirrorData[10], mirrorData[11]])
            self.mirrorForce     = np.array([mirrorData[12], mirrorData[13], mirrorData[14]])
            self.mirrorGrav      = np.array([mirrorData[15], mirrorData[16], mirrorData[17]])

    def addMirror(self):
        radFromMirror = np.linalg.norm( self.posGas - self.mirrorCenter, axis=1 )
        outMirror = radFromMirror > self.mirrorRadius
        inMirror  = radFromMirror < self.mirrorRadius

        mirrorPhi = np.mean(self.phiGas[inMirror])

        self.phiGas = self.phiGas[outMirror]
        self.posGas = self.posGas[outMirror,:]
        self.vGas = self.vGas[outMirror,:]
        self.massGas = self.massGas[outMirror]
        self.temp = self.temp[outMirror]
        self.dens = self.dens[outMirror]
        self.Hdens = self.Hdens[outMirror]
        self.ie = self.ie[outMirror]

        newposDM = np.zeros((2,3))
        newposDM[0,:] = self.posDM
        newposDM[1,:] = self.mirrorCenter
        self.posDM = newposDM

        newvDM = np.zeros((2,3))
        newvDM[0,:] = self.vDM
        newvDM[1,:] = self.mirrorVel
        self.vDM = newvDM

        newphiDM = np.zeros(2)
        newphiDM[0] = self.phiDM
        newphiDM[1] = mirrorPhi
        self.phiDM = newphiDM

        newmassDM = np.zeros(2)
        newmassDM[0] = self.massDM
        newmassDM[1] = self.mirrorMass
        self.massDM = newmassDM

        newsoftLen = np.zeros(2)
        newsoftLen[0] = self.softLen
        newsoftLen[1] = self.mirrorRadius / 2.
        self.softLen = newsoftLen

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

        self.gasKEraw = 0.5 * self.massGas * np.linalg.norm(self.vGas, axis=1) * np.linalg.norm(self.vGas, axis=1)
        self.gasKErawtot = self.gasKEraw.sum()
        self.DMKEraw = 0.5 * self.massDM * np.linalg.norm(self.vDM, axis=1) * np.linalg.norm(self.vDM, axis=1)
        self.DMKErawtot = self.DMKEraw.sum()

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

    def getMomentum(self):

        coreP = self.mPrim * self.vPrim
        compP = self.mComp * self.vComp
        coreL = self.mPrim * np.cross(self.posPrim, self.vPrim)
        compL = self.mComp * np.cross(self.posComp, self.vComp)

        self.corePx = coreP[0]
        self.corePy = coreP[1]
        self.corePz = coreP[2]
        self.compPx = compP[0]
        self.compPy = compP[1]
        self.compPz = compP[2]
        self.coreLx = coreL[0]
        self.coreLy = coreL[1]
        self.coreLz = coreL[2]
        self.compLx = compL[0]
        self.compLy = compL[1]
        self.compLz = compL[2]

        gasP = 0. * self.vGas
        gasP[:,0] = self.massGas * self.vGas[:,0]
        gasP[:,1] = self.massGas * self.vGas[:,1]
        gasP[:,2] = self.massGas * self.vGas[:,2]
        # gasP = np.multiply(self.massGas, self.vGas)
        gasPbound = gasP[self.boundBool,:]
        gasPunbound = gasP[self.unboundBool,:]
        gasPxbound = gasPbound[:,0]
        gasPybound = gasPbound[:,1]
        gasPzbound = gasPbound[:,2]
        gasPxunbound = gasPunbound[:,0]
        gasPyunbound = gasPunbound[:,1]
        gasPzunbound = gasPunbound[:,2]
        self.gasPbound_tot = (np.linalg.norm(gasPbound, axis=1)).sum()
        self.gasPunbound_tot = (np.linalg.norm(gasPunbound, axis=1)).sum()
        self.gasPxbound_tot = gasPxbound.sum()
        self.gasPybound_tot = gasPybound.sum()
        self.gasPzbound_tot = gasPzbound.sum()
        self.gasPxunbound_tot = gasPxunbound.sum()
        self.gasPyunbound_tot = gasPyunbound.sum()
        self.gasPzunbound_tot = gasPzunbound.sum()

        gasL = 0. * self.vGas
        cross = np.cross(self.posGas, self.vGas)
        gasL[:,0] = self.massGas * cross[:,0]
        gasL[:,1] = self.massGas * cross[:,1]
        gasL[:,2] = self.massGas * cross[:,2]
        # gasL = np.multiply(self.massGas, np.cross(self.posGas,self.vGas))
        gasLbound = gasL[self.boundBool,:]
        gasLunbound = gasL[self.unboundBool,:]
        gasLxbound = gasLbound[:,0]
        gasLybound = gasLbound[:,1]
        gasLzbound = gasLbound[:,2]
        gasLxunbound = gasLunbound[:,0]
        gasLyunbound = gasLunbound[:,1]
        gasLzunbound = gasLunbound[:,2]
        self.gasLbound_tot = (np.linalg.norm(gasLbound, axis=1)).sum()
        self.gasLunbound_tot = (np.linalg.norm(gasLunbound, axis=1)).sum()
        self.gasLxbound_tot = gasLxbound.sum()
        self.gasLybound_tot = gasLybound.sum()
        self.gasLzbound_tot = gasLzbound.sum()
        self.gasLxunbound_tot = gasLxunbound.sum()
        self.gasLyunbound_tot = gasLyunbound.sum()
        self.gasLzunbound_tot = gasLzunbound.sum()

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

        self.Emech = self.DMKErawtot + self.gasKErawtot + self.PECoreCore + self.PEGasGas + self.PECoreGas

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

    def getDynFric(self):

        #posRelComp = self.posGas - self.posComp
        #radRelComp = np.linalg.norm( posRelComp, axis=1 )
        #posRelPrim = self.posGas - self.posPrim
        #radRelPrim = np.linalg.norm( posRelPrim, axis=1 )
        #inBool = radRel < self.rScalar
        #posRel = posRel[inBool,:]
        #radRel = radRel[inBool]
        #massIn = self.massGas[inBool]
        #gravComp = self.mComp*self.massGas*posRelComp/radRelComp/radRelComp/radRelComp
        #gravPrim = self.mPrim*self.massGas*posRelPrim/radRelPrim/radRelPrim/radRelPrim

        posRelPrim = self.posGas - self.posPrim
        radRelPrim = np.linalg.norm( posRelPrim, axis=1 )
        u = radRelPrim / self.softLen[0]
        boolArray1 = u < 0.5
        boolArray2 = u < 1.0
        boolArrayIn = np.array( boolArray1, dtype=bool )
        boolArrayMid = np.logical_and( boolArray2, np.logical_not(boolArray1) )
        boolArrayOut = np.logical_not( boolArray2 )

        radiusIn = radRelPrim[boolArrayIn]
        radiusMid = radRelPrim[boolArrayMid]
        radiusOut = radRelPrim[boolArrayOut]
        massIn = self.massGas[boolArrayIn]
        massMid = self.massGas[boolArrayMid]
        massOut = self.massGas[boolArrayOut]
        uIn = u[boolArrayIn]
        uMid = u[boolArrayMid]
        uOut = u[boolArrayOut]

        factorIn = 14./5.*uIn-16./3.*np.power(uIn,3.)+48./5.*np.power(uIn,5.)-32./5.*np.power(uIn,6.)
        factorMid = -1./15.+16./5.*uMid-32./3.*np.power(uMid,3.)+16.*np.power(uMid,4.)-48./5.*np.power(uMid,5.)+32./15.*np.power(uMid,6.)
        factorOut = 1.

        gravInX = factorIn * massIn * self.mPrim * posRelPrim[boolArrayIn][:,0] /radiusIn/radiusIn/radiusIn
        gravInY = factorIn * massIn * self.mPrim * posRelPrim[boolArrayIn][:,1] /radiusIn/radiusIn/radiusIn
        gravInZ = factorIn * massIn * self.mPrim * posRelPrim[boolArrayIn][:,2] /radiusIn/radiusIn/radiusIn
        gravMidX = factorMid * massMid * self.mPrim * posRelPrim[boolArrayMid][:,0] /radiusMid/radiusMid/radiusMid
        gravMidY = factorMid * massMid * self.mPrim * posRelPrim[boolArrayMid][:,1] /radiusMid/radiusMid/radiusMid
        gravMidZ = factorMid * massMid * self.mPrim * posRelPrim[boolArrayMid][:,2] /radiusMid/radiusMid/radiusMid
        gravOutX = factorOut * massOut * self.mPrim * posRelPrim[boolArrayOut][:,0] /radiusOut/radiusOut/radiusOut
        gravOutY = factorOut * massOut * self.mPrim * posRelPrim[boolArrayOut][:,1] /radiusOut/radiusOut/radiusOut
        gravOutZ = factorOut * massOut * self.mPrim * posRelPrim[boolArrayOut][:,2] /radiusOut/radiusOut/radiusOut

        gravIn = np.zeros((boolArrayIn.sum(),3))
        gravMid = np.zeros((boolArrayMid.sum(),3))
        gravOut = np.zeros((boolArrayOut.sum(),3))
        gravIn[:,0] = gravInX
        gravIn[:,1] = gravInY
        gravIn[:,2] = gravInZ
        gravMid[:,0] = gravMidX
        gravMid[:,1] = gravMidY
        gravMid[:,2] = gravMidZ
        gravOut[:,0] = gravOutX
        gravOut[:,1] = gravOutY
        gravOut[:,2] = gravOutZ

        #gravMid = factorMid * massMid * self.mPrim * posRelPrim[boolArrayMid] /radiusMid/radiusMid/radiusMid
        #gravOut = factorOut * massOut * self.mPrim * posRelPrim[boolArrayOut] /radiusOut/radiusOut/radiutOut

        forceCoreCore = self.mPrim*self.mComp/self.rScalar/self.rScalar/self.rScalar*(self.posPrim-self.posComp)

        gravPrim = np.linalg.norm(gravIn,axis=0)+np.linalg.norm(gravMid,axis=0)+np.linalg.norm(gravOut,axis=0)-forceCoreCore

        gravComp = self.mirrorGrav*self.mirrorMass
        gravCompGas = gravComp - forceCoreCore

        gravCompGasCorr = gravCompGas - self.mComp/self.mPrim*gravPrim
        mirrorForceCorr = self.mirrorForce - self.mComp/self.mPrim*gravPrim

        vRel = self.vComp - self.vPrim
        vRelUnit = -vRel / np.linalg.norm(vRel)
        rRelUnit = (self.posComp-self.posPrim)/np.linalg.norm(self.posComp-self.posPrim)
        nplane = np.cross(rRelUnit,vRelUnit)
        nplane = nplane / np.linalg.norm(nplane)
        phiHat = np.cross(nplane,rRelUnit)
        forceDynFric = np.dot(gravCompGasCorr,-phiHat)
        #forceDynFric = np.dot(gravCompGasCorr,-vRelUnit)

        self.mirrorGravCorr = gravCompGasCorr
        self.mirrorForceCorr = mirrorForceCorr
        self.dynFric = forceDynFric

    def doEverything(self):

        self.readData()
        if movingBC :
            self.addMirror()
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
        self.getMomentum()
        if movingBC :
            self.getDynFric()
