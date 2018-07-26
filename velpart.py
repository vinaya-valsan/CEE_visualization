from __main__ import *
import yt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from yt import YTQuantity
from berniter import *
from timestuff import *

userho = 0

if velpart_fixlimits:
	sizingappend = ''
else:
	sizingappend = '_sizing'

num = 1000000 + startingset
numstr = str(num)
cut = numstr[1:7]

ts = yt.load(readpath + outprefix + cut, bounding_box = hbox )

cv = ts.arr(1.0, 'code_velocity')

def _vnorm(field, data) :
	vel = data[('Gas','Velocities')] / cv
	posCM, vCM = getCM(data.ds)
	vnorm = np.linalg.norm(vel - vCM, axis=1)
	return vnorm

yt.add_field(('Gas','vnorm'), function = _vnorm, particle_type = True )

plot = yt.ParticlePlot(ts, ('Gas','particle_position_x'), ('Gas','particle_position_y'), \
	('Gas','vnorm'), width = velpart_plotwidth )

time, timelabel = getTime(ts, 0)

if velpart_fixlimits:
	plot.set_zlim('all',velpart_lowlim,bern_highlim)

fig = plot.plots['vnorm'].figure

def animate(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'velpart: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
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
velpart_saveas = writepath + 'velpart_' + simname + sizingappend + '.mp4'
anim.save(velpart_saveas)
print 'velpart: Saved animation ' + velpart_saveas
