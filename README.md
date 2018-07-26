DRIVERS: ---------------------------------------------------------------------------------------------

The driver imports the default configuration file and then the job-specific config file specified by the user. THE JOB-SPECIFIC CONFIG FILE MUST BE SPECIFIED IN THE DRIVER. Config files (other than the default) should be stored in a subdirectory called 'config', which must contain an empty file named '__init__.py'.

FUNCTION FILES: --------------------------------------------------------------------------------------

There are a few functions, contained in the files berniter and timestuff, that are called by many modules. They are:

-- getTime
    Gets the current time from the data set, and uses it along with the iteration number to figure out an appropriate unit for the time. Returns both the value (time) and unit (label).
    
-- getMesa
    Imports the data from a specified MESA file, converts it from logs to cgs units.
    
-- getCM
    Determines the position and velocity of the center of mass of the dark matter particles and BOUND gas combined. It does this via an iterative scheme that determines which particles are bound using the Bernoulli constant. Threshold and smoothing options determine the stopping criterion. Will crash if maxiter is exceeded.
    
MODULES: ---------------------------------------------------------------------------------------------
    
-- coretemp
    Plots the maximum temperature of the gas as a function of time. If the core of the star is a dark matter particle, the results will be nonsensical.
    
-- radprof
    Plots density vs radius from the origin of coordinates. The corecorrect option uses the position of the dark matter core as the origin, to correct for drifting of the DM particle. The plot_mesa option overplots the density profile of a specified MESA file.
    
-- "mult" files
    Used for comparing multiple simulations.
    
-- "snapshot" files
    Used for making a plot of only one frame rather than an animation of all of them. Can use partskip to skip some of the particles so that the image file isn't gigantic.
    
-- tempprof
    Plots temperature vs radius from the origin of coordinates. The corecorrect option uses the position of the dark matter core as the origin, to correct for drifting of the DM particle. The plot_mesa option overplots the temperature profile of a specified MESA file.
    
-- entprof
    Plots entprof vs radius from the origin of coordinates. The corecorrect option uses the position of the dark matter core as the origin, to correct for drifting of the DM particle. WIP: overplotting MESA data.
    
-- densanim
    Makes a projection plot of the density, with options for marking the DM core, DM companion, and the center of mass.
    
-- partsliceanim
    Same as densanim, but uses number density of H or He instead of mass density.
    
-- orbel
    CEE only. Plots the separation, semi-major axis, positions of the primary, companion, and CM, velocity of the CM, and eccentricity of the orbit.
    
-- energies
    CEE only. Makes a single plot of the different energy contributions to the system over time.
    
-- bernoulli
    CEE only. Makes a particle plot of the Bernoulli constant of the gas.
    
-- enercomp
    CEE only. Plots the energy distributions of each type of energy in the gas, as well as the Bernoulli constant. Also plots the amount of unbound material as a fraction of the total mass.
    
CONFIG PARAMETERS: -----------------------------------------------------------------------------------

-- maxproc
    Maximum number of threads allowed by the driver.
    
-- readpath
    Path to the data. (string)
    
-- writepath
    Path to where all the output will go. (string)
    
-- simname
    A name for the simulation (this will go in the names of all the output files). (string)
    
-- nframes
    Number of data sets you want to analyze.
    
-- frameskip
    The spacing in the data sets to be analyzed. (Every 1 set, every 5, etc.)
    
-- starting set
    What is the number of the first data set?
    
-- period
    The period of each animation frame, in milliseconds.
    
-- do_marks
    Mark the locations of the core, companion, and CM.
    
-- do_snapshot
    Take a snapshot of a specific frame instead of making an animation.
    
-- dataset
    If taking a snapshot, which data set should be used?
    
-- partskip
    If taking a snapshot, skip how many particles?
    
-- do_enercomp
    Use the enercomp module.
        ADD ENERCOMP OPTIONS LATER
        
-- do_bernoulli
    Use the bernoulli module.
    
        -- bern_fixlimits
            Specify an upper limit on the Bernoulli plot.
            
        -- bern_highlim
            Upper limit.
            
        -- bern_plotwidth
            Width of the Bernoulli plot in code units.
            
-- do_energies
    Use the energies module.
    
-- do_orbel
    Use the orbel module.
    
-- do_coretemp
    Use the coretemp module.
    
-- plot_mesa
    Overplot MESA data.
    
-- mesadata
    Which MESA file should be used? (string)
    
-- corecorrect
    Correct for the motion of the DM core in profile plots.
    
-- do_radprof
    Use the radprof module.
    
       -- radprof_fixaxes
            Specify axis limits.  
            
        -- radprof_axes
            Axis limits.
            
-- do_tempprof
    Use the tempprof module.
    
       -- tempprof_fixaxes
            Specify axis limits.
            
        -- tempprof_axes
            Axis limits.
            
-- do_entprof
    Use the entprof module.
    
        -- entprof_fixaxes
            Specify axis limits.
            
       -- entprof_axes
            Axis limits.
            
-- do_densanim
    Use the densanim module.
    
        -- densanim_direction
            Axis along which to do the projection. (string)
            
        -- densanim_plotwith
            Width of the projection plot in code units.
            
        -- densanim_fixlimits
            Put limits on the density projection colorbar.
            
        -- densanim_lowlim
            Lower limit on colorbar.
            
        -- densanim_highlim
            Higher limit on colorbar.
            
-- do_partslice
    Use the partsliceanim module.
    
        -- partslice_direction
            Axis along which to do the projection. (string)
            
        -- partslice_parttype
            Which type of particle? (H or He) (string)
            
        -- partslice_plotwith
            Width of the projection plot in code units.
            
        -- partslice_fixlimits
            Put limits on the projection plot colorbar.
            
        -- partslice_lowlim
            Lower limit on colorbar.
            
        -- partslice_highlim
            Higher limit on colorbar.
            
-- do_comparison
    Is this a comparison between multiple simulations?
    
        -- comparison_name
            Name for the comparison plots, which will go in their filename. (string)
            
        -- nplots
            Number of simulations to compare.
            
        -- nrows
            Number of rows in the comparison plots. Note that (nrows) x (ncolumns) cannot exceed nplots.
            
        -- ncolumns
            Number of columns in the comparison plots. Note that (nrows) x (ncolumns) cannot exceed nplots.
            
        -- readpath(1-8)
            Paths to the data of the different simulations. If readpath = 'skip', the space will be left blank. (string)
            
        -- title(1-8)
            Title of plots for each simulation. (string)
            
-- gamma
    Adiabatic index.
    
-- G
    Gravitational constant in cgs.
    
-- R
    Gas constant in code units.
    
-- Rsun
    Solar radius in cm.
    
-- Msun
    Solar mass in grams.
