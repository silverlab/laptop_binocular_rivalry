from psychopy import monitors, visual, event
from psychopy.visual import GratingStim, filters, ImageStim

import numpy as np
def makeGratingStimuliForRivalry(bottomOri, topOri, bottomColor, topColor, stimulusSize, stimulusPhase=0.0, stimulusCPD=8.0):
    '''Description'''
    colorDict = {
        "blue": 2,
        "green": 1,
        "red": 0
    }
    
    botColorIndex = colorDict[bottomColor]
    topColorIndex = colorDict[topColor]
    
    # initialize a generic array of the size we want - we'll set the color soon
    baseGrat = np.zeros((stimulusSize, stimulusSize, 3), 'f')
    baseGrat[:,:,0]=-1.0
    baseGrat[:,:,1]=-1.0
    baseGrat[:,:,2]=-1.0
    
    # determine features of the top and bottom grating respectively
    topGrating = filters.makeGrating(ori=topOri, phase=stimulusPhase, 
        gratType='sin', res=stimulusSize, cycles=stimulusCPD)
    bottomGrating = filters.makeGrating(ori=bottomOri, phase=stimulusPhase, 
        gratType='sin', res=stimulusSize, cycles=stimulusCPD)
    
    # set each grating to the specific color channel we want it 
    bottomImage = baseGrat
    bottomImage[:,:,botColorIndex] = bottomGrating
    
    topImage = baseGrat
    topImage[:,:,topColorIndex] = topGrating
    
    
    return bottomImage, topImage
        
win = visual.Window(allowGUI=False, fullscr=True, units='deg', monitor=monitors.Monitor("testMonitor")) #fullscr=True, units="deg",

myTex = np.array([
    [1,0],
    [0,-1]
    ])
    
myTex = np.random.random((8,8,4))
myMask = np.array([
    [1,0,-1,0],
    [0,-1,0,1],
    [-1,0,1,0],
    [0,1,0,-1]
    ])

grating_res = 256
grating = filters.makeGrating(ori=45.0, phase=0.0, gratType='sin', res=256, cycles=8.0)

blue_grating=np.ones((grating_res, grating_res, 3))* -1.0
blue_grating[...,1] = grating

blueGrat = np.zeros((grating_res, grating_res, 3), 'f')
blueGrat[:,:,0]=-1.0
blueGrat[:,:,1]=-1.0 
blueGrat[:,:,2]=grating

#grating2 = filters.makeGrating(ori=(45.0+90.0), phase=0.0, gratType ='sin', res=grating_res, cycles=8.0)
#redGrat = np.zeros((grating_res, grating_res, 3), 'f')
#redGrat[:,:,0]=grating2
#redGrat[:,:,1]=-1.0
#redGrat[:,:,2]=-1.0

# Need to make own circle mask

# need to expand on circle mask to make "faux" mixed percept
gratingSize=10
    
myStimG = ImageStim(win, mask="circle", image=blueGrat, size=(gratingSize, gratingSize), opacity=1.0)# color='red')
myStimG.draw()

topImage, bottomImage = makeGratingStimuliForRivalry(135,45, "red", "blue", 256*2)

topStim = ImageStim(win, mask="circle", image=topImage, size=(gratingSize, gratingSize), opacity=0.5)# color='red')
topStim.draw()
win.flip()

event.waitKeys()
win.close()

