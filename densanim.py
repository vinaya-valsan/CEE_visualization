from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation
from berniter import *
from timestuff import *

if densanim_fixlimits:
	sizingappend = ''
else:
	sizingappend = '_sizing'

# create figure
ts = yt.load( readpath + 'star.out.00000' + str(startingset) )
plot = yt.ProjectionPlot(ts, densanim_direction, ('gas', 'density'), width = densanim_plotwidth )

time, timelabel = getTime(ts, 0)

if densanim_fixlimits:
	plot.set_zlim('all',densanim_lowlim,densanim_highlim)
	
fig = plot.plots['density'].figure

# create frames
def animate(i):
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'densanim: ' + simname + ' Frame ' + str(i) + ' Data Set ' + cut
	
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
densanim_saveas = writepath + densanim_direction + '_dens_' + simname + sizingappend + '.mp4'
anim.save(densanim_saveas)
print 'densanim: Saved animation ' + writepath + densanim_direction + '_dens_' + simname + sizingappend + '.mp4'
