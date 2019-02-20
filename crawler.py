import numpy as np
import sys
from datastruc import *
import time as realtime
import os

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

def findPattern():

    i = 1
    foundCount = 0
    sets = [0,0]
    while foundCount < 2:
        num = i + 1000000
        numstr = str(num)
        cut = numstr[1:7]
        filename = 'star.out.' + cut
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
    print('Parsed parameter file')

def dataSize():
    size = 19
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
    gasPEtot = data[:,24]
    DMKEtot = data[:,25]
    DMPEtot = data[:,26]

    return setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, gasPEtot, DMKEtot, DMPEtot

def crawl():
    print('\nCrawling...\n')
    parseParams()
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
        gasPEtot = []
        DMKEtot = []
        DMPEtot = []

    else:
        setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
    	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
    	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, gasPEtot, DMKEtot, DMPEtot = splitData(cutdata)

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
        filename = 'star.out.' + cut

        try:
            dataset = Dataset(filename, hbox)
        except:
            print('No more files found, breaking...')
            break
        # print('Starting dataset ' + str(i) + ' ... ' )
        sys.stdout.write('Starting dataset ' + str(i) + ' ... ')
        sys.stdout.flush()

        dataset.readData()
        dataset.getPE()
        dataset.findCM()
        dataset.getKE()
        dataset.getTime()
        dataset.getUnbound()
        dataset.getOrbit()

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
        gasPEtot = np.append( gasPEtot, dataset.gasPEtot )
        DMKEtot = np.append( DMKEtot, dataset.DMKEtot )
        DMPEtot = np.append( DMPEtot, dataset.DMPEtot )

        newdata = np.stack( (setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, fracunbound_i, \
    	sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, \
    	posCompz, massGasTot, ejeceff, ejeceff_i, ietot, ie_idealtot, gasKEtot, gasPEtot, DMKEtot, DMPEtot), axis=1 )
        crawlWrite(newdata)
        endtime = realtime.time()
        elapsed = endtime - starttime
        print('took ' + str(elapsed)[0:4] + ' seconds')

        i = i + frameskip

    print('Done crawling')

if __name__ == '__main__':
    crawl()
