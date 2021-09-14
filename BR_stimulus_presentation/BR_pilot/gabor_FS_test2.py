#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import psychtoolbox as ptb
from psychopy import core, visual, event, monitors, data, gui, sound
from psychopy.hardware import keyboard


import os
from datetime import date

from builtins import range
from random import random

wrongKeyNote = sound.Sound('C', secs=0.1)

# create your list of stimuli
# NB as of version 1.62 you could simply import an excel spreadsheet with this
# using data.importConditions('someFile.xlsx')
stimList = []
for ori in [45]:
    for sf in [0.5, 1.0, 2.0]:
        # append a python 'dictionary' to the list
        stimList.append({'sf': sf, 'ori': ori})

### Get Subject Variables
inputDlg = gui.Dlg(title='Binocular Rivalry')
inputDlg.addText('Subject Information')
inputDlg.addField('Subject Number:')
inputDlg.addField('Session Number:')
inputData = inputDlg.show()
print(inputData)



# organize them with the trial handler
trials = data.TrialHandler(stimList, 2,
                           extraInfo={'participant': inputData[0], 'session':inputData[1]})




# create a window to draw in
win = visual.Window(allowGUI=False, fullscr=True, units='deg', monitor=monitors.Monitor("testMonitor")) #fullscr=True, units="deg",

# INITIALISE SOME STIMULI
#gabor = visual.GratingStim(win, tex="sin", mask="gauss", texRes=256, 
#           size=[10.0, 10.0], sf=[0.5, 0], ori = 0, name='gabor1', color=(1.0, 0, 0))
#gabor.autoDraw = True
message = visual.TextStim(win, pos=(0.0, -0.9), text='Hit Q to quit')
trialClock = core.Clock()
kb = keyboard.Keyboard()

### TRial Handler Test
# run the experiment
nDone = 0

for thisTrial in trials:  # handler can act like a for loop
    trialSF = thisTrial['sf']
    trialOrientation = thisTrial['ori']
    gaborB = visual.GratingStim(win, tex="sin", mask="gauss", texRes=256, 
           size=[10.0, 10.0], sf=[trialSF, trialSF], ori = trialOrientation, name='gaborBlue', color=[-1,1,-1], colorSpace='rgb', contrast=1.0)
    gaborB.phase += 0.01
    gaborB.draw()
    
    gaborR = visual.GratingStim(win, tex="sin", mask="gauss", texRes=256, 
           size=[10.0, 10.0], sf=[trialSF, trialSF], ori = trialOrientation+90, name='gaborRed', color=[1,-1,-1], colorSpace='rgb', contrast=1.0)
    gaborR.phase += 0.01
    gaborR.draw()
    win.flip()
    # run key data
    waitForKeys = True
    kb.clock.reset()
    while waitForKeys:
        responseKeys = ['right', 'left', 'quit']
        keys = kb.getKeys( waitRelease=True)
        if 'q' in keys:
            win.close()
            core.quit()
            break
        for key in keys:
            if key in responseKeys:
                thisReactionTime = key.rt
                thisChoice = key.name
                print(key.name, key.rt, key.duration, key.tDown)
                waitForKeys = False
                break
            else:
                # beep for incorrect key
                wrongKeyNote.play()
                print('beep!')
    
    trials.data.add('RT', thisReactionTime)  # add the data to our set
    trials.data.add('choice', thisChoice)
    nDone += 1  # just for a quick reference



# Save a copy of the whole TrialHandler object, which can be reloaded later to
# re-create the experiment.
cwd = os.getcwd()
dataDir = os.path.join(cwd, 'Data')
fileName =  "s{}_session{}_BRdata".format(inputData[0], inputData[0])# subject Number, session date
subjectDataFileName = os.path.join(dataDir, fileName)
trials.saveAsPickle(subjectDataFileName)


# Wide format is useful for analysis with R or SPSS.
todaysDate = date.today()
fileName =  "s{}_session{}_{}_BRdata.csv".format(inputData[0], inputData[0], todaysDate)# subject Number, session date
subjectDataFileNameWide = os.path.join(dataDir, fileName)
df = trials.saveAsWideText(subjectDataFileNameWide, delim=",")


win.close()
core.quit()



# The contents of this file are in the public domain.
