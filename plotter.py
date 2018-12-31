from crawler import crawlRead
from crawler import splitData
import numpy as np
import argparse
import sys

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--unbound', action='store_true')
parser.add_argument('--orbel', action='store_true')
parser.add_argument('--mass', action='store_true')
parser.add_argument('--no_latex', action='store_true')
args = parser.parse_args()

if args.no_latex :
    latex = 0
else:
    latex = 1

if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')

numsets, data = crawlRead()
setnums, time, posCMx, posCMy, posCMz, vCMx, vCMy, vCMz, fracunbound, sep, velCMnorm, posPrimx, posPrimy, posPrimz, posCompx, posCompy, posCompz, massGasTot = splitData(data)

def plotMass( time, massGasTot ):
    fig = plt.figure()
    plot = plt.plot( time, massGasTot, lw=2 )
    plt.xlabel('Time (days)', fontsize=25 )
    plt.ylabel('Total Gas Mass', fontsize=25 )
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.tight_layout()
    # saveas = writepath + 'unbound_' + simname + '.pdf'
    saveas = 'masstot.pdf'
    fig.savefig(saveas)
    print('Saved plot ' + saveas)
    plt.clf()

def plotUnbound( time, fracunbound ):
    fig = plt.figure()
    plot = plt.plot( time, fracunbound, lw=2 )
    plt.xlabel('Time (days)', fontsize=25 )
    plt.ylabel('Ejection Efficiency', fontsize=25 )
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.tight_layout()
    # saveas = writepath + 'unbound_' + simname + '.pdf'
    saveas = 'unbound.pdf'
    fig.savefig(saveas)
    print('Saved plot ' + saveas)
    plt.clf()

def plotOrbEl( time, sep, a, ecc, boolArray, velCMnorm, posCMx, posCMy, posCMz, posPrimx, posPrimy, posPrimz, posCompx, posCompy, posCompz ):
    fig = plt.figure(figsize=(9,9))

    plt.subplot(2,2,1)
    plt.plot(time, sep, c='b', lw=2 )
    # plt.plot(time, periapse, c='g')
    # plt.plot(time, apoapse, c='c')
    plt.plot(time[boolArray], a[boolArray], c='r', lw=2 )
    # plt.axis([0., 120., 0., 54.])
    plt.xlabel('Time (days)', fontsize=20 )
    plt.ylabel(r'Distance ($R_{\odot}$)', fontsize=20 )
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.title('Separation', fontsize=20)

    plt.subplot(2,2,3)
    plt.plot( posPrimx, posPrimy, c='g', lw=2, label='Primary' )
    plt.plot( posCompx, posCompy, c='b', lw=2, label='Companion' )
    plt.plot( posCMx, posCMy, c='r', lw=2, label='CM' )
    plt.legend()
    plt.xlabel('x (cm)', fontsize=20)
    plt.ylabel('y (cm)', fontsize=20)
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.title('Positions',fontsize=20)

    plt.subplot(2,2,4)
    plt.plot(time, velCMnorm, lw=2)
    plt.xlabel('Time (days)',fontsize=20 )
    plt.ylabel('CM Velocity (km/s)',fontsize=20)
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.title('CM Velocity',fontsize=20)

    plt.subplot(2,2,2)
    plt.plot(time[boolArray], ecc[boolArray], lw=2)
    plt.xlabel('Time (days)',fontsize=20 )
    plt.ylabel('Eccentricity',fontsize=20)
    plt.xticks( fontsize=20)
    plt.yticks( fontsize=20)
    plt.title('Eccentricity',fontsize=20)

    plt.tight_layout()

    # saveas = writepath + 'orbel_' + simname + '.pdf'
    saveas = 'orbel.pdf'
    fig.savefig(saveas)
    print('Saved figure ' + saveas)

    plt.clf()

def findAE( numsets, sep ):
    sys.stdout.write('Getting semi-major axis & eccentricity ... ')
    sys.stdout.flush()

    nframes = numsets
    ecc = np.zeros(nframes)
    is_peri = np.full(nframes, False, dtype = bool)
    is_apo = np.full(nframes, False, dtype = bool)
    periapse = np.zeros(nframes)
    apoapse = np.zeros(nframes)
    peridomain = np.zeros(nframes)
    apodomain = np.zeros(nframes)
    a = np.zeros(nframes)

    periapse[0] = sep[0]
    apoapse[0] = sep[0]
    a[0] = sep[0]
    pericount = 0
    apocount = 0
    peridomain[0] = 0
    apodomain[0] = 0
    is_peri[0] = True
    is_apo[0] = True
    is_peri[nframes-1] = True
    is_apo[nframes-1] = True
    for k in range(1,nframes-1):
    	if( sep[k] > sep[k-1] and sep[k] > sep[k+1]):
    		is_apo[k] = True
    		apocount = apocount + 1
    		apodomain[apocount] = k
    	if( sep[k] < sep[k-1] and sep[k] < sep[k+1]):
    		is_peri[k] = True
    		pericount = pericount + 1
    		peridomain[pericount] = k
    apodomain[apocount+1] = nframes-1
    peridomain[pericount+1] = nframes-1

    apocount = 0
    pericount = 0
    boolArray = np.zeros( nframes, dtype=bool )
    for m in range(1,nframes):
    	apoapse[m] = np.interp(m, [apodomain[apocount], apodomain[apocount+1]],
    		[sep[int(apodomain[apocount])], sep[int(apodomain[apocount+1])]])
    	periapse[m] = np.interp(m, [peridomain[pericount], peridomain[pericount+1]],
    		[sep[int(peridomain[pericount])], sep[int(peridomain[pericount+1])]])
    	if (apodomain[apocount+1] == nframes-1) or (peridomain[pericount+1] == nframes-1) :
    		a[m] = 0.
    		ecc[m] = 0.
    	elif (apodomain[apocount] == 0 or peridomain[pericount] == 0) :
    		a[m] = 0.
    		ecc[m] = 0.
    	else :
    		a[m] = (apoapse[m] + periapse[m]) / 2.0
    		ecc[m] = (apoapse[m] - periapse[m]) / (apoapse[m] + periapse[m])
    		boolArray[m] = True
    	if is_apo[m]:
    		apocount = apocount + 1
    	if is_peri[m]:
    		pericount = pericount + 1

    print('done')
    return a, ecc, boolArray

if args.unbound :
    plotUnbound( time, fracunbound )
if args.mass :
    plotMass( time, massGasTot )
if args.orbel :
    a, ecc, boolArray = findAE( numsets, sep )
    plotOrbEl( time, sep, a, ecc, boolArray, velCMnorm, posCMx, posCMy, posCMz, posPrimx, posPrimy, posPrimz, posCompx, posCompy, posCompz )
