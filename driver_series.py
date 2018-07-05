import numpy as np

from config.test_config import *

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
		print '\nStarting Radial Density Profile ( ' + simname + ' )\n'
		import radprof
	
	if do_tempprof:
		print '\nStarting Radial Temperature Profile ( ' + simname + ' )\n'
		import tempprof
	
	if do_densanim:
		if do_snapshot:
			print '\nStarting ' + densanim_direction + ' Density Snapshot ( ' + simname + ' ) Frame ' + str(dataset) + '\n'
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
