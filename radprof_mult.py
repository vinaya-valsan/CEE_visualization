from __main__ import *
import yt
import matplotlib
matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
from timestuff import *

readpath = np.chararray(9, itemsize = 100)
readpath[1] = readpath1
readpath[2] = readpath2
readpath[3] = readpath3
readpath[4] = readpath4
readpath[5] = readpath5
readpath[6] = readpath6
readpath[7] = readpath7
readpath[8] = readpath8

title = np.chararray(9, itemsize = 100)
title[1] = title1
title[2] = title2
title[3] = title3
title[4] = title4
title[5] = title5
title[6] = title6
title[7] = title7
title[8] = title8

radprof_dotsize = 1
time = np.zeros(nframes)

if radprof_fixaxes:
	sizingappend = ''
else:
	sizingappend = '_sizing'

if nrows == 1:
	fig_y = 6
else:
	fig_y = 9
	
if ncolumns == 1:
	fig_x = 6
elif ncolumns == 2:
	fig_x = 12
else:
	fig_x = 15

fig = plt.figure(figsize=(fig_x,fig_y))

def animate(i):
	plt.clf()
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'radprof_mult: ' + comparison_name + ' Frame ' + str(i) + ' Data Set ' + cut
	
	time[i], timelabel = getTime(ds, i)
	
	for j in range(1,nplots+1):
		
		plt.subplot( nrows, ncolumns, j )
		
		if (readpath[j] != '') :
			
			ds = yt.load(readpath[j] + outprefix + cut, bounding_box = hbox )
			ad = ds.all_data()
			pos = ad[('Gas','Coordinates')]
			if corecorrect :
				corepos = ad[('DarkMatter','Coordinates')]
				pos = pos - corepos
			radius = np.linalg.norm(pos, axis=1)
			density = ad[('Gas','density')]
			plt.scatter( radius, density, s= radprof_dotsize )
		
		plt.xscale('log')
		plt.yscale('log')
	
		if radprof_fixaxes:
			plt.axis(radprof_axes)
		
		if j > ncolumns * (nrows - 1):
			plt.xlabel('Radius (cm)')
		
		if (j == 1) or (j == 1 + ncolumns) or (j == 1 + 2*ncolumns) or (j == 1 + 3*ncolumns):
			plt.ylabel('Density (g/cm^3)')
	
		if j == 1:
			plt.title(title1 + ' Radial Density Profile ' + cut + ' Time: ' + str(time[i])[0:5] + ' ' + timelabel )
		else:
			plt.title(title[j])
	
anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
radprof_mult_saveas = writepath + 'radprof_' + comparison_name + sizingappend + '.mp4'
anim.save(radprof_mult_saveas)
print 'radprof_mult: Saved animation ' + radprof_mult_saveas
