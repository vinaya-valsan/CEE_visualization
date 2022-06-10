import numpy as np
from scipy.interpolate import interp1d

def readProfiles() :
    profilePath  = '~/code/CEE_visualization/'

    radPath      = profilePath + 'outfileRad'
    #radPathMesa  = profilePath + 'outfileRadMesa'
    densPath     = profilePath + 'outfileDens'
    #densPathMesa = profilePath + 'outfileDensMesa'
    presPath     = profilePath + 'outfilePres'
    #presPathMesa = profilePath + 'outfilePresMesa'
    tempPath     = profilePath + 'outfileTemp'
    #tempPathMesa = profilePath + 'outfileTempMesa'

    rad      = np.loadtxt(radPath)
    #radMesa  = np.loadtxt(radPathMesa)
    dens     = np.loadtxt(densPath)
    #densMesa = np.loadtxt(densPathMesa)
    pres     = np.loadtxt(presPath)
    #presMesa = np.loadtxt(presPathMesa)
    temp     = np.loadtxt(tempPath)
    #tempMesa = np.loadtxt(tempPathMesa)

    interpDens = interp1d(rad,dens,kind='linear')
    #interpDensMesa = interp1d(radMesa,densMesa,kind='linear')
    interpPres = interp1d(rad,pres,kind='linear')
    #interpPresMesa = interp1d(radMesa,presMesa,kind='linear')
    interpTemp = interp1d(rad,temp,kind='linear')
    #interpTempMesa = interp1d(radMesa,tempMesa,kind='linear')

    return interpDens, interpPres, interpTemp
    
