from __main__ import *
import yt
import matplotlib
matplotlib.rc("text", usetex=True)
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from timestuff import *

coretemp_dotsize = 10

coretemp = np.zeros(nframes)
time = np.zeros(nframes)

for i in range(0,nframes):
	
	num = i*frameskip + 1000000 + startingset
	numstr = str(num)
	cut = numstr[1:7]
	print 'coretemp: ' + simname + ' Data Set ' + cut
	
	ds = yt.load(readpath + outprefix + cut, bounding_box = hbox )
	ad = ds.all_data()
	
# 	coretemp[i] = 1.6e-24/1.38e-16 * ad[('Gas','Temperature')].max()
	coretemp[i] = ad[('Gas','Temperature')].max()
	time[i], timelabel = getTime(ds, i)

plt.clf()
plt.scatter(time,coretemp,s= coretemp_dotsize )
	
plt.xlabel( 'Time (' + timelabel + ')' )
plt.ylabel('Core Temperature (K)')
plt.title(simname + ' Core Temperature')
coretemp_saveas = writepath + 'coretemp_' + simname + '.pdf'
plt.savefig(coretemp_saveas)
print 'coretemp: Saved figure ' + coretemp_saveas
plt.clf()
