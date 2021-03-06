#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project headed by Liz Lawler
Collaborators:
    Jen Holmberg, UC Berkeley PhD Student - worked on Catch Trials
    Miranda Shen, UC Berkeley Undergraduate student - worked on countdown 
    functions and formatting saved data 
"""

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

import BR_functions_v2 as runRivalry



#### DEBUG MODE
debug_mode = 1


### Declare Variables & Parameters -------------
wrongKeyNote = sound.Sound('C', secs=0.1)
repeatCond = 1
gratingSize = 4.4 # this is in degrees visual angle based on monitor properties saved into MonitorCenter
spatialFrequency = 3
cyclesForStim = gratingSize * spatialFrequency
trialClock = core.Clock()
kb = keyboard.Keyboard()
demoTime = 5
rivalryLength = 5#100
breakTime = 3#0
textSize = 0.7 # height of the text to display during instructions

## Keys for stimulus
redKey = 'left' 
blueKey = 'right'
mixedKey = 'space'
nextKey = ['down', 'return']

## Images for demo
cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
demoDir = os.path.join(cwd, 'demo_images')
red_demoImg = os.path.join(demoDir, 'Red_45.png')
blue_demoImg = os.path.join(demoDir, 'Blue_45.png')
mixed_demoImg = os.path.join(demoDir, 'MixedPercept_circle.png')
red_blue_glassesImg = os.path.join(demoDir, 'red_blue_glasses_1.png')

## End variables & parameters


# create your list of stimuli
# NB as of version 1.62 you could simply import an excel spreadsheet with this
# using data.importConditions('someFile.xlsx')
stimList = []
trialCount = 0
for ori in [45, 135]:
    for color in ['red', 'blue']:
        #for redOpacity in [0.35, 0.45, 0.5, 0.55, 0.65]:
        for redOpacity in [0.5]:
            # append a python 'dictionary' to the list
            trialCount += 1
            stimList.append({'topColor': color, 'topOri': ori, 'redOpacity':redOpacity})
            


### Get Subject Variables
dinputDlg = gui.Dlg(title='Binocular Rivalry')
inputDlg = gui.Dlg(title='Binocular Rivalry')
inputDlg.addText('Subject Information')
inputDlg.addField('Subject Number:')
inputDlg.addField('Session Number:')
inputDlg.addField('Skip Demo? (0 - no, 1 - yes; for debug only)')
inputData = inputDlg.show()
subject = inputData[0]
session = inputData[1]
skipIntro = int(inputData[2])

    

# create a window to draw in
thisMonitor = monitors.Monitor('Lenovo_CarbonX1')
thisMonitor.setDistance(60)
# monitors.Monitor("testMonitor")
win = visual.Window(allowGUI=False, fullscr=True,screen=1, units='deg', size = [1920, 1080], monitor=thisMonitor) #fullscr=True, units="deg",
win.setMouseVisible(False) # suppress mouse cursor

## Display Parameters
shiftY=3
centerScreenX = win.size[0]
centerScreenY = win.size[1]
imgScale = 1.0
upperTexPos = (0.0, 6.5)
wrapWidthScale = 28
demoStimPos = (0.0, 0.0)
bottomTexPos = (0.0, -5.5)
bottomTexLongPos = (0.0, -5.0)


# organize trials with the trial handler
trials = data.TrialHandler(stimList, repeatCond, 
                           extraInfo={'participant': subject, 'session':session})
                           # *** Todo: make variable of experiment parameters to save to extraInfo 

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

# An ExperimentHandler isn't essential but helps with data saving
expName = 'BR_test'
expInfo = {u'Session': session, u'Participant': subject}

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=subjectDataFileNameWide)

thisExp.addLoop(trials)

if skipIntro == 0:
    ### INTRODUCTION & DEMO 
    messageIntro = visual.TextStim(win, 
        text = "Welcome to the Binocular Rivalry Test Demo! \n Hit any key to continue",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0.0, 0.0), alignText="center", wrapWidth = wrapWidthScale)
    
    messageIntro.draw()
    win.flip()
    event.waitKeys()
    
    ## INSTRUCTIONS
    # Keyboard Screen
    
    # Stimulus Screen 
    redDemoStim = visual.ImageStim(win, image=red_demoImg, pos=(-9,shiftY))# color='red')
    redDemoStim.size = redDemoStim.size * imgScale
    redDemoStim.draw()
    
    blueDemoStim = visual.ImageStim(win, image=blue_demoImg, pos=(0,shiftY))# color='red')
    blueDemoStim.size = blueDemoStim.size *imgScale
    blueDemoStim.draw()
    
    mixedDemoStim = visual.ImageStim(win, image=mixed_demoImg, pos=(9,shiftY))# color='red')
    mixedDemoStim.size = mixedDemoStim.size *imgScale
    mixedDemoStim.draw()
    
    bottomText = visual.TextStim(win, 
        text = "In the next experiment, you could either see a RED pattern, a BLUE pattern or a MIX between the two. \n When you see a specific pattern, you'll be asked to PRESS and HOLD each key for as long as you see that respective pattern \n Hit any key to continue",
        color = "white",
        font = "Open Sans", height = textSize, alignText='center', pos=bottomTexLongPos, wrapWidth = wrapWidthScale)
    bottomText.draw()
    win.flip()
    event.waitKeys()
    
    # Red Stimulus
    redDemoStim = visual.ImageStim(win, image=red_demoImg, pos=demoStimPos)# color='red')
    redDemoStim.size = redDemoStim.size * imgScale
    redDemoStim.draw()
    
    topText = visual.TextStim(win, 
        text = "When you see the RED pattern, press the left key on the keyboard. \n Hold LEFT key down as long as you see a RED pattern",
        color = "white",
        font = "Open Sans", height = textSize, pos=upperTexPos, alignText="center", wrapWidth = wrapWidthScale)
    bottomText = visual.TextStim(win, 
        text = "Press the left key on the keyboard now",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center", wrapWidth = wrapWidthScale)
    topText.draw()
    bottomText.draw()
    win.flip()
    event.waitKeys()
    
    runRivalry.waitForKey(win, kb, redKey)
    
    # Blue Stimulus
    blueDemoStim = visual.ImageStim(win, image=blue_demoImg, pos=demoStimPos)# color='red')
    blueDemoStim.size = blueDemoStim.size *imgScale
    blueDemoStim.draw()
    
    topText = visual.TextStim(win, 
        text = "When you see the BLUE pattern, press the right key on the keyboard. \n Hold RIGHT key down as long as you see a BLUE pattern",
        color = "white",
        font = "Open Sans", height = textSize, pos=upperTexPos, alignText="center", wrapWidth = wrapWidthScale)
    bottomText = visual.TextStim(win, 
        text = "Press the right key on the keyboard now",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center", wrapWidth = wrapWidthScale)
    topText.draw()
    bottomText.draw()
    win.flip()
    runRivalry.waitForKey(win, kb, blueKey)
    
    # Mixex Stimulus
    mixedDemoStim = visual.ImageStim(win, image=mixed_demoImg, pos=demoStimPos)# color='red')
    mixedDemoStim.size = mixedDemoStim.size *imgScale
    mixedDemoStim.draw()
    
    topText = visual.TextStim(win, 
        text = "When you see the a mixture between the two patterns, press the SPACE key on the keyboard. \n Hold SPACE down as long as you see a mixed pattern",
        color = "white",
        font = "Open Sans",  height = textSize, pos=upperTexPos, alignText="center", wrapWidth = wrapWidthScale)
    bottomText = visual.TextStim(win, 
        text = "Press the SPACE key on the keyboard now",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center", wrapWidth = wrapWidthScale)
    topText.draw()
    bottomText.draw()
    win.flip()
    runRivalry.waitForKey(win, kb, mixedKey)
    
    # Practice Intro
    waitText = visual.TextStim(win, 
        text = u"You'll start by practicing on a couple of examples \n Press ENTER or \u2193 to start",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
    waitText.draw()
    win.flip()
    runRivalry.waitForKey(win, kb, nextKey)
    win.flip()
    core.wait(1.0)
    
    # Red Demo
    runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'red', demoTime, win, kb, textSize, bottomTexPos, imgScale)
    
    # Pause Screen
    waitText = visual.TextStim(win, 
        text = u"Next, you'll practice pressing RIGHT for BLUE \n Press ENTER or \u2193 to start",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0,0), wrapWidth = wrapWidthScale, alignText="center")
    waitText.draw()
    win.flip()
    runRivalry.waitForKey(win, kb, nextKey)
    win.flip()
    core.wait(1.0)
    
    # Blue Demo
    runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'blue', demoTime, win, kb, textSize, bottomTexPos, imgScale)
    
    # Pause Screen
    waitText = visual.TextStim(win, 
        text = u"Next, you'll practice pressing SPACE for MIXED \n Press ENTER or \u2193 to start",
        color = "white",
        font = "Open Sans", height = textSize, wrapWidth = wrapWidthScale, pos=(0,0), alignText="center")
    waitText.draw()
    win.flip()
    runRivalry.waitForKey(win, kb, nextKey)
    win.flip()
    core.wait(1.0)
    
    # Mixed Demo 
    runRivalry.runPracticeTest(redKey, mixedKey, blueKey, 'mixed', demoTime, win, kb, textSize, bottomTexPos, imgScale)
    
    # Practice with the glasses:
    
    # put on glasses now 
    #glassesStim = visual.ImageStim(win, image=red_blue_glassesImg, pos=(-10,shiftY))# color='red')
    #glassesStim.draw()
    glassesText = visual.TextStim(win, 
        text = u"Please put on your Red/Blue glasses now. \n\n You'll practice once more with the glasses on \n Press ENTER or \u2193 to start",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
    glassesText.draw()
    
    win.flip()
    runRivalry.waitForKey(win, kb, nextKey)
    win.flip()
    core.wait(1.0)
    
    # Demo params 
    glassesDemoLength = 10
    demoParams = {}
    demoParams['color'] = 'red'
    demoParams['ori'] = 45
    runRivalry.runGlassesDemo(kb, win, demoParams, redKey, blueKey, mixedKey, glassesDemoLength,wrongKeyNote, gratingSize, bottomTexPos, textSize)
    win.flip()
    
# Ask subjects if ready
waitText = visual.TextStim(win, 
    text = u"The practice has ended! When you feel ready, press ENTER or \u2193 to start",
    color = "white",
    font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
waitText.draw()
win.flip()
runRivalry.waitForKey(win, kb, nextKey)
win.flip()
core.wait(1.0)

runRivalry.startCountdown(win, 5, textSize, wrapWidthScale)


### TRial Handler Test
# run the experiment
nDone = 0


kb.clearEvents()
expClock = core.MonotonicClock()
count = 0
numTrials = trialCount

for thisTrial in trials:  # handler can act like a for loop
    count += 1
    topColor = thisTrial['topColor']
    topOrientation = thisTrial['topOri']
    
    topParams = {}
    topParams['color'] = topColor
    topParams['ori'] = topOrientation 
    topParams['redOpacity'] = thisTrial['redOpacity']
    
    
    runRivalry.runRivalryTrials(trials, kb, win, topParams, redKey, blueKey, 
        mixedKey, rivalryLength, wrongKeyNote, gratingSize, expClock, textSize,
        wrapWidthScale)
    thisExp.nextEntry() # advance the experiment handler 
    
    #runRivalryTesting.runRivalryTrials_usingPsychopyGratingStim(trials, kb, win, topParams, redKey, blueKey, mixedKey, rivalryLength, wrongKeyNote, gratingSize, expClock)

    # clear out the keyboard
    kb.clearEvents()
    kb.clock.reset()
    
    if count < numTrials:
        # 30 second break
        runRivalry.breakCountdown(win, breakTime, textSize, wrapWidthScale)
        
        # intertrial text 
        waitText = visual.TextStim(win, 
        text = u"Break End. \n Hit ENTER or \u2193 to continue.",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0,0), alignText="center")
        waitText.draw()
        win.flip()
        runRivalry.waitForKey(win, kb, nextKey)
        
    elif count == numTrials: # end the session
        waitText = visual.TextStim(win, 
        text = u"Experiment End!. \n Hit ENTER or \u2193 to close.",
        color = "white",
        font = "Open Sans", height = textSize, pos=(0,0), alignText="center")
        waitText.draw()
        win.flip()
        runRivalry.waitForKey(win, kb, nextKey)
    




win.close()
core.quit()

# The contents of this file are in the public domain.
