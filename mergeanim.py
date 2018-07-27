import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.image as mpimg
import matplotlib.animation as animation
import math
from template_config import *

# SPECIFY CONFIG FILE HERE
from config.test_config import *

fig = plt.figure() # (figsize=(9,7))

def animate(i):
	plt.clf()
	dataset = i * frameskip + startingset
	file = densanim_direction + '_snap_' + simname + '_ds' + str(dataset) + '.png'
	img = mpimg.imread( framepath + file )
	imgplot = plt.imshow(img)
	plt.axis('off')
	print 'mergeanim: Added file ' + file
	return imgplot

anim = animation.FuncAnimation(fig, animate, frames = nframes, interval = period, repeat = False)
saveas = writepath + 'mergeanim_' + simname + '.mp4'
anim.save( saveas, dpi=500 )
print 'mergeanim: Saved animation ' + saveas
