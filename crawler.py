import numpy as np
import sys
from datastruc import *
import time as realtime

def crawlRead():

    try:
        data = np.loadtxt('data.txt')
        numsets = np.shape(data)[0]
    except:
        numsets = 0
        data = []
    print('Found ' + str(numsets) + ' analyzed datasets')
    return numsets, data

def crawlWrite(data):

    size = np.shape(data)[0]
    file = open('data.txt','w')
    for i in range(0,size):
        datastr = str(data[i,:])
        datastr = datastr.replace('\n','')
        datastr = datastr[2:len(datastr)-15] + '\n'
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
    sep = data[:,9]
    velCMnorm = data[:,10]
    posPrimx = data[:,11]
    posPrimy = data[:,12]
    posPrimz = data[:,13]
    posCompx = data[:,14]
    posCompy = data[:,15]
    posCompz = data[:,16]
    massGasTot = data[:,17]

    return setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, posCompz, massGasTot

def crawl():
    print('\nCrawling...\n')
    parseParams()
    from params import dPeriod
    lim = dPeriod / 2. * 1.0001
    hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])
    numsets, data = crawlRead()
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
        sep = []
        velCMnorm = []
        posPrimx = []
        posPrimy = []
        posPrimz = []
        posCompx = []
        posCompy = []
        posCompz = []
        massGasTot = []

    else:
        setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, posCompz, massGasTot = splitData(data)

    beginset = startingset + frameskip * numsets
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
        dataset.findCM()
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
        sep = np.append( sep, dataset.sep )
        velCMnorm = np.append( velCMnorm, dataset.velCMnorm )
        posPrimx = np.append( posPrimx, dataset.posDM[0,0] )
        posPrimy = np.append( posPrimy, dataset.posDM[0,1] )
        posPrimz = np.append( posPrimz, dataset.posDM[0,2] )
        posCompx = np.append( posCompx, dataset.posDM[1,0] )
        posCompy = np.append( posCompy, dataset.posDM[1,1] )
        posCompz = np.append( posCompz, dataset.posDM[1,2] )
        massGasTot = np.append( massGasTot, dataset.massGasTot )

        newdata = np.stack( (setnums,time,posCMx,posCMy,posCMz,vCMx,vCMy,vCMz,fracunbound,sep,velCMnorm,posPrimx,posPrimy,posPrimz,posCompx,posCompy,posCompz,massGasTot), axis=1 )
        crawlWrite(newdata)
        endtime = realtime.time()
        elapsed = endtime - starttime
        print('took ' + str(elapsed)[0:4] + ' seconds')

        i = i + frameskip

    print('Done crawling')

if __name__ == '__main__':
    crawl()
