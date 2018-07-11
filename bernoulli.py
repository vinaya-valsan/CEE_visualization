from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from yt import YTQuantity
from berniter import *

userho = 0

if bern_fixlimits:
	sizingappend = ''
else:
	sizingappend = '_sizing'

gamma = 5.0/3.0
G = 6.674e-8
R = 8.314e7 / G
Rsun = 7.0e10
Msun = 2.0e33

# create figure
ts = yt.load( readpath + 'star.out.00000' + str(startingset) )

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

yt.add_field(('Gas','bernoulli'), function = _bern, particle_type = True )

plot = yt.ParticlePlot(ts, ('Gas','particle_position_x'), ('Gas','particle_position_y'), \
	('Gas','bernoulli'), width = bern_plotwidth )

if (dDelta > 5.0):
	timelabel = 'day'
else:
	timelabel = 'hr'

if bern_fixlimits:
	plot.set_zlim('all',0.9,bern_highlim)

fig = plot.plots['bernoulli'].figure

# create frames
def animate(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'bernoulli: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
	ds = yt.load(readpath + 'star.out.' + cut)

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
	
# create animation object
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
bern_saveas = writepath + 'bern_' + simname + sizingappend + '.mp4'
anim.save(bern_saveas)
print 'bern: Saved animation ' + bern_saveas
