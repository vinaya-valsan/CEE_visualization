from __main__ import *
import yt

# import mesa_reader as mr

def getTime( ds, iter, cutoff=5.0 ) :

	time = ds.current_time
	ratio = time / frameskip / (iter + 1)

	if ratio > cutoff :
		label = 'day'
	else :
		label = 'hr'

	time = time.in_units(label)

	return time, label

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

def getEnt( ds ) :
	ad = ds.all_data()
	K = ds.arr(1.0,'K')
	g = ds.arr(1.0,'g')
	cl = ds.arr(1.0,'code_length')

	T = ad[('gas','temperature')]/K
	mass = ad[('gas','cell_mass')]/g
	V = ad[('gas','cell_volume')]/cl/cl/cl

	ent = R * ( 5./2. + np.log( np.divide(V,mass) / R /h/h/h * k**2.5 * np.power( 2. * math.pi * mpart * T, 1.5 ) ) )

	return ent

def getEnt2( ds ) :
	ad = ds.all_data()
	K = ds.arr(1.0,'K')
	g = ds.arr(1.0,'g')
	cl = ds.arr(1.0,'code_length')

	T = ad[('gas','temperature')]/K
	mass = ad[('gas','cell_mass')]/g
	V = ad[('gas','cell_volume')]/cl/cl/cl
	rho = np.divide(mass, V)

	ent = R * np.divide(T, np.power(rho, gamma-1) )

	return ent

def getEnt3( ds ) :
	ad = ds.all_data()
	K = ds.arr(1.0,'K')
	g = ds.arr(1.0,'g')
	cl = ds.arr(1.0,'code_length')

	ie = ad[('Gas','ie')]
	rho = ad[('Gas','rho')]

	T = ad[('Gas','Temperature')]
	ie = gamma/(gamma-1.) * R * T

	ent = (gamma-1) * np.divide(ie, np.power(rho, gamma-1) )

	return ent
