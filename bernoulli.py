from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from yt import YTQuantity
from berniter import *
from timestuff import *

userho = 0

if bern_fixlimits:
	sizingappend = ''
else:
	sizingappend = '_sizing'

num = 1000000 + startingset
numstr = str(num)
cut = numstr[1:7]

ts = yt.load(readpath + outprefix + cut, bounding_box = hbox )

cl = ts.arr(1.0, 'code_length')
cm = ts.arr(1.0, 'code_mass')
cv = ts.arr(1.0, 'code_velocity')
K = YTQuantity(1.0,'K')

def _bern(field, data) :
	PE = data[('Gas','Phi')]/cl
	posCM, velCM = getCM(data.ds)
	v = np.linalg.norm( data[('Gas','Velocities')]/cv - velCM, axis=1 )
	KE = 0.5*np.multiply(v,v)
	enthalpy = gamma / (gamma-1.0) * R * data[('Gas','Temperature')] / K
	bern = PE + KE + enthalpy
	bern = np.clip( -bern, 1.0, None )
	if userho :
		rho = data[('Gas','rho')]
		bern = np.multiply( bern, rho )
	return bern

def _bernbound(field, data) :
	PE = data[('Gas','Phi')]/cl
	posCM, velCM = getCM(data.ds)
	v = np.linalg.norm( data[('Gas','Velocities')]/cv - velCM, axis=1 )
	KE = 0.5*np.multiply(v,v)
	enthalpy = gamma / (gamma-1.0) * R * data[('Gas','Temperature')] / K
	bern = PE + KE + enthalpy
	bern = np.clip( -bern, 1.0e-15, 1.0e2 )
	return bern

yt.add_field(('Gas','bernoulli'), function = _bern, particle_type = True )
yt.add_field(('Gas','bern_bound'), function = _bernbound, particle_type = True )

time, timelabel = getTime(ts, 0)

#############################################################################################

plot = yt.ParticlePlot(ts, ('Gas','particle_position_x'), ('Gas','particle_position_y'), \
	('Gas','bernoulli'), width = bern_plotwidth )

if bern_fixlimits:
	plot.set_zlim('all',0.9,bern_highlim)

fig = plot.plots['bernoulli'].figure

def animate(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'bernoulli: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

	plot.annotate_clear()
	plot.annotate_timestamp(time_unit = timelabel)

	if do_marks :
		ad = ds.all_data()
		dm_pos = ad[('DarkMatter','Coordinates')]
		core = dm_pos[0][:]
		comp = dm_pos[1][:]
		cl = ds.arr(1.0, 'code_length')
		posCM, velCM = getCM(ds)
		plot.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
		plot.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')
		plot.annotate_marker( posCM*cl, coord_system = 'data', plot_args={'color':'black'}, marker = '*')
	
	plot._switch_ds(ds)
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
bern_saveas = writepath + 'bern_' + simname + sizingappend + '.mp4'
anim.save(bern_saveas)
print 'bern: Saved animation ' + bern_saveas

#############################################################################################

pl.clf()
plot2 = yt.ParticlePlot(ts, ('Gas','particle_position_x'), ('Gas','particle_position_y'), \
	('Gas','bern_bound'), width = bern_plotwidth )

plot2.set_zlim('all',99.0,1.0e2)

fig2 = plot2.plots['bern_bound'].figure

def animate2(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'bern_bound: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )

	plot2.annotate_clear()
	plot2.annotate_timestamp(time_unit = timelabel)

	if do_marks :
		ad = ds.all_data()
		dm_pos = ad[('DarkMatter','Coordinates')]
		core = dm_pos[0][:]
		comp = dm_pos[1][:]
		cl = ds.arr(1.0, 'code_length')
		posCM, velCM = getCM(ds)
		plot2.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
		plot2.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')
		plot2.annotate_marker( posCM*cl, coord_system = 'data', plot_args={'color':'black'}, marker = '*')
	
	plot2._switch_ds(ds)
	
anim2 = animation.FuncAnimation(fig2, animate2, frames = nframes, interval = period, repeat = False)
bern_saveas = writepath + 'bound_' + simname + '.mp4'
anim2.save(bern_saveas)
print 'bern: Saved animation ' + bern_saveas

#############################################################################################

fig = pl.figure()

time = np.zeros(nframes)

def animate(i):
	pl.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'bernprof: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()
	pos = ad[('Gas','Coordinates')]/cl

	posCM, velCM = getCM(ds)
	
	radius = np.linalg.norm(pos - posCM, axis=1)
	bern = ad[('Gas','bernoulli')]
	time[i], timelabel = getTime(ds, i)
	
	scat = pl.scatter( radius, bern, s=1 )
	pl.xscale('log')
	
	pl.axis([1.0e8, 1.0e15, -1.0e22, 1.0e22])
	
	pl.xlabel('Radius (cm)')
	pl.ylabel('Bernoulli Constant')
	pl.title('Radial Bernoulli Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )

	pl.hlines( 0.0, 1.0, 1.0e16 )

	return scat
	pl.clf()
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
saveas = writepath + 'bernprof_' + simname + sizingappend + '.mp4'
anim.save(saveas)
print 'bernprof: Saved animation ' + saveas
