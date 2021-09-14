#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from psychopy import core, visual, event, monitors, data, gui, sound
from psychopy.visual import filters 
from psychopy.hardware import keyboard
import numpy as np

import os
from datetime import date

from builtins import range
from random import random
from scipy import ndimage

import BR_functions as runRivalry


#### DEBUG MODE
debug_mode = 1



### Declare Functions
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
    

## End Functions

### Declare Variables & Parameters -------------
wrongKeyNote = sound.Sound('C', secs=0.1)
repeatCond = 1
gratingSize = 15
trialClock = core.Clock()
kb = keyboard.Keyboard()
demoTime = 5
rivalryLength = 5

## Keys for stimulus
redKey = 'left' # *** MOVE TO TOP!
blueKey = 'right'
mixedKey = 'space'

## Images for demo
cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
demoDir = os.path.join(cwd, 'demo_images')
red_demoImg = os.path.join(demoDir, 'Red_45.png')
blue_demoImg = os.path.join(demoDir, 'Blue_45.png')
mixed_demoImg = os.path.join(demoDir, 'MixedPercept_circle.png')
red_blue_glassesImg = os.path.join(demoDir, 'red_blue_glasses_1.png')
#keyboardDemo = 


## End variables & parameters



# create your list of stimuli
# NB as of version 1.62 you could simply import an excel spreadsheet with this
# using data.importConditions('someFile.xlsx')
stimList = []
for ori in [45, 135]:
    for color in ['red', 'blue']:
        # append a python 'dictionary' to the list
        stimList.append({'topColor': color, 'topOri': ori})
        


### Get Subject Variables
dinputDlg = gui.Dlg(title='Binocular Rivalry')
inputDlg = gui.Dlg(title='Binocular Rivalry')
inputDlg.addText('Subject Information')
inputDlg.addField('Subject Number:')
inputDlg.addField('Session Number:')
inputData = inputDlg.show()
subject = inputData[0]
session = inputData[1]

    

# create a window to draw in
win = visual.Window(allowGUI=False, fullscr=True, units='deg', monitor=monitors.Monitor("testMonitor")) #fullscr=True, units="deg",
win.setMouseVisible(False) # suppress mouse cursor

# organize trials with the trial handler
trials = data.TrialHandler(stimList, repeatCond,
                           extraInfo={'participant': subject, 'session':session})
                           # *** Todo: make variable of experiment parameters to save to extraInfo 



### INTRODUCTION & DEMO 
messageIntro = visual.TextStim(win, 
    text = "Welcome to the Binocular Rivalry Test Demo! \n Hit any key to continue",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, 0.0), alignText="center", wrapWidth = 45)


messageIntro.draw()
win.flip()
event.waitKeys()

### INSTRUCTIONS
## Keyboard Screen

## Stimulus Screen 
shiftY=3
centerScreenX = win.size[0]
centerScreenY = win.size[1]

redDemoStim = visual.ImageStim(win, image=red_demoImg, pos=(-15,shiftY))# color='red')
#redDemoStim.size = redDemoStim.size * 0.8
redDemoStim.draw()

blueDemoStim = visual.ImageStim(win, image=blue_demoImg, pos=(0,shiftY))# color='red')
#blueDemoStim.size = blueDemoStim.size *0.8
blueDemoStim.draw()

mixedDemoStim = visual.ImageStim(win, image=mixed_demoImg, pos=(15,shiftY))# color='red')
#mixedDemoStim.size = mixedDemoStim.size *0.8
mixedDemoStim.draw()

bottomText = visual.TextStim(win, 
    text = "In the next experiment, you could either see a RED pattern, a BLUE pattern or a MIX between the two. \n When you see a specific pattern, you'll be asked to PRESS and HOLD each key for as long as you see that respective pattern \n Hit any key to continue",
    color = "white",
    font = "Open Sans", height = 0.9, alignText='center', pos=(0.0, -5.0), wrapWidth = 45)
bottomText.draw()
win.flip()
event.waitKeys()

## Red Stimulus
redDemoStim = visual.ImageStim(win, image=red_demoImg, pos=(0,shiftY))# color='red')

redDemoStim.draw()
#visual.TextStim(win, 
#    text = "In the next experiment, you could either see a RED pattern, a BLUE pattern or a MIX between the two. \n When you see a specific pattern, you'll be asked to Press and Hold each key for as long as you see that respective pattern",
#    color = "white",
#    font = "Open Sans", height = 0.9, alignText='center', pos=(0.0, -5.0), wrapWidth = 45)
topText = visual.TextStim(win, 
    text = "When you see the RED pattern, press the left key on the keyboard. \n Hold LEFT key down as long as you see a RED pattern",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, 13.0), alignText="center", wrapWidth = 45)
bottomText = visual.TextStim(win, 
    text = "Press the left key on the keyboard now",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, -5.0), alignText="center", wrapWidth = 45)
topText.draw()
bottomText.draw()
win.flip()
event.waitKeys()

## Blue Stimulus
blueDemoStim = visual.ImageStim(win, image=blue_demoImg, pos=(0,shiftY))# color='red')

blueDemoStim.draw()
topText = visual.TextStim(win, 
    text = "When you see the BLUE pattern, press the right key on the keyboard. \n Hold RIGHT key down as long as you see a BLUE pattern",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, 13.0), alignText="center", wrapWidth = 45)
bottomText = visual.TextStim(win, 
    text = "Press the right key on the keyboard now",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, -5.0), alignText="center", wrapWidth = 45)
topText.draw()
bottomText.draw()
win.flip()
event.waitKeys()

## Mixex Stimulus
mixedDemoStim = visual.ImageStim(win, image=mixed_demoImg, pos=(0,shiftY))# color='red')

mixedDemoStim.draw()
topText = visual.TextStim(win, 
    text = "When you see the a mixture between the two patterns, press the SPACE key on the keyboard. \n Hold SPACE down as long as you see a mixed pattern",
    color = "white",
    font = "Open Sans",  height = 0.9, pos=(0.0, 13.0), alignText="center", wrapWidth = 45)
bottomText = visual.TextStim(win, 
    text = "Press the SPACE key on the keyboard now",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0.0, -5.0), alignText="center", wrapWidth = 45)
topText.draw()
bottomText.draw()
win.flip()
event.waitKeys()

## Practice Intro
waitText = visual.TextStim(win, 
    text = "You'll start by practicing on a couple of examples \n Press SPACE to start",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0,0), alignText="center", wrapWidth = 45)
waitText.draw()
win.flip()
event.waitKeys()
win.flip()
core.wait(1.0)

## Red Demo
runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'red', demoTime, win, kb)

## Pause Screen
waitText = visual.TextStim(win, 
    text = "Next, you'll practice pressing RIGHT for BLUE \n Press SPACE to start",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0,0), wrapWidth = 45, alignText="center")
waitText.draw()
win.flip()
event.waitKeys()
win.flip()
core.wait(1.0)

## Blue Demo
runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'blue', demoTime, win, kb)

## Pause Screen
waitText = visual.TextStim(win, 
    text = "Next, you'll practice pressing SPACE for MIXED \n Press SPACE to start",
    color = "white",
    font = "Open Sans", height = 0.9, wrapWidth = 45, pos=(0,0), alignText="center")
waitText.draw()
win.flip()
event.waitKeys()
win.flip()
core.wait(1.0)

## Mixed Demo 
runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'mixed', demoTime, win, kb)

## Practice with the glasses:

## put on glasses now 
glassesStim = visual.ImageStim(win, image=red_blue_glassesImg, pos=(-10,shiftY))# color='red')
#glassesStim.draw()
glassesText = visual.TextStim(win, 
    text = "Please put on your Red/Blue glasses now. You'll practice once more with the glasses on",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0,0), alignText="center", wrapWidth = 45)
glassesText.draw()

win.flip()
event.waitKeys()
win.flip()
core.wait(1.0)

# Demo params 
glassesDemoLength = 10
demoParams = {}
demoParams['color'] = 'red'
demoParams['ori'] = 45
runRivalry.runGlassesDemo(kb, win, demoParams, redKey, blueKey, mixedKey, glassesDemoLength,wrongKeyNote, gratingSize)
win.flip()

## Ask subjects if ready
waitText = visual.TextStim(win, 
    text = "The practice has ended! When you feel ready, press any key to start",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0,0), alignText="center", wrapWidth = 45)
waitText.draw()
win.flip()
event.waitKeys()
win.flip()
core.wait(1.0)


### TRial Handler Test
# run the experiment
nDone = 0


kb.clearEvents()
expClock = core.MonotonicClock()

for thisTrial in trials:  # handler can act like a for loop
    topColor = thisTrial['topColor']
    topOrientation = thisTrial['topOri']
    
    topParams = {}
    topParams['color'] = topColor
    topParams['ori'] = topOrientation 
    
    runRivalry.runRivalryTrials(trials, kb, win, topParams, redKey, blueKey, mixedKey, rivalryLength, wrongKeyNote, gratingSize, expClock)
    
    # clear out the keyboard
    kb.clearEvents()
    kb.clock.reset()
    
    # intertrial text 
    waitText = visual.TextStim(win, 
    text = "End Trial. Hit Space to continue.",
    color = "white",
    font = "Open Sans", height = 0.9, pos=(0,0), alignText="center")
    waitText.draw()
    win.flip()
    event.waitKeys()


# Save a copy of the whole TrialHandler object, which can be reloaded later to
# re-create the experiment.
fileName =  "s{}_session{}_BRdata".format(subject, session)# subject Number, session date
subjectDataFileName = os.path.join(dataDir, fileName)
trials.saveAsPickle(subjectDataFileName)


# Wide format is useful for analysis with R or SPSS.
todaysDate = date.today()
fileName =  "s{}_session{}_{}_BRdata.csv".format(subject, session, todaysDate)# subject Number, session date
subjectDataFileNameWide = os.path.join(dataDir, fileName)
df = trials.saveAsWideText(subjectDataFileNameWide, delim=",")


win.close()
core.quit()

# The contents of this file are in the public domain.
