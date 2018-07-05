from __main__ import *
import yt
import matplotlib.pyplot as pl
import matplotlib.animation as animation

if (dDelta > 5.0):
	timelabel = 'day'
else:
	timelabel = 'hr'

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + 'star.out.' + cut)

plot = yt.ProjectionPlot(ds, densanim_direction, ('gas', 'density'), width = densanim_plotwidth )

if densanim_fixlimits:
	plot.set_zlim('all',densanim_lowlim,densanim_highlim)

plot.annotate_clear()
plot.annotate_timestamp(time_unit = timelabel)

if do_marks :
	ad = ds.all_data()
	dm_pos = ad[("DarkMatter","Coordinates")]
	core = dm_pos[0][:]
	comp = dm_pos[1][:]
	plot.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
	plot.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')

snapshot_saveas = writepath + densanim_direction + '_snap_' + simname + '_ds' + str(dataset) + '.pdf'
plot.save(snapshot_saveas)
print 'snapshot: Saved projection ' + writepath + densanim_direction + '_snap_' + simname + '_ds' + str(dataset) + '.pdf'
