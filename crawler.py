import numpy as np
import sys
from datastruc import *
import time as realtime
import os
import multiprocessing

def crawlRead(path=''):

    try:
        cwd = os.getcwd()
        filepath = cwd + '/' + path + 'data.txt'
        data = np.loadtxt(filepath)
        numsets = np.shape(data)[0]
        print('Found ' + str(numsets) + ' analyzed datasets')
    except:
        numsets = 0
        data = []
        print('Found no analyzed datasets')
    return numsets, data

def crawlCutData( numsets, data ):
    cutdata = data[ 0:numsets-1, : ]
    return cutdata

def crawlWrite(data,path=''):

    size = np.shape(data)[0]
    file = open(path + 'data.txt','w')
    for i in range(0,size):
        datastr = str(data[i,:])
        datastr = datastr.replace('\n','')
        datastr = datastr[1:len(datastr)-15] + '\n'
        file.write(datastr)
    file.close()
    sys.stdout.write('wrote data file ... ')

def getFilePrefix():

    return 'patch3.out.'

def findPattern():

    i = 1
    foundCount = 0
    sets = [0,0]
    while foundCount < 2:
        num = i + 1000000
        numstr = str(num)
        cut = numstr[1:7]
        filename = getFilePrefix() + cut
        try:
            open(filename,'r')
            sets[foundCount] = i
            foundCount = foundCount+1
        except IOError:
            pass
        i = i+1
    startingset = sets[0]
    frameskip = sets[1] - sets[0]
    print('First set ' + str(startingset) + ' with skip ' + str(frameskip) )
    return startingset, frameskip

def parseParams():

    filename = 'sph.param'
    try:
        open('sph.param','r')
    except:
        filename = 'mm.param'
    readfile = open( filename, 'r' )
    text = readfile.read()
    readfile.close()
    textsplit = text.split('\n')
    for i in range(0,len(textsplit)):
        if textsplit[i][0:3] == 'ach':
            textsplit[i] = ''
        elif textsplit[i][0:4] == 'Mesa':
            textsplit[i] = ''
    writefile = open('params.py','w')
    for x in textsplit:
        writefile.write( x + '\n' )
    writefile.close()
    print('Parsed parameter file ... ')

def dataSize():
    size = 97
    return size

def splitData(data):

    setnums = data[:,0]
    time = data[:,1]
    posCMx = data[:,2]
    posCMy = data[:,3]
    posCMz = data[:,4]
    vCMx = data[:,5]
    vCMy = data[:,6]
    vCMz = data[:,7]
    fracunbound = data[:,8]
    fracunbound_i = data[:,9]
    sep = data[:,10]
    velCMnorm = data[:,11]
    posPrimx = data[:,12]
    posPrimy = data[:,13]
    posPrimz = data[:,14]
    posCompx = data[:,15]
    posCompy = data[:,16]
    posCompz = data[:,17]
    massGasTot = data[:,18]
    ejeceff = data[:,19]
    ejeceff_i = data[:,20]
    ietot = data[:,21]
    ie_idealtot = data[:,22]
    gasKEtot = data[:,23]
    DMKEtot = data[:,24]
    velCMDMnorm = data[:,25]
    fracunbound_noIe = data[:,26]
    ejeceff_noIe = data[:,27]
    gasKEunbound = data[:,28]
    gasKEbound = data[:,29]
    gasIEunbound = data[:,30]
    gasIEbound = data[:,31]
    PECoreGasUnboundPrim = data[:,32]
    PECoreGasBoundPrim = data[:,33]
    PECoreGasUnboundComp = data[:,34]
    PECoreGasBoundComp = data[:,35]
    PECoreCore = data[:,36]
    PEGasGasUnbound = data[:,37]
    PEGasGasBound = data[:,38]
    Emech = data[:,39]
    gasPbound = data[:,40]
    gasPunbound = data[:,41]
    gasPxbound = data[:,42]
    gasPybound = data[:,43]
    gasPzbound = data[:,44]
    gasPxunbound = data[:,45]
    gasPyunbound = data[:,46]
    gasPzunbound = data[:,47]
    gasLbound = data[:,48]
    gasLunbound = data[:,49]
    gasLxbound = data[:,50]
    gasLybound = data[:,51]
    gasLzbound = data[:,52]
    gasLxunbound = data[:,53]
    gasLyunbound = data[:,54]
    gasLzunbound = data[:,55]
    corePx = data[:,56]
    corePy = data[:,57]
    corePz = data[:,58]
    compPx = data[:,59]
    compPy = data[:,60]
    compPz = data[:,61]
    coreLx = data[:,62]
    coreLy = data[:,63]
    coreLz = data[:,64]
    compLx = data[:,65]
    compLy = data[:,66]
    compLz = data[:,67]
    reflectiveCount = data[:,68]
    edgeCount = data[:,69]
    mirrorLeft = data[:,70]
    mirrorRight = data[:,71]
    mirrorRadius = data[:,72]
    mirrorCenterX = data[:,73]
    mirrorCenterY = data[:,74]
    mirrorCenterZ = data[:,75]
    mirrorMass = data[:,76]
    mirrorVelX = data[:,77]
    mirrorVelY = data[:,78]
    mirrorVelZ = data[:,79]
    mirrorForceX = data[:,80]
    mirrorForceY = data[:,81]
    mirrorForceZ = data[:,82]
    mirrorGravX = data[:,83]
    mirrorGravY = data[:,84]
    mirrorGravZ = data[:,85]
    mirrorGravCorrX = data[:,86]
    mirrorGravCorrY = data[:,87]
    mirrorGravCorrZ = data[:,88]
    dynFric = data[:,89]
    dynFricV = data[:,90]
    dynFricNoCorr = data[:,91]
    mPrim = data[:,92]
    mComp = data[:,93]
    gravPrimGasX = data[:,94]
    gravPrimGasY = data[:,95]
    gravPrimGasZ = data[:,96]

    return setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, DMKEtot, velCMDMnorm, fracunbound_noIe, ejeceff_noIe, \
    gasKEunbound, gasKEbound, gasIEunbound, gasIEbound, PECoreGasUnboundPrim, PECoreGasBoundPrim, PECoreGasUnboundComp, PECoreGasBoundComp, PECoreCore, PEGasGasUnbound, PEGasGasBound, \
    Emech, gasPbound, gasPunbound, gasPxbound, gasPybound, gasPzbound, gasPxunbound, gasPyunbound, gasPzunbound, gasLbound, gasLunbound, gasLxbound, gasLybound, gasLzbound, gasLxunbound, gasLyunbound, gasLzunbound, \
    corePx, corePy, corePz, compPx, compPy, compPz, coreLx, coreLy, coreLz, compLx, compLy, compLz, \
    reflectiveCount, edgeCount, mirrorLeft, mirrorRight, mirrorRadius, mirrorCenterX, mirrorCenterY, mirrorCenterZ, \
    mirrorMass, mirrorVelX, mirrorVelY, mirrorVelZ, mirrorForceX, mirrorForceY, mirrorForceZ, mirrorGravX, mirrorGravY, mirrorGravZ, mirrorGravCorrX, mirrorGravCorrY, mirrorGravCorrZ, dynFric, dynFricV, dynFricNoCorr, \
    mPrim, mComp, gravPrimGasX, gravPrimGasY, gravPrimGasZ

def crawl():
    print('\nCrawling...\n')
    parseParams()
    sys.stdout.flush()
    from params import dPeriod
    lim = dPeriod / 2. * 1.0001
    hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])
    numsets, data = crawlRead()
    if numsets != 0:
        cutdata = crawlCutData(numsets,data)
    else:
        cutdata = data
    startingset, frameskip = findPattern()

    if numsets == 0:
        setnums = []
        time = []
        posCMx = []
        posCMy = []
        posCMz = []
        vCMx = []
        vCMy = []
        vCMz = []
        fracunbound = []
        fracunbound_i = []
        sep = []
        velCMnorm = []
        posPrimx = []
        posPrimy = []
        posPrimz = []
        posCompx = []
        posCompy = []
        posCompz = []
        massGasTot = []
        ejeceff = []
        ejeceff_i = []
        ietot = []
        ie_idealtot = []
        gasKEtot = []
        DMKEtot = []
        velCMDMnorm = []
        fracunbound_noIe = []
        ejeceff_noIe = []
        gasKEunbound = []
        gasKEbound = []
        gasIEunbound = []
        gasIEbound = []
        PECoreGasUnboundPrim = []
        PECoreGasBoundPrim = []
        PECoreGasUnboundComp = []
        PECoreGasBoundComp = []
        PECoreCore = []
        PEGasGasUnbound = []
        PEGasGasBound = []
        Emech = []
        gasPbound = []
        gasPunbound = []
        gasPxbound = []
        gasPybound = []
        gasPzbound = []
        gasPxunbound = []
        gasPyunbound = []
        gasPzunbound = []
        gasLbound = []
        gasLunbound = []
        gasLxbound = []
        gasLybound = []
        gasLzbound = []
        gasLxunbound = []
        gasLyunbound = []
        gasLzunbound = []
        corePx = []
        corePy = []
        corePz = []
        compPx = []
        compPy = []
        compPz = []
        coreLx = []
        coreLy = []
        coreLz = []
        compLx = []
        compLy = []
        compLz = []
        reflectiveCount = []
        edgeCount = []
        mirrorLeft = []
        mirrorRight = []
        mirrorRadius = []
        mirrorCenterX = []
        mirrorCenterY = []
        mirrorCenterZ = []
        mirrorMass = []
        mirrorVelX = []
        mirrorVelY = []
        mirrorVelZ = []
        mirrorForceX = []
        mirrorForceY = []
        mirrorForceZ = []
        mirrorGravX = []
        mirrorGravY = []
        mirrorGravZ = []
        mirrorGravCorrX = []
        mirrorGravCorrY = []
        mirrorGravCorrZ = []
        dynFric = []
        dynFricV = []
        dynFricNoCorr = []
        mPrim = []
        mComp = []
        gravPrimGasX = []
        gravPrimGasY = []
        gravPrimGasZ = []

    else:
        setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
    	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
    	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, DMKEtot, velCMDMnorm, fracunbound_noIe, ejeceff_noIe, \
        gasKEunbound, gasKEbound, gasIEunbound, gasIEbound, PECoreGasUnboundPrim, PECoreGasBoundPrim, PECoreGasUnboundComp, PECoreGasBoundComp, PECoreCore, PEGasGasUnbound, PEGasGasBound, \
        Emech, gasPbound, gasPunbound, gasPxbound, gasPybound, gasPzbound, gasPxunbound, gasPyunbound, gasPzunbound, gasLbound, gasLunbound, gasLxbound, gasLybound, gasLzbound, gasLxunbound, gasLyunbound, gasLzunbound, \
        corePx, corePy, corePz, compPx, compPy, compPz, coreLx, coreLy, coreLz, compLx, compLy, compLz, \
        reflectiveCount, edgeCount, mirrorLeft, mirrorRight, mirrorRadius, mirrorCenterX, mirrorCenterY, mirrorCenterZ, \
        mirrorMass, mirrorVelX, mirrorVelY, mirrorVelZ, mirrorForceX, mirrorForceY, mirrorForceZ, mirrorGravX, mirrorGravY, mirrorGravZ, mirrorGravCorrX, mirrorGravCorrY, mirrorGravCorrZ, dynFric, dynFricV, dynFricNoCorr, \
        mPrim, mComp, gravPrimGasX, gravPrimGasY, gravPrimGasZ = splitData(cutdata)

    if numsets==0:
        beginset = startingset
    else:
        beginset = startingset + frameskip * (numsets - 1)
    i = beginset
    endflag = 0
    while endflag == 0:

        starttime = realtime.time()
        num = i + 1000000
        numstr = str(num)
        cut = numstr[1:7]
        filename = getFilePrefix() + cut

        try:
            dataset = Dataset(filename, hbox)
        except:
            print('No more files found, breaking...')
            break
        # print('Starting dataset ' + str(i) + ' ... ' )
        sys.stdout.write('Starting dataset ' + str(i) + ' ... ')
        sys.stdout.flush()

        movingBC = False

        dataset.readData()
        if movingBC :
            dataset.addMirror()
        # if args.cutvacuum :
            # dataset.cutVacuum()
        dataset.getIE()
        dataset.getPE()
        dataset.findCM()
        dataset.findCMDM()
        dataset.getKE()
        dataset.getTime()
        dataset.getEjecta()
        dataset.getOrbit()
        dataset.getBoundUnbound()
        dataset.PEstuff()
        dataset.getMomentum()
        if movingBC :
            dataset.getDynFric()

        setnums = np.append( setnums, i )
        time = np.append( time, dataset.time )
        posCMx = np.append( posCMx, dataset.posCM[0] )
        posCMy = np.append( posCMy, dataset.posCM[1] )
        posCMz = np.append( posCMz, dataset.posCM[2] )
        vCMx = np.append( vCMx, dataset.vCM[0] )
        vCMy = np.append( vCMy, dataset.vCM[1] )
        vCMz = np.append( vCMz, dataset.vCM[2] )
        fracunbound = np.append( fracunbound, dataset.fracunbound )
        fracunbound_i = np.append( fracunbound_i, dataset.fracunbound_i )
        sep = np.append( sep, dataset.sep )
        velCMnorm = np.append( velCMnorm, dataset.velCMnorm )
        posPrimx = np.append( posPrimx, dataset.posDM[0,0] )
        posPrimy = np.append( posPrimy, dataset.posDM[0,1] )
        posPrimz = np.append( posPrimz, dataset.posDM[0,2] )
        posCompx = np.append( posCompx, dataset.posDM[1,0] )
        posCompy = np.append( posCompy, dataset.posDM[1,1] )
        posCompz = np.append( posCompz, dataset.posDM[1,2] )
        massGasTot = np.append( massGasTot, dataset.massGasTot )
        ejeceff = np.append( ejeceff, dataset.ejeceff )
        ejeceff_i = np.append( ejeceff_i, dataset.ejeceff_i )
        ietot = np.append( ietot, dataset.ietot )
        ie_idealtot = np.append( ie_idealtot, dataset.ie_idealtot )
        gasKEtot = np.append( gasKEtot, dataset.gasKEtot )
        DMKEtot = np.append( DMKEtot, dataset.DMKEtot )
        velCMDMnorm = np.append( velCMDMnorm, dataset.velCMDMnorm )
        fracunbound_noIe = np.append( fracunbound_noIe, dataset.fracunbound_noIe )
        ejeceff_noIe = np.append( ejeceff_noIe, dataset.ejeceff_noIe )
        gasKEunbound = np.append( gasKEunbound, dataset.gasKEunboundTot )
        gasKEbound = np.append( gasKEbound, dataset.gasKEboundTot )
        gasIEunbound = np.append( gasIEunbound, dataset.gasIEunboundTot )
        gasIEbound = np.append( gasIEbound, dataset.gasIEboundTot )
        PECoreGasUnboundPrim = np.append( PECoreGasUnboundPrim, dataset.PECoreGasUnboundCore )
        PECoreGasBoundPrim = np.append( PECoreGasBoundPrim, dataset.PECoreGasBoundCore )
        PECoreGasUnboundComp = np.append( PECoreGasUnboundComp, dataset.PECoreGasUnboundComp )
        PECoreGasBoundComp = np.append( PECoreGasBoundComp, dataset.PECoreGasBoundComp )
        PECoreCore = np.append( PECoreCore, dataset.PECoreCore )
        PEGasGasUnbound = np.append( PEGasGasUnbound, dataset.PEGasGasUnbound )
        PEGasGasBound = np.append( PEGasGasBound, dataset.PEGasGasBound )
        Emech = np.append( Emech, dataset.Emech )
        gasPbound = np.append( gasPbound, dataset.gasPbound_tot )
        gasPunbound = np.append( gasPunbound, dataset.gasPunbound_tot )
        gasPxbound = np.append( gasPxbound, dataset.gasPxbound_tot )
        gasPybound = np.append( gasPybound, dataset.gasPybound_tot )
        gasPzbound = np.append( gasPzbound, dataset.gasPzbound_tot )
        gasPxunbound = np.append( gasPxunbound, dataset.gasPxunbound_tot )
        gasPyunbound = np.append( gasPyunbound, dataset.gasPyunbound_tot )
        gasPzunbound = np.append( gasPzunbound, dataset.gasPzunbound_tot )
        gasLbound = np.append( gasLbound, dataset.gasLbound_tot )
        gasLunbound = np.append( gasLunbound, dataset.gasLunbound_tot )
        gasLxbound = np.append( gasLxbound, dataset.gasLxbound_tot )
        gasLybound = np.append( gasLybound, dataset.gasLybound_tot )
        gasLzbound = np.append( gasLzbound, dataset.gasLzbound_tot )
        gasLxunbound = np.append( gasLxunbound, dataset.gasLxunbound_tot )
        gasLyunbound = np.append( gasLyunbound, dataset.gasLyunbound_tot )
        gasLzunbound = np.append( gasLzunbound, dataset.gasLzunbound_tot )
        corePx = np.append( corePx, dataset.corePx )
        corePy = np.append( corePy, dataset.corePy )
        corePz = np.append( corePz, dataset.corePz )
        compPx = np.append( compPx, dataset.compPx )
        compPy = np.append( compPy, dataset.compPy )
        compPz = np.append( compPz, dataset.compPz )
        coreLx = np.append( coreLx, dataset.coreLx )
        coreLy = np.append( coreLy, dataset.coreLy )
        coreLz = np.append( coreLz, dataset.coreLz )
        compLx = np.append( compLx, dataset.compLx )
        compLy = np.append( compLy, dataset.compLy )
        compLz = np.append( compLz, dataset.compLz )
        reflectiveCount = np.append( reflectiveCount, dataset.reflectiveCount )
        edgeCount = np.append( edgeCount, dataset.edgeCount )
        mirrorLeft = np.append( mirrorLeft, dataset.mirrorLeft )
        mirrorRight = np.append( mirrorRight, dataset.mirrorRight )
        mirrorRadius = np.append( mirrorRadius, dataset.mirrorRadius )
        mirrorCenterX = np.append( mirrorCenterX, dataset.mirrorCenter[0] )
        mirrorCenterY = np.append( mirrorCenterY, dataset.mirrorCenter[1] )
        mirrorCenterZ = np.append( mirrorCenterZ, dataset.mirrorCenter[2] )
        mirrorMass = np.append( mirrorMass, dataset.mirrorMass )
        mirrorVelX = np.append( mirrorVelX, dataset.mirrorVel[0] )
        mirrorVelY = np.append( mirrorVelY, dataset.mirrorVel[1] )
        mirrorVelZ = np.append( mirrorVelZ, dataset.mirrorVel[2] )
        mirrorForceX = np.append( mirrorForceX, dataset.mirrorForce[0] )
        mirrorForceY = np.append( mirrorForceY, dataset.mirrorForce[1] )
        mirrorForceZ = np.append( mirrorForceZ, dataset.mirrorForce[2] )
        mirrorGravX = np.append( mirrorGravX, dataset.mirrorGrav[0] )
        mirrorGravY = np.append( mirrorGravY, dataset.mirrorGrav[1] )
        mirrorGravZ = np.append( mirrorGravZ, dataset.mirrorGrav[2] )
        mirrorGravCorrX = np.append( mirrorGravCorrX, dataset.mirrorGravCorr[0] )
        mirrorGravCorrY = np.append( mirrorGravCorrY, dataset.mirrorGravCorr[1] )
        mirrorGravCorrZ = np.append( mirrorGravCorrZ, dataset.mirrorGravCorr[2] )
        dynFric = np.append( dynFric, dataset.dynFric )
        dynFricV = np.append( dynFricV, dataset.dynFricV )
        dynFricNoCorr = np.append( dynFricNoCorr, dataset.dynFricNoCorr )
        mPrim = np.append( mPrim, dataset.mPrim )
        mComp = np.append( mComp, dataset.mComp )
        gravPrimGasX = np.append( gravPrimGasX, dataset.gravPrimGas[0] )
        gravPrimGasY = np.append( gravPrimGasY, dataset.gravPrimGas[1] )
        gravPrimGasZ = np.append( gravPrimGasZ, dataset.gravPrimGas[2] )

        newdata = np.stack( (setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
    	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
    	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, DMKEtot, velCMDMnorm, fracunbound_noIe, ejeceff_noIe, \
        gasKEunbound, gasKEbound, gasIEunbound, gasIEbound, PECoreGasUnboundPrim, PECoreGasBoundPrim, PECoreGasUnboundComp, PECoreGasBoundComp, PECoreCore, PEGasGasUnbound, PEGasGasBound, \
        Emech, gasPbound, gasPunbound, gasPxbound, gasPybound, gasPzbound, gasPxunbound, gasPyunbound, gasPzunbound, gasLbound, gasLunbound, gasLxbound, gasLybound, gasLzbound, gasLxunbound, gasLyunbound, gasLzunbound, \
        corePx, corePy, corePz, compPx, compPy, compPz, coreLx, coreLy, coreLz, compLx, compLy, compLz, \
        reflectiveCount, edgeCount, mirrorLeft, mirrorRight, mirrorRadius, mirrorCenterX, mirrorCenterY, mirrorCenterZ, \
        mirrorMass, mirrorVelX, mirrorVelY, mirrorVelZ, mirrorForceX, mirrorForceY, mirrorForceZ, mirrorGravX, mirrorGravY, mirrorGravZ, mirrorGravCorrX, mirrorGravCorrY, mirrorGravCorrZ, dynFric, dynFricV, dynFricNoCorr, \
        mPrim, mComp, gravPrimGasX, gravPrimGasY, gravPrimGasZ ), axis=1 )
        crawlWrite(newdata)
        endtime = realtime.time()
        elapsed = endtime - starttime
        print('took ' + str(elapsed)[0:4] + ' seconds')

        i = i + frameskip

    print('Done crawling')

def readSet(i,hbox):
    num = i + 1000000
    numstr = str(num)
    cut = numstr[1:7]
    filename = getFilePrefix() + cut
    sys.stdout.write('Starting set ' + str(i) + ' ... ')

    try:
        dataset = Dataset(filename, hbox)

        dataset.readData()
        if movingBC :
            dataset.addMirror()
        dataset.getIE()
        dataset.getPE()
        dataset.findCM()
        dataset.findCMDM()
        dataset.getKE()
        dataset.getTime()
        dataset.getEjecta()
        dataset.getOrbit()
        dataset.getBoundUnbound()
        dataset.PEstuff()
        if movingBC :
            dataset.getDynFric()

        setnums = i
        time = dataset.time
        posCMx = dataset.posCM[0]
        posCMy = dataset.posCM[1]
        posCMz = dataset.posCM[2]
        vCMx = dataset.vCM[0]
        vCMy = dataset.vCM[1]
        vCMz = dataset.vCM[2]
        fracunbound = dataset.fracunbound
        fracunbound_i = dataset.fracunbound_i
        sep = dataset.sep
        velCMnorm = dataset.velCMnorm
        posPrimx = dataset.posDM[0,0]
        posPrimy = dataset.posDM[0,1]
        posPrimz = dataset.posDM[0,2]
        posCompx = dataset.posDM[1,0]
        posCompy = dataset.posDM[1,1]
        posCompz = dataset.posDM[1,2]
        massGasTot = dataset.massGasTot
        ejeceff = dataset.ejeceff
        ejeceff_i = dataset.ejeceff_i
        ietot = dataset.ietot
        ie_idealtot = dataset.ie_idealtot
        gasKEtot = dataset.gasKEtot
        DMKEtot = dataset.DMKEtot
        velCMDMnorm = dataset.velCMDMnorm
        fracunbound_noIe = dataset.fracunbound_noIe
        ejeceff_noIe = dataset.ejeceff_noIe
        gasKEunbound = dataset.gasKEunboundTot
        gasKEbound = dataset.gasKEboundTot
        gasIEunbound = dataset.gasIEunboundTot
        gasIEbound = dataset.gasIEboundTot
        PECoreGasUnboundPrim = dataset.PECoreGasUnboundCore
        PECoreGasBoundPrim = dataset.PECoreGasBoundCore
        PECoreGasUnboundComp = dataset.PECoreGasUnboundComp
        PECoreGasBoundComp = dataset.PECoreGasBoundComp
        PECoreCore = dataset.PECoreCore
        PEGasGasUnbound = dataset.PEGasGasUnbound
        PEGasGasBound = dataset.PEGasGasBound
        Emech = dataset.Emech
        gasPbound = dataset.gasPbound_tot
        gasPunbound = dataset.gasPunbound_tot
        gasPxbound = dataset.gasPxbound_tot
        gasPybound = dataset.gasPybound_tot
        gasPzbound = dataset.gasPzbound_tot
        gasPxunbound = dataset.gasPxunbound_tot
        gasPyunbound = dataset.gasPyunbound_tot
        gasPzunbound = dataset.gasPzunbound_tot
        gasLbound = dataset.gasLbound_tot
        gasLunbound = dataset.gasLunbound_tot
        gasLxbound = dataset.gasLxbound_tot
        gasLybound = dataset.gasLybound_tot
        gasLzbound = dataset.gasLzbound_tot
        gasLxunbound = dataset.gasLxunbound_tot
        gasLyunbound = dataset.gasLyunbound_tot
        gasLzunbound = dataset.gasLzunbound_tot
        corePx = dataset.corePx
        corePy = dataset.corePy
        corePz = dataset.corePz
        compPx = dataset.compPx
        compPy = dataset.compPy
        compPz = dataset.compPz
        coreLx = dataset.coreLx
        coreLy = dataset.coreLy
        coreLz = dataset.coreLz
        compLx = dataset.compLx
        compLy = dataset.compLy
        compLz = dataset.compLz
        reflectiveCount = dataset.reflectiveCount
        edgeCount = dataset.edgeCount
        mirrorLeft = dataset.mirrorLeft
        mirrorRight = dataset.mirrorRight
        mirrorRadius = dataset.mirrorRadius
        mirrorCenterX = dataset.mirrorCenter[0]
        mirrorCenterY = dataset.mirrorCenter[1]
        mirrorCenterZ = dataset.mirrorCenter[2]
        mirrorMass = dataset.mirrorMass
        mirrorVelX = dataset.mirrorVel[0]
        mirrorVelY = dataset.mirrorVel[1]
        mirrorVelZ = dataset.mirrorVel[2]
        mirrorForceX = dataset.mirrorForce[0]
        mirrorForceY = dataset.mirrorForce[1]
        mirrorForceZ = dataset.mirrorForce[2]
        mirrorGravX = dataset.mirrorGrav[0]
        mirrorGravY = dataset.mirrorGrav[1]
        mirrorGravZ = dataset.mirrorGrav[2]
        mirrorGravCorrX = dataset.mirrorGravCorr[0]
        mirrorGravCorrY = dataset.mirrorGravCorr[1]
        mirrorGravCorrZ = dataset.mirrorGravCorr[2]
        dynFric = dataset.dynFric
        dynFricV = dataset.dynFricV
        dynFricNoCorr = dataset.dynFricNoCorr
        mPrim = dataset.mPrim
        mComp = dataset.mComp
        gravPrimGasX = dataset.gravPrimGas[0]
        gravPrimGasY = dataset.gravPrimGas[1]
        gravPrimGasZ = dataset.gravPrimGas[2]

        endflag = 0

        newdata = np.stack( (setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
    	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
    	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, DMKEtot, velCMDMnorm, fracunbound_noIe, ejeceff_noIe, \
        gasKEunbound, gasKEbound, gasIEunbound, gasIEbound, PECoreGasUnboundPrim, PECoreGasBoundPrim, PECoreGasUnboundComp, PECoreGasBoundComp, PECoreCore, PEGasGasUnbound, PEGasGasBound, \
        Emech, gasPbound, gasPunbound, gasPxbound, gasPybound, gasPzbound, gasPxunbound, gasPyunbound, gasPzunbound, gasLbound, gasLunbound, gasLxbound, gasLybound, gasLzbound, gasLxunbound, gasLyunbound, gasLzunbound, \
        corePx, corePy, corePz, compPx, compPy, compPz, coreLx, coreLy, coreLz, compLx, compLy, compLz, \
        reflectiveCount, edgeCount, mirrorLeft, mirrorRight, mirrorRadius, mirrorCenterX, mirrorCenterY, mirrorCenterZ, \
        mirrorMass, mirrorVelX, mirrorVelY, mirrorVelZ, mirrorForceX, mirrorForceY, mirrorForceZ, mirrorGravX, mirrorGravY, mirrorGravZ, mirrorGravCorrX, mirrorGravCorrY, mirrorGravCorrZ, dynFric, dynFricV, dynFricNoCorr, \
        mPrim, mComp, gravPrimGasX, gravPrimGasY, gravPrimGasZ ), axis=0 )

    except:
        endflag = 1
        newdata = np.zeros( dataSize() )

    print('done')
    return newdata, endflag

def crawlMulti(threads):
    print('\nStarting up ' + str(threads) + ' workers ...\n')
    numsets = 0
    startingset, frameskip = findPattern()

    previousNumsets, previousData = crawlRead()

    setnums = []
    time = []
    posCMx = []
    posCMy = []
    posCMz = []
    vCMx = []
    vCMy = []
    vCMz = []
    fracunbound = []
    fracunbound_i = []
    sep = []
    velCMnorm = []
    posPrimx = []
    posPrimy = []
    posPrimz = []
    posCompx = []
    posCompy = []
    posCompz = []
    massGasTot = []
    ejeceff = []
    ejeceff_i = []
    ietot = []
    ie_idealtot = []
    gasKEtot = []
    DMKEtot = []
    velCMDMnorm = []
    fracunbound_noIe = []
    ejeceff_noIe = []
    gasKEunbound = []
    gasKEbound = []
    gasIEunbound = []
    gasIEbound = []
    PECoreGasUnboundPrim = []
    PECoreGasBoundPrim = []
    PECoreGasUnboundComp = []
    PECoreGasBoundComp = []
    PECoreCore = []
    PEGasGasUnbound = []
    PEGasGasBound = []
    Emech = []
    gasPbound = []
    gasPunbound = []
    gasPxbound = []
    gasPybound = []
    gasPzbound = []
    gasPxunbound = []
    gasPyunbound = []
    gasPzunbound = []
    gasLbound = []
    gasLunbound = []
    gasLxbound = []
    gasLybound = []
    gasLzbound = []
    gasLxunbound = []
    gasLyunbound = []
    gasLzunbound = []
    corePx = []
    corePy = []
    corePz = []
    compPx = []
    compPy = []
    compPz = []
    coreLx = []
    coreLy = []
    coreLz = []
    compLx = []
    compLy = []
    compLz = []
    reflectiveCount = []
    edgeCount = []
    mirrorLeft = []
    mirrorRight = []
    mirrorRadius = []
    mirrorCenterX = []
    mirrorCenterY = []
    mirrorCenterZ = []
    mirrorMass = []
    mirrorVelX = []
    mirrorVelY = []
    mirrorVelZ = []
    mirrorForceX = []
    mirrorForceY = []
    mirrorForceZ = []
    mirrorGravX = []
    mirrorGravY = []
    mirrorGravZ = []
    mirrorGravCorrX = []
    mirrorGravCorrY = []
    mirrorGravCorrZ = []
    dynFric = []
    dynFricV = []
    dynFricNoCorr = []
    mPrim = []
    mComp = []
    gravPrimGasX = []
    gravPrimGasY = []
    gravPrimGasZ = []

    parseParams()
    from params import dPeriod
    lim = dPeriod / 2. * 1.0001
    hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

    beginset = startingset + frameskip * previousNumsets
    i = beginset
    emptyRows = 500
    data = np.zeros( (emptyRows,dataSize()) )
    dataCount = 0
    endflag = 0
    from functools import partial
    while endflag == 0:

        numarray = np.zeros(threads)
        for j in range(0,threads):
            numarray[j] = i + j * frameskip

        pool = multiprocessing.Pool(threads)
        dataSegment = pool.map( partial(readSet,hbox=hbox), numarray )

        i = i + frameskip * threads

        for k in range(0,threads):
            dataSlice = dataSegment[k][0]
            data[k+dataCount,:] = dataSlice
            crawlWriteMulti(dataSlice)
            if dataSlice[0] == 0.0:
                endflag = 1
        dataCount = dataCount + threads
        print('Wrote data file')

    print('Done')

def crawlWriteMulti(data,path=''):

    if data[0] == 0.0:
        pass
    else:
        size = np.shape(data)[0]
        file = open(path + 'data.txt','a')
        # for i in range(0,size):
            # datastr = str(data[i,:])
        datastr = str(data)
        datastr = datastr.replace('[','')
        datastr = datastr.replace(']','')
        datastr = datastr.replace('\n','')
        datastr = datastr.replace('dimensionless','')
        datastr = datastr + '\n'
        file.write(datastr)
        # file.close()

if __name__ == '__main__':

    threadsStr = input('# threads = ')
    threads = int(threadsStr)
    if (threads > 1) :
        crawlMulti(threads)
    else:
        crawl()
