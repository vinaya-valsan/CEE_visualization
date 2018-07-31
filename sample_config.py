maxproc = 3 # use no more than 3 threads
readpath = '/Users/ljprust/data/ce/ohlmann/mm_amr/' # path to data
writepath = '/Users/ljprust/data/testplots/' # where the output will go
simname = 'blah' # name of the simulation (can be whatever you want)
nframes = 7 # the number of data sets to analyze, starting from the startingset
startingset = 5 # the first data set
frameskip = 5 # do every fifth data set (5, 10, 15, 20, 25, 30, 35)
period = 200 # number of milliseconds of each frame in the animations
dPeriod = 1.4e14 # what is the side length of the simulation box?
nref = 16 # resolution of any mesh plots (1 is highest resolution, 64 is lowest (I think))

# CORETEMP
do_coretemp = 1 # create a plot showing the core temperature of the star as a function of time

# RADPROF
do_radprof = 1 # create an animation of the radial density profile over time
radprof_fixaxes = 0 # do not fix the axes of the plot; let them float
radprof_axes = [1.0e10, 1.0e13, 1.0e-8, 1.0e-1] # the axes of the plot
corecorrect = 0 # if the core is a dark matter particle, set it as the origin of coordinates

# DENSANIM
do_densanim = 1 # create a projection plot of the density
densanim_direction = 'z' # the axis to project along
densanim_plotwidth = 4.0e13 # the width of the plot window
densanim_fixlimits = 1 # set limits on the colorbar
densanim_lowlim = 6.0e4 # lower limit on the colorbar
densanim_highlim = 4.0e8 # upper limit on the colorbar
