"""
Helper Functions for Binocular Rivalry Test (BR_test.py)
Project headed by Liz Lawler
Collaborators:
    Jen Holmberg, UC Berkeley PhD Student - worked on Catch Trials
    Miranda Shen, UC Berkeley Undergraduate student - worked on countdown 
    functions and formatting saved data 
    Sean Noah, UC Berkeley postdoc
"""
from __future__ import absolute_import, division, print_function

from psychopy import core, visual, event, monitors, data, gui, sound
from psychopy.visual import filters 
from psychopy.hardware import keyboard
import numpy as np
import math

import os
from datetime import date

from builtins import range
from random import random

cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
demoDir = os.path.join(cwd, 'demo_images')
red_demoImg = os.path.join(demoDir, 'Red_45.png')
blue_demoImg = os.path.join(demoDir, 'Blue_45.png')
mixed_demoImg = os.path.join(demoDir, 'MixedPercept_circle.png')

def startCountdown(windowObject, countDuration, textSize, wrapWidthScale):
    ''' puts text on the screen and counts down before the first trial'''
    introTimer = core.CountdownTimer(countDuration) # create trial timer object
    
    while introTimer.getTime() > 0 :
        countDownTime = math.ceil(introTimer.getTime())
        displayText = visual.TextStim(windowObject, 
            text = u"Trial starting in \n" + str(countDownTime),
            color = "white",
            font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
        displayText.draw()
        windowObject.flip()
    
def breakCountdown(windowObject, countDuration, textSize, wrapWidthScale):
    ''' puts text on the screen and counts down for a required break'''
    breakTimer = core.CountdownTimer(countDuration) # create trial timer object
    
    while breakTimer.getTime() > 0 :
        countDownTime = math.ceil(breakTimer.getTime())
        displayText = visual.TextStim(windowObject, 
            text = u"Take a break for \n" + str(countDownTime),
            color = "white",
            font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
        displayText.draw()
        windowObject.flip()

def waitForKey(windowObject, keyboardObject, keyName):
    '''Waits for a specific key press '''
    keyPressed = 0
    
    if type(keyName) is not list:
        keyName = [keyName] 
        
    while not keyPressed:
        keyResp = keyboardObject.getKeys(waitRelease=True, clear=True) # get keypresses from the subject
                
        if len(keyResp) > 0 : # check to make sure we have key presses
            for key in keyResp:
                
                if key.name in keyName:
                    keyPressed = 1
                    break
                

def makeGratingStimuliForRivalry(windowObject, bottomOri, topOri, bottomColor, topColor, stimulusSize, stimulusPhase=0.0, stimulusCPD=6.0):
    '''Description'''
    colorDict = {
        "blue": 2,
        "green": 1,
        "red": 0
    }
    
    botColorIndex = 2#0 #9/17 trying force blue to be top color to remove red ghosting #colorDict[bottomColor]
    topColorIndex = 0#2 #colorDict[topColor]
    
    gh = 256
    gw = 256
    
    topStim = visual.GratingStim(win=windowObject, size=(stimulusSize, stimulusSize), ori=topOri, mask='raisedCos', opacity=0.35)
    
    baseGrating = filters.makeGrating(res=256)
    
    top_hsv_tex = np.ones((gh, gw, 3))
    top_hsv_tex = top_hsv_tex *-1
    
    top_hsv_tex[...,topColorIndex] = (baseGrating)/2.0
    
    topStim.tex = top_hsv_tex #psychopy.tools.colorspacetools.hsv2rgb(hsv_tex)
    topStim.sf=350.0/256

    botStim = visual.GratingStim(win=windowObject, size=(stimulusSize, stimulusSize), ori=bottomOri, mask='raisedCos', )
    
    baseGrating = filters.makeGrating(res=256)
    
    bot_hsv_tex = np.ones((gh, gw, 3))
    bot_hsv_tex = bot_hsv_tex *-1
    
    bot_hsv_tex[...,botColorIndex] = (baseGrating)/2.0
    
    botStim.tex = bot_hsv_tex #psychopy.tools.colorspacetools.hsv2rgb(hsv_tex)
    botStim.sf=350.0/256
    
    return topStim, botStim

def runRivalryTrials(trialHandlerObject, 
                    keyboardObject, 
                    windowObject,
                    topImageParams,
                    redKey, 
                    blueKey, 
                    mixedKey, 
                    rivalryLength,
                    wrongKeyNote, 
                    gratingSize,
                    expClockObj,
                    textSize,
                    wrapWidthScale):
    # display this trial's stimuli on the screen
    topOrientation = topImageParams['ori']
    topColor = topImageParams['color']
    botOrientation = topOrientation + 90
    if topColor == 'red':
        botColor = 'blue'
    elif topColor == 'blue':
        botColor = 'red'
    topStim, botStim = makeGratingStimuliForRivalry(windowObject, topOrientation,botOrientation, topColor, botColor, gratingSize)
     
    botStim.draw()
    topStim.draw()
    windowObject.flip()
    
    
    # initialize response arrays
    allResponses_RT = []
    allResponses_Dur = []
    allResponses_Names = []
    allResponses = []
    
    # reset keyboard clock
    keyboardObject.clock.reset()
    keyboardObject.clearEvents(eventType='Keyboard')
    
    rivalryTimer = core.CountdownTimer(rivalryLength) # create trial timer object
    rivalryBuffer = core.CountdownTimer(rivalryLength+2)
    
    #windowObject._getFrame().save('laptop_stim.png') - useful for saving images of stimuli 
    # start rivarly trial 
    trialStart = expClockObj.getTime()
    while rivalryBuffer.getTime() > 0: # countdown for the rivalry duration
        while rivalryTimer.getTime() > 0:
            keyResp = keyboardObject.getKeys(waitRelease=True, clear=True) # get keypresses from the subject
            
            if len(keyResp) > 0 : # check to make sure we have key presses
                for key in keyResp:
                    if key.name not in [redKey, blueKey, mixedKey]: # incorrect key pressed
                        # make error sound
                        wrongKeyNote.play()
            
                if 'q' in keyResp:
                    windowObject.close()
                    core.quit()
            
            # Compile multiple keyresponses as they come in
            allResponses_RT.extend([key.rt for key in keyResp])
            allResponses.extend(keyResp)
            allResponses_Dur.extend([key.duration for key in keyResp])
            allResponses_Names.extend([key.name for key in keyResp])
        
        # END rivalry timer 
        #if keyResp
        trialEnd = expClockObj.getTime()
        
        displayText = visual.TextStim(windowObject, 
            text = u"Release Key",
            color = "white",
            font = "Open Sans", height = textSize, pos=(0,0), alignText="center", wrapWidth = wrapWidthScale)
        displayText.draw()
        windowObject.flip()
        
        
        # out of rivalry While loop but in buffer
        keyResp = keyboardObject.getKeys(waitRelease=True, clear=True)
        if len(keyResp) > 0 :
            trialHandlerObject.addData('Flag', 'cut off by trial end')
            allResponses_RT.extend([key.rt for key in keyResp])
            allResponses.extend(keyResp)
            allResponses_Dur.extend([key.duration for key in keyResp])
            allResponses_Names.extend([key.name for key in keyResp])
    
    additionalKeySave = event.getKeys(timeStamped=True)

#    if rivalryTime.getTime() == 0.0 and key.duration is None:
        

    # save key responses to the trialHandler 
    trialHandlerObject.addData('keyDur', allResponses_Dur)
    trialHandlerObject.addData('keyRT', allResponses_RT)
    trialHandlerObject.addData('keyName', allResponses_Names)
    trialHandlerObject.addData('keys', allResponses)
    trialHandlerObject.addData('expTime-TrialStart', trialStart)
    trialHandlerObject.addData('expTime-TrialEnd', trialEnd)
    trialHandlerObject.addData('eventKeys', additionalKeySave)

def runGlassesDemo(keyboardObject, 
                    windowObject,
                    topImageParams,
                    redKey, 
                    blueKey, 
                    mixedKey, 
                    rivalryLength,
                    wrongKeyNote, 
                    gratingSize,
                    bottomTextPos,
                    textSize):
                        
    redText = visual.TextStim(windowObject, 
        text = "Red Key Down",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTextPos, alignText="center")
    blueText = visual.TextStim(windowObject, 
        text = "Blue Key Down",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTextPos, alignText="center")
    mixedText = visual.TextStim(windowObject, 
                    text = "Mixed Key Down",
                    color = "white",
                    font = "Open Sans", height = textSize, pos=bottomTextPos, alignText="center")
    emptyText = visual.TextStim(windowObject, 
        text = "",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTextPos, alignText="center")
                    
    # display this trial's stimuli on the screen
    topOrientation = topImageParams['ori']
    topColor = topImageParams['color']
    botOrientation = topOrientation + 90
    if topColor == 'red':
        botColor = 'blue'
    elif topColor == 'blue':
        botColor = 'red'
    topStim, botStim = makeGratingStimuliForRivalry(windowObject, topOrientation,botOrientation, topColor, botColor, gratingSize)
     
    botStim.draw()
    topStim.draw()
    windowObject.flip()
    
    rivalryTimer = core.CountdownTimer(rivalryLength) # create trial timer object
    
    # reset keyboard clock
    keyboardObject.clock.reset()
    keyboardObject.clearEvents(eventType='Keyboard')
    
    refresh = 0
    # start rivarly trial 
    while rivalryTimer.getTime() > 0: # countdown for the rivalry duration
        #keyResp = keyboardObject.getKeys(waitRelease=True, clear=True) # get keypresses from the subject
        
        keyStr = ''
        responseKeys = [redKey, blueKey, mixedKey, 'q']
        botStim.draw()
        topStim.draw()
        
        
        if refresh:
            keys = keyboardObject.getKeys(waitRelease=False, clear=True)
            refresh = 0
        else:     
            keys = keyboardObject.getKeys(waitRelease=False, clear=False)
        keyArray = [key.name for key in keys]
        
        if len(keyArray) > 0:
            keyStr = keys[-1].name

            if keys[-1].name == redKey:
                if keys[-1].duration is None:
                    redText.draw()
                else:
                    refresh = 1
                    emptyText.draw()

            
            if keys[-1].name == blueKey:
                if keys[-1].duration is None:
                    blueText.draw()
                else:
                    refresh = 1
                    emptyText.draw()
            
            if keys[-1].name == mixedKey:
                if keys[-1].duration is None:
                    mixedText.draw()
                else:
                    refresh = 1
                    emptyText.draw()
        windowObject.flip()


def runPracticeTest(redKey, mixedKey, blueKey, currentColor, practiceTime, windowObject, keyboardObj, textSize, bottomTexPos, imgScale):
    ## make demo stimuli
    if currentColor == 'red':
        demoImg = red_demoImg
        correctKey = redKey
    elif currentColor =='blue':
        demoImg = blue_demoImg
        correctKey = blueKey
    elif currentColor == 'mixed':
        demoImg = mixed_demoImg
        correctKey = mixedKey
    demoStim = visual.ImageStim(windowObject, image=demoImg, pos=(0,0))
    demoStim.size = demoStim.size * imgScale

    demoStim.draw()
    windowObject.flip()

    centerX = demoStim.size[0] / 2
    correctText = visual.TextStim(windowObject, 
        text = "Good!",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center")
    emptyText = visual.TextStim(windowObject, 
        text = "",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center")
    incorrectText = visual.TextStim(windowObject, 
                    text = "Incorrect Key!",
                    color = "white",
                    font = "Open Sans", height = textSize, pos=bottomTexPos, alignText="center")
    
    keyboardObj.clock.reset()
    keyboardObj.clearEvents()
    timer = core.CountdownTimer(practiceTime)
    refresh = 0

    while timer.getTime() > 0:
        keyStr = ''
        responseKeys = [redKey, blueKey, mixedKey, 'q']
        demoStim.draw()
        
        if refresh:
            keys = keyboardObj.getKeys(waitRelease=False, clear=True)
            refresh = 0
        else:     
            keys = keyboardObj.getKeys(waitRelease=False, clear=False)
        keyArray = [key.name for key in keys]
        
        if len(keyArray) > 0:
            keyStr = keys[-1].name

            if keys[-1].name == correctKey:
                if keys[-1].duration is None:
                    correctText.draw()
                else:
                    refresh = 1

            
            if keys[-1].name != correctKey:
                if keys[-1].duration is None:
                    incorrectText.draw()
                else:
                    refresh = 1
                    emptyText.draw()
        windowObject.flip()
    
