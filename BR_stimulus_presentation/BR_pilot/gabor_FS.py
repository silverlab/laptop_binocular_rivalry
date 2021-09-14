#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from psychopy import core, visual, event, monitors, data
import pandas as pd
import os

from builtins import range
from random import random

# create your list of stimuli
# NB as of version 1.62 you could simply import an excel spreadsheet with this
# using data.importConditions('someFile.xlsx')
stimList = []
for ori in range(90, 180, 30):
    for sf in [0.5, 1.0, 2.0]:
        # append a python 'dictionary' to the list
        stimList.append({'sf': sf, 'ori': ori})

# organize them with the trial handler
trials = data.TrialHandler(stimList, 10,
                           extraInfo={'participant': "Nobody", 'session':'001'})




# create a window to draw in
win = visual.Window(allowGUI=False, fullscr=True, units='deg', monitor=monitors.Monitor("testMonitor")) #fullscr=True, units="deg",

# INITIALISE SOME STIMULI
gabor = visual.GratingStim(win, tex="sin", mask="gauss", texRes=256, 
           size=[10.0, 10.0], sf=[0.5, 0], ori = 0, name='gabor1', color=(1.0, 0, 0))
gabor.autoDraw = True
message = visual.TextStim(win, pos=(0.0, -0.9), text='Hit Q to quit')
trialClock = core.Clock()

### TRial Handler Test
# run the experiment
nDone = 0
for thisTrial in trials:  # handler can act like a for loop
    # simulate some data
    thisReactionTime = random() + float(thisTrial['sf']) / 2.0
    thisChoice = round(random())
    trials.data.add('RT', thisReactionTime)  # add the data to our set
    trials.data.add('choice', thisChoice)
    nDone += 1  # just for a quick reference

    msg = 'trial %i had position %s in the list (sf=%.1f)'
    print(msg % (nDone, trials.thisIndex, thisTrial['sf']))

# After the experiment, print a new line
print('\n')

# Write summary data to screen
trials.printAsText(stimOut=['sf', 'ori'],
                   dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# Write summary data to a text file ...
trials.saveAsText(fileName='testData',
                  stimOut=['sf', 'ori'],
                  dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# ... or an xlsx file (which supports sheets)
trials.saveAsExcel(fileName='testData',
                   sheetName='rawData',
                   stimOut=['sf', 'ori'],
                   dataOut=['RT_mean', 'RT_std', 'choice_raw'])

# Save a copy of the whole TrialHandler object, which can be reloaded later to
# re-create the experiment.
trials.saveAsPickle(fileName='testData')

# Wide format is useful for analysis with R or SPSS.
df = trials.saveAsWideText('testDataWide.txt')







# repeat drawing for each frame
while trialClock.getTime() < 20: 
    gabor.phase += 0.01
    message.draw()
    # handle key presses each frame
    if event.getKeys(keyList=['escape', 'q']):
        win.close()
        core.quit()

    win.flip()

#data = [['red', 1], ['blue', 0]]
#df_data = pd.DataFrame(data, columns=['color', 'duration'])

#rint(data)
#print(df_data)

cwd = os.getcwd()
#dataSavePath = os.path.join(cwd, 'Data', 'PLEASESAVE.csv')
#df_data.to_csv(dataSavePath, index=False)

dataSavePath2 = os.path.join(cwd, 'Data', 'PLEASESAVE2.txt')
file = open(dataSavePath2, 'w')
file.write('data???')
file.close()



win.close()
core.quit()



# The contents of this file are in the public domain.
