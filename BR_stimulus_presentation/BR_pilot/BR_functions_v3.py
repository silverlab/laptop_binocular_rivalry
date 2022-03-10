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

import base64
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)



cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
demoDir = os.path.join(cwd, 'demo_images')
right_demoImg = os.path.join(demoDir, 'RightRed_45.png')
left_demoImg = os.path.join(demoDir, 'LeftBlue_45.png')
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

def makeGratingStimuliForCatchTrial(windowObject, bottomOri, topOri, bottomColor, topColor, stimulusSize, stimulusPhase=0.0, stimulusCPD=6.0):
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
    
    topStim = visual.GratingStim(win=windowObject, size=(stimulusSize, stimulusSize), ori=topOri, mask='raisedCos', )
    
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
                    rightKey, 
                    leftKey, 
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
    topStim, botStim = makeGratingStimuliForRivalry(windowObject, topOrientation, botOrientation, topColor, botColor, gratingSize)
     
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
                    if key.name not in [rightKey, leftKey, mixedKey]: # incorrect key pressed
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

    # If more than [X fraction] of key presses are not left, right, or mixed key, flag for trial redo.
    Xfraction = 2/3
    if ((allResponses_Names.count(rightKey) + allResponses_Names.count(leftKey) + allResponses_Names.count(mixedKey))/len(allResponses_Names)) < Xfraction :
        trialHandlerObject.addData('ButtonCheck', 1)
    else: 
        trialHandlerObject.addData('ButtonCheck', 0)

def runRivalryCatchTrials(trialHandlerObject, 
                    keyboardObject, 
                    windowObject,
                    topImageParams,
                    rightKey, 
                    leftKey, 
                    mixedKey, 
                    CatchTrial_Length,
                    wrongKeyNote, 
                    gratingSize,
                    expClockObj,
                    textSize,
                    wrapWidthScale):
    # display this trial's stimuli on the screen
    topOrientation = topImageParams['ori']
    topColor = topImageParams['color']
    if topOrientation == 45:
        botOrientation = 135
    elif topOrientation == 135:
        botOrientation = 45
    if topColor == 'red':
        botColor = 'blue'
    elif topColor == 'blue':
        botColor = 'red'
    topStim, botStim = makeGratingStimuliForCatchTrial(windowObject, topOrientation, botOrientation, topColor, botColor, gratingSize)
    
    coinflip = np.random.randint(0, 2)
    if coinflip == 0:
        botStim.draw()
        if botOrientation == 45:
            correct_Key = leftKey
        elif botOrientation == 135:
            correct_Key = rightKey
    elif coinflip == 1:
        topStim.draw()
        if topOrientation == 45:
            correct_Key = leftKey
        elif topOrientation == 135:
            correct_Key = rightKey
    windowObject.flip()
    
    
    # initialize response arrays
    allResponses_RT = []
    allResponses_Dur = []
    allResponses_Names = []
    allResponses = []
    
    # reset keyboard clock
    keyboardObject.clock.reset()
    keyboardObject.clearEvents(eventType='Keyboard')
    
    rivalryTimer = core.CountdownTimer(CatchTrial_Length) # create trial timer object
    rivalryBuffer = core.CountdownTimer(CatchTrial_Length+2)
    
    #windowObject._getFrame().save('laptop_stim.png') - useful for saving images of stimuli 
    # start rivarly trial 
    trialStart = expClockObj.getTime()
    while rivalryBuffer.getTime() > 0: # countdown for the rivalry duration
        while rivalryTimer.getTime() > 0:
            keyResp = keyboardObject.getKeys(waitRelease=True, clear=True) # get keypresses from the subject
            
            if len(keyResp) > 0 : # check to make sure we have key presses
                for key in keyResp:
                    if key.name not in [rightKey, leftKey, mixedKey]: # incorrect key pressed
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
            trialHandlerObject.addData('CatchTrial_Flag', 'cut off by trial end')
            allResponses_RT.extend([key.rt for key in keyResp])
            allResponses.extend(keyResp)
            allResponses_Dur.extend([key.duration for key in keyResp])
            allResponses_Names.extend([key.name for key in keyResp])
    
    additionalKeySave = event.getKeys(timeStamped=True)

#    if rivalryTime.getTime() == 0.0 and key.duration is None:
        

    # save key responses to the trialHandler 
    trialHandlerObject.addData('CatchTrial_keyDur', allResponses_Dur)
    trialHandlerObject.addData('CatchTrial_keyRT', allResponses_RT)
    trialHandlerObject.addData('CatchTrial_keyName', allResponses_Names)
    trialHandlerObject.addData('CatchTrial_keys', allResponses)
    trialHandlerObject.addData('CatchTrial_expTime-TrialStart', trialStart)
    trialHandlerObject.addData('CatchTrial_expTime-TrialEnd', trialEnd)
    trialHandlerObject.addData('CatchTrial_eventKeys', additionalKeySave)

    # If more than [X fraction] of key presses are not the correct key, flag for trial redo.
    Xfraction = 1/2
    if ((allResponses_Names.count(correct_Key))/len(allResponses_Names)) < Xfraction :
        trialHandlerObject.addData('CatchTrial_ButtonCheck', 1)
        return 1
    else: 
        trialHandlerObject.addData('CatchTrial_ButtonCheck', 0)
        return 0

def runGlassesDemo(keyboardObject, 
                    windowObject,
                    topImageParams,
                    rightKey, 
                    leftKey, 
                    mixedKey, 
                    rivalryLength,
                    wrongKeyNote, 
                    gratingSize,
                    bottomTextPos,
                    textSize):
                        
    rightText = visual.TextStim(windowObject, 
        text = "Right Key Down",
        color = "white",
        font = "Open Sans", height = textSize, pos=bottomTextPos, alignText="center")
    leftText = visual.TextStim(windowObject, 
        text = "Left Key Down",
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
        responseKeys = [rightKey, leftKey, mixedKey, 'q']
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

            if keys[-1].name == rightKey:
                if keys[-1].duration is None:
                    rightText.draw()
                else:
                    refresh = 1
                    emptyText.draw()

            
            if keys[-1].name == leftKey:
                if keys[-1].duration is None:
                    leftText.draw()
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


def runPracticeTest(rightKey, mixedKey, leftKey, currentOri, practiceTime, windowObject, keyboardObj, textSize, bottomTexPos, imgScale):
    ## make demo stimuli
    if currentOri == 'right':
        demoImg = right_demoImg
        correctKey = rightKey
    elif currentOri =='left':
        demoImg = left_demoImg
        correctKey = leftKey
    elif currentOri == 'mixed':
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
        responseKeys = [rightKey, leftKey, mixedKey, 'q']
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

def sendoutputemail(filename)
    message = Mail(
        from_email='berkeleypsychedelic@gmail.com',
        to_emails='berkeleypsychedelic@gmail.com',
        subject='Sendgrid test',
        html_content='test message')

    with open(filename, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(filename),
        FileType('application/csv'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
