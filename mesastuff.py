from __main__ import *
import mesa_reader as mr

def getMesa( profileFile ) :
    data = mr.MesaData(profileFile)

    logT   = data.logT
    mass   = data.mass
    logR   = data.logR
    logRho = data.logRho
    logP   = data.logP

    mass = mass * Msun
    T = np.power(10.,logT)
    P = np.power(10.,logP) / G
    radius = np.power(10.,logR)
    rSun = 7e10
    radius = radius * rSun
    rho = np.power(10.,logRho)

    return T, mass, radius, rho, P

def getMesaEnt( profileFile ) :
	data = mr.MesaData(profileFile)

	logT = data.logT
	mass = data.mass
	mass = mass*Msun
	logP = data.logP
	logR = data.logR

	T = np.power(10.,logT)
	P = np.power(10.,logP) / G

	dm = np.zeros(len(mass))
	for i in range(0,len(mass)-1) :
		dm[i] = mass[i] - mass[i+1]
	dm[len(mass)-1] = mass[len(mass)-1]

	ent = R * ( 5./2. + np.log( np.power(k*T,2.5) / P /h/h/h * np.power(2. * math.pi * mpart, 1.5) ) )

	return ent, dm

def getMesaEnt2( profileFile ) :
	data = mr.MesaData(profileFile)

	logT = data.logT
	mass = data.mass
	mass = mass*Msun
	logP = data.logP
	logR = data.logR
	logRho = data.logRho

	P = np.power(10.,logP) / G
	rho = np.power(10.,logRho)

	# dm = np.zeros(len(mass))
	# for i in range(0,len(mass)-1) :
	# 	dm[i] = mass[i] - mass[i+1]
	# dm[len(mass)-1] = mass[len(mass)-1]

	ent = np.divide( P, np.power( rho, gamma ) )

	return ent
