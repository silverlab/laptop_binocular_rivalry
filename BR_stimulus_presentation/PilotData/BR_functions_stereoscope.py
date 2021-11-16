"""
Helper Functions for Binocular Rivalry Test (BR_test.py)
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

cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
demoDir = os.path.join(cwd, 'demo_images')
red_demoImg = os.path.join(demoDir, 'Red_45.png')
blue_demoImg = os.path.join(demoDir, 'Blue_45.png')
mixed_demoImg = os.path.join(demoDir, 'MixedPercept_circle.png')

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
    bottomImage = baseGrat.copy()
    bottomImage[:,:,botColorIndex] = bottomGrating
    
    topImage = baseGrat.copy()
    topImage[:,:,topColorIndex] = topGrating
    
    
    return topImage, bottomImage
    
def presentAlignmentStimuliForStereoscope(keyboardOjbect, windowObject, gratingSize, leftEyePos, rightEyePos):
    '''make stimuli to alignstereoscope'''
    
    circleRadius = (gratingSize/2) + 0.6
    circleDiameter = circleRadius/2
    leftEyePos = (-gratingSize*2, 0)
    rightEyePos = (gratingSize*2, 0)
    
    leftEyeAnnulus = visual.Circle(windowObject, radius=(gratingSize/2)+0.6, units='deg', lineWidth=20.0, fillColor=None, lineColor='black', pos=(-leftEyePos[0],0), edges=64)
    rightEyeAnnulus = visual.Circle(windowObject, radius=(gratingSize/2)+0.6, units='deg', lineWidth=20.0, fillColor=None, lineColor='black', pos=(rightEyePos[0],0), edges=64)
    
    
    leftEyeCrossH = visual.Line(win=windowObject, units='deg', start=(leftEyePos[0]-0.5,0), end=(leftEyePos[0]+0.5, 0), lineWidth = 5, lineColor='black', fillColor=None)
    leftEyeCrossV = visual.Line(win=windowObject, units='deg', start=(leftEyePos[0], leftEyePos[1]-0.5), end=(leftEyePos[0], leftEyePos[1]+0.5), lineWidth = 5, lineColor='black', fillColor=None)
    rightEyeCrossH = visual.Line(win=windowObject, units='deg', start=(rightEyePos[0]-0.5, 0), end=(rightEyePos[0]+0.5, 0), lineWidth = 5, lineColor='black', fillColor=None)
    rightEyeCrossV = visual.Line(win=windowObject, units='deg', start=(rightEyePos[0], rightEyePos[1]-0.5), end=(rightEyePos[0], rightEyePos[1]+0.5), lineWidth = 5, lineColor='black', fillColor=None)

    
    leftEyeHorizontal = visual.Line(win=windowObject, units='deg', start=(leftEyePos[0]-circleRadius, 0), end=(leftEyePos[0]+circleRadius, 0), lineWidth = 5, lineColor='white')
    rightEyeVertical = visual.Line(win=windowObject, units='deg', start=(rightEyePos[0], rightEyePos[1]-circleRadius), end=(rightEyePos[0], rightEyePos[1]+circleRadius), lineWidth = 5, lineColor='white')
    
    
    leftEyeHorizontal.draw()
    rightEyeVertical.draw()
    
    leftEyeCrossH.draw()
    leftEyeCrossV.draw()
    rightEyeCrossH.draw()
    rightEyeCrossV.draw()
    
    leftEyeAnnulus.draw()
    rightEyeAnnulus.draw()
    
    windowObject.flip()
    event.waitKeys()

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
                    expClockObj):
    # display this trial's stimuli on the screen
    topOrientation = topImageParams['ori']
    topColor = topImageParams['color']
    botOrientation = topOrientation + 90
    if topColor == 'red':
        botColor = 'blue'
    elif topColor == 'blue':
        botColor = 'red'
    topImage, bottomImage = makeGratingStimuliForRivalry(topOrientation,botOrientation, topColor, botColor, 256*2)
    
    circleStimL = visual.Circle(windowObject, radius=(gratingSize/2)+0.6, units='deg', lineWidth=20.0, fillColor=None, lineColor='black', pos=(-gratingSize*3,0), edges=64)
    circleStimR = visual.Circle(windowObject, radius=(gratingSize/2)+0.6, units='deg', lineWidth=20.0, fillColor=None, lineColor='black', pos=(gratingSize*3,0), edges=64)
    
    bottomStim = visual.ImageStim(windowObject, mask='raisedCos', image=bottomImage, size=(gratingSize, gratingSize), opacity=1.0, pos=(-gratingSize*2,0))
    # previously mask='circle'
    bottomStim.draw()
    topStim = visual.ImageStim(windowObject, mask='raisedCos', image=topImage, size=(gratingSize, gratingSize), opacity=0.5, pos=(gratingSize*2,0))
    topStim.draw()
    
    circleStimL.draw()
    circleStimR.draw()
    
    windowObject.flip()
    
    rivalryTimer = core.CountdownTimer(rivalryLength) # create trial timer object
    rivalryBuffer = core.CountdownTimer(rivalryLength+1)
    
    # initialize response arrays
    allResponses_RT = []
    allResponses_Dur = []
    allResponses_Names = []
    allResponses = []
    
    # reset keyboard clock
    keyboardObject.clock.reset()
    keyboardObject.clearEvents(eventType='Keyboard')
    
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
            
        #if keyResp
        trialEnd = expClockObj.getTime()
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
                    gratingSize):
                        
    redText = visual.TextStim(windowObject, 
        text = "Red Key Down",
        color = "white",
        font = "Open Sans", height = 0.9, pos=(0,-10), alignText="center")
    blueText = visual.TextStim(windowObject, 
        text = "Blue Key Down",
        color = "white",
        font = "Open Sans", height = 0.9, pos=(0,-10), alignText="center")
    mixedText = visual.TextStim(windowObject, 
                    text = "Mixed Key Down",
                    color = "white",
                    font = "Open Sans", height = 0.9, pos=(0,-10), alignText="center")
    emptyText = visual.TextStim(windowObject, 
        text = "",
        color = "white",
        font = "Open Sans", height = 0.9, pos=(0,-8), alignText="center")
                    
    # display this trial's stimuli on the screen
    topOrientation = topImageParams['ori']
    topColor = topImageParams['color']
    botOrientation = topOrientation + 90
    if topColor == 'red':
        botColor = 'blue'
    elif topColor == 'blue':
        botColor = 'red'
    topImage, bottomImage = makeGratingStimuliForRivalry(topOrientation,botOrientation, topColor, botColor, 256*2)
     
    bottomStim = visual.ImageStim(windowObject, mask="raisedCos", image=bottomImage, size=(gratingSize, gratingSize), opacity=1.0, maskParams={'fringeWidth':0.5}, pos=(-5, 0))
    bottomStim.draw()
    topStim = visual.ImageStim(windowObject, mask="raisedCos", image=topImage, size=(gratingSize, gratingSize), opacity=0.5, maskParams={'fringeWidth':0.5}, pos=(500,0))
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
        topStim.draw()
        bottomStim.draw()
        
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


def runPracticeTest(redKey, mixedKey, blueKey, currentColor, practiceTime, windowObject, keyboardObj):
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

    demoStim.draw()
    windowObject.flip()

    centerX = demoStim.size[0] / 2
    correctText = visual.TextStim(windowObject, 
        text = "Good!",
        color = "white",
        font = "Open Sans", height = 0.9, pos=(0,-8), alignText="center")
    emptyText = visual.TextStim(windowObject, 
        text = "",
        color = "white",
        font = "Open Sans", height = 0.9, pos=(0,-8), alignText="center")
    incorrectText = visual.TextStim(windowObject, 
                    text = "Incorrect Key!",
                    color = "white",
                    font = "Open Sans", height = 0.9, pos=(0,-8), alignText="center")
    
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
    

