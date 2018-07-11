from __main__ import *
import yt
import mesa_reader as mr

def getTime( ds, iter, cutoff=5.0 ) :

	time = ds.current_time
	ratio = time / frameskip / (iter + 1)
	if ratio > cutoff :
		label = 'day'
	else :
		label = 'hr'
	time = time.in_units(label)
	return time

def getTimeLabel( ds, iter, cutoff=5.0 ) :

	time = ds.current_time
	ratio = time / frameskip / (iter + 1)
	if ratio > cutoff :
		label = 'day'
	else :
		label = 'hr'
	return label

def getMesa( profileFile ) :
    data = mr.MesaData(profileFile)

    logT   = data.logT
    mass   = data.mass
    logR   = data.logR
    logRho = data.logRho

    T = np.power(10.,logT)
    R = np.power(10.,logR)
    rSun = 7e10
    R = R * rSun
    rho = np.power(10.,logRho)

    return T, mass, R, rho