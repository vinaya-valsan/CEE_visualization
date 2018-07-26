from __main__ import *
import yt
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *
from berniter import *

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut, bounding_box = hbox, n_ref=nref )

time, timelabel = getTime(ds, dataset-1)

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
	cl = ds.arr(1.0, 'code_length')
	posCM, velCM = getCM(ds)
	plot.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
	plot.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')
	plot.annotate_marker( posCM*cl, coord_system = 'data', plot_args={'color':'black'}, marker = '*')

snapshot_saveas = writepath + densanim_direction + '_snap_' + simname + '_ds' + str(dataset) + '.png'
plot.save(snapshot_saveas)
print 'snapshot: Saved projection ' + snapshot_saveas
