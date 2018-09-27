from __main__ import *
import yt
if latex :
	import matplotlib
	matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from timestuff import *
from berniter import *

#########################################################

num = 1000000 + dataset
numstr = str(num)
cut = numstr[1:7]
ds = yt.load(readpath + outprefix + cut, bounding_box = hbox, n_ref=nref )

time = getTime(ds)

plot = yt.ProjectionPlot(ds, densanim_direction, ('gas', 'density'), width = densanim_plotwidth, fontsize=35 )

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
	posCM, velCM = getCM(ds, IE=useIE)
	plot.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
	plot.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')
	plot.annotate_marker( posCM*cl, coord_system = 'data', plot_args={'color':'black'}, marker = '*')

snapshot_saveas = writepath + densanim_direction + '_snap_' + simname + '_ds' + str(dataset) + '.png'
plot.save(snapshot_saveas)
print 'snapshot: Saved projection ' + snapshot_saveas

###################### PAPER MODE ###################################

# from mpl_toolkits.axes_grid1 import AxesGrid

# npanes = len(framearray)

# fig = plt.figure() # (figsize=(9,12))
# grid = AxesGrid( fig, rect=(0.1,0.1,0.8,0.8), nrows_ncols=(2,3), cbar_mode='single', \
# 	cbar_location='right', share_all=True, cbar_size='2%', label_mode='L' )

# sets = np.chararray( npanes, itemsize = 100 )
# for i in range(0,npanes) :
# 	dataset = framearray[i]
# 	num = 1000000 + dataset
# 	numstr = str(num)
# 	cut = numstr[1:7]
# 	sets[i] = outprefix + cut

# for i, file in enumerate(sets) :
# 	dataset = framearray[i]
# 	print 'dataset: ' + str(dataset)
# 	ds = yt.load(readpath + file, bounding_box = hbox, n_ref=nref )

# 	time = getTime(ds)

# 	plot = yt.ProjectionPlot(ds, densanim_direction, ('gas', 'density'), width = densanim_plotwidth )
# 	ds.define_unit('Solar_Radii',(Rsun,'cm'))
# 	plot.set_axes_unit('Solar_Radii')

# 	if densanim_fixlimits:
# 		plot.set_zlim('density',densanim_lowlim,densanim_highlim)

# 	# plot.annotate_clear()
# 	plot.annotate_timestamp( time_unit = timelabel, draw_inset_box = False )

# 	if do_marks :
# 		ad = ds.all_data()
# 		dm_pos = ad[('DarkMatter','Coordinates')]
# 		core = dm_pos[0][:]
# 		comp = dm_pos[1][:]
# 		# cl = ds.arr(1.0, 'code_length')
# 		# posCM, velCM = getCM(ds, IE=useIE)
# 		plot.annotate_marker( core, coord_system = 'data', plot_args={'color':'black'}, marker = '+')
# 		plot.annotate_marker( comp, coord_system = 'data', plot_args={'color':'black'}, marker = 'x')
# 		# plot.annotate_marker( posCM*cl, coord_system = 'data', plot_args={'color':'black'}, marker = '*')

# 	p = plot.plots['density']
# 	p.figure = fig
# 	p.axes = grid[i].axes
# 	p.cax = grid.cbar_axes[0]
# 	# cbar = fig.colorbar(p, cax=p.cax, orientation='horizontal')
# 	plot._setup_plots()

# snapshot_saveas = writepath + densanim_direction + '_6snap_' + simname + '.png'
# plt.savefig(snapshot_saveas)
# print 'snapshot: Saved projection ' + snapshot_saveas
