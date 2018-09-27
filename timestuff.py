from __main__ import *
import yt
from yt import YTQuantity

def getTime( ds ) :

	ct = ds.arr( math.sqrt(G), 'code_time' )
	time = ds.current_time / ct
	sec = YTQuantity(1.0,'s')

	time = time * sec.in_units(timelabel)

	return time

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
