import numpy as np
from multiprocessing import Process

from config.test_config import *

def rp_mult():
	import radprof_mult
def tp_mult():
	import tempprof_mult
def ct():
	import coretemp
def rp():
	import radprof
def tp():
	import tempprof
def dens():
	import densanim
def ps():
	import partslice

if do_comparison:

	if do_radprof:
		print '\nStarting Radial Density Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		p1 = Process(target = rp_mult)
		p1.start()
		
	if do_tempprof:
		print '\nStarting Radial Temperature Profile '+str(nrows)+' x '+str(ncolumns)+' ( '+comparison_name+' )\n'
		p2 = Process(target = tp_mult)
		p2.start()
		
	if do_radprof:
		p1.join()
	if do_tempprof:
		p2.join()
	
else:
	
	nproc = do_coretemp + do_radprof + do_tempprof + do_densanim + do_partslice
	if (nproc > maxproc):
		print '\n Terminating: too many processes \n'
		import sys
		sys.exit(0)
	
	if do_coretemp:
		print '\nStarting Core Temperature ( ' + simname + ' )\n'
		p3 = Process(target = ct)
		p3.start()

	if do_radprof:
		print '\nStarting Radial Density Profile ( ' + simname + ' )\n'
		p4 = Process(target = rp)
		p4.start()
	
	if do_tempprof:
		print '\nStarting Radial Temperature Profile ( ' + simname + ' )\n'
		p5 = Process(target = tp)
		p5.start()
	
	if do_densanim:
		print '\nStarting Density Projection ( ' + simname + ' )\n'
		p6 = Process(target = dens)
		p6.start()
	
	if do_partslice:
		print '\nStarting Particle Slice ( ' + simname + ' )\n'
		p7 = Process(target = ps)
		p7.start()
		
	if do_coretemp:
		p3.join()
	if do_radprof:
		p4.join()
	if do_tempprof:
		p5.join()
	if do_densanim:
		p6.join()
	if do_partslice:
		p7.join()
