import numpy as np
import math
from template_config import *
from multiprocessing import Process

# SPECIFY CONFIG FILE HERE
from config.cee_ohlmann_config import *

lim = dPeriod / 2. * 1.0001
hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

def rp_mult():
	import radprof_mult
def tp_mult():
	import tempprof_mult
def ctemp():
	import coretemp
def rp():
	import radprof
def tp():
	import tempprof
def dens():
	import densanim
def snap():
	import snapshot
def snap_rad():
	import radprof_snapshot
def snap_temp():
	import tempprof_snapshot
def snap_ent():
	import entprof_snapshot
def densx():
	densanim_direction = 'x'
	import densanim
def densy():
	densanim_direction = 'y'
	import densanim
def densz():
	densanim_direction = 'z'
	import densanim
def ps():
	import partslice
def orb():
	import orbel
def ener():
	import energies
def ent():
	import entprof
def bern():
	import bernoulli
def ec():
	import enercomp

if do_comparison:

	nproc = do_radprof + do_tempprof + do_densanim * 3
	if (nproc > maxproc):
		print '\n Terminating: too many processes \n'
		import sys
		sys.exit(0)

	if do_radprof:
		print '\nStarting Radial Density Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		p_rpm = Process(target = rp_mult)
		p_rpm.start()
		
	if do_tempprof:
		print '\nStarting Radial Temperature Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		p_tpm = Process(target = tp_mult)
		p_tpm.start()

	if do_densanim:
		print '\nStarting Density Projection (All Directions) ( ' + simname + ' )\n'

		densanim_direction = 'x'
		p_dx = Process(target = densx)
		p_dx.start()

		densanim_direction = 'y'
		p_dy = Process(target = densy)
		p_dy.start()

		densanim_direction = 'z'
		p_dz = Process(target = densz)
		p_dz.start()
		
	if do_radprof:
		p_rpm.join()
	if do_tempprof:
		p_tpm.join()
	if do_densanim:
		p_dx.join()
		p_dy.join()
		p_dz.join()
	
else:
	
	nproc = do_coretemp + do_radprof + do_tempprof + do_densanim + do_partslice + do_orbel \
		+ do_energies + do_entropy + do_bernoulli + do_enercomp

	if (nproc > maxproc):
		print '\n Terminating: too many processes \n'
		import sys
		sys.exit(0)
	
	if do_coretemp:
		print '\nStarting Core Temperature ( ' + simname + ' )\n'
		p_ctemp = Process(target = ctemp)
		p_ctemp.start()

	if do_radprof:
		if do_snapshot:
			print '\nStarting Radial Density Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			p_snap_rad = Process(target = snap_rad)
			p_snap_rad.start()
		else:
			print '\nStarting Radial Density Profile ( ' + simname + ' )\n'
			p_rp = Process(target = rp)
			p_rp.start()
	
	if do_tempprof:
		if do_snapshot:
			print '\nStarting Radial Temperature Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			p_snap_temp = Process(target = snap_temp)
			p_snap_temp.start()
		else:
			print '\nStarting Radial Temperature Profile ( ' + simname + ' )\n'
			p_tp = Process(target = tp)
			p_tp.start()
	
	if do_densanim:
		if do_snapshot:
			print '\nStarting ' + densanim_direction + ' Density Snapshot ( ' + simname + ' ) Frame ' + str(dataset) + '\n'
			p_snap = Process(target = snap)
			p_snap.start()
		else:
			print '\nStarting ' + densanim_direction + ' Density Projection ( ' + simname + ' )\n'
			p_d = Process(target = dens)
			p_d.start()
	
	if do_partslice:
		print '\nStarting '+partslice_direction+' '+partslice_parttype+' Particle Slice ( '+simname+' )\n'
		p_ps = Process(target = ps)
		p_ps.start()

	if do_orbel:
		print '\nStarting Orbital Elements ( ' + simname + ' )\n'
		p_orb = Process(target = orb)
		p_orb.start()

	if do_energies:
		print '\nStarting Energy Budget ( ' + simname + ' )\n'
		p_ener = Process(target = ener)
		p_ener.start()

	if do_entropy:
		if do_snapshot:
			print '\nStarting Radial Entropy Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			p_snap_ent = Process(target = snap_ent)
			p_snap_ent.start()
		else:
			print '\nStarting Radial Entropy Profile ( ' + simname + ' )\n'
			p_ent = Process(target = ent)
			p_ent.start()

	if do_bernoulli:
		print '\nStarting Bernoulli Constant ( ' + simname + ' )\n'
		p_bern = Process(target = bern)
		p_bern.start()

	if do_enercomp:
		print '\nStarting Energy Breakdown ( ' + simname + ' ) \n'
		p_ec = Process(target = ec)
		p_ec.start()
		
	if do_coretemp:
		p_ctemp.join()
	if do_radprof:
		if do_snapshot:
			p_snap_rad.join()
		else:
			p_rp.join()
	if do_tempprof:
		if do_snapshot:
			p_snap_temp.join()
		else:
			p_tp.join()
	if do_densanim:
		if do_snapshot:
			p_snap.join()
		else:
			p_d.join()
	if do_partslice:
		p_ps.join()
	if do_orbel:
		p_orb.join()
	if do_energies:
		p_ener.join()
	if do_entropy:
		if do_snapshot:
			p_snap_ent.join()
		else:
			p_ent.join()
	if do_bernoulli:
		p_bern.join()
	if do_enercomp:
		p_ec.join()
