import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.image as mpimg
import matplotlib.animation as animation
import math
from template_config import *

# SPECIFY CONFIG FILE HERE
from config.paper_config import *

fig = plt.figure() # (figsize=(9,7))

if do_densanim :
	fileprefix = densanim_direction
	writename = densanim_direction + '_dens_'
elif do_bernoulli :
	fileprefix = 'bern'
	writename = 'bern_'

def animate(i):
	plt.clf()
	dataset = i * frameskip + startingset
	file = fileprefix + '_snap_' + simname + '_ds' + str(dataset) + '.png'
	img = mpimg.imread( framepath + file )
	imgplot = plt.imshow(img)
	plt.axis('off')
	# plt.tight_layout()
	print('mergeanim: Added file ' + file)
	return imgplot

anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
saveas = writepath + writename + simname + '.mp4'
anim.save( saveas, dpi=500 )
print('mergeanim: Saved animation ' + saveas)
