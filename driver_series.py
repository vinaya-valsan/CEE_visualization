import numpy as np
import math
from template_config import *

# SPECIFY CONFIG FILE HERE
from config.rg_config import *

lim = dPeriod / 2. * 1.0001
hbox = np.array([[-lim,lim],[-lim,lim],[-lim,lim]])

if do_comparison:

	if do_radprof:
		print '\nStarting Radial Density Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		import radprof_mult
		
	if do_tempprof:
		print '\nStarting Radial Temperature Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		import tempprof_mult
	
else:

	if do_coretemp:
		print '\nStarting Core Temperature ( ' + simname + ' )\n'
		import coretemp

	if do_radprof:
		if do_snapshot:
			print '\nStarting Radial Density Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			import radprof_snapshot
		else:
			print '\nStarting Radial Density Profile ( ' + simname + ' )\n'
			import radprof
	
	if do_tempprof:
		if do_snapshot:
			print '\nStarting Radial Temperature Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			import tempprof_snapshot
		else:
			print '\nStarting Radial Temperature Profile ( ' + simname + ' )\n'
			import tempprof
	
	if do_densanim:
		if do_snapshot:
			print '\nStarting ' + densanim_direction + ' Density Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			import snapshot
		else:
			print '\nStarting ' + densanim_direction + ' Density Projection ( ' + simname + ' )\n'
			import densanim
	
	if do_partslice:
		print '\nStarting '+partslice_direction+' '+partslice_parttype+' Particle Slice ( '+simname+' )\n'
		import partsliceanim

	if do_orbel:
		print '\nStarting Orbital Elements ( ' + simname + ' )\n'
		import orbel

	if do_energies:
		print '\nStarting Energy Budget ( ' + simname + ' )\n'
		import energies

	if do_entropy:
		if do_snapshot:
			print '\nStarting Radial Entropy Profile Snapshot ( ' + simname + ' ) Data Set ' + str(dataset) + '\n'
			import entprof_snapshot
		else:
			print '\nStarting Radial Entropy Profile ( ' + simname + ' )\n'
			import entprof

	if do_bernoulli:
		print '\nStarting Bernoulli Constant ( ' + simname + ' )\n'
		import bernoulli

	if do_enercomp:
		print '\nStarting Energy Breakdown ( ' + simname + ' ) \n'
		import enercomp

	# if do_velpart:
	# 	print '\nStarting Velocity Particle Plot ( ' + simname + ' ) \n'
	# 	import velpart
