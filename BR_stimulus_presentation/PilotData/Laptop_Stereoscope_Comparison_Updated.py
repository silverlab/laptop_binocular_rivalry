#!/usr/bin/env python
# coding: utf-8

# In[105]:


# Modules 
import collections
import numpy as np
import seaborn as sbn
import matplotlib
import matplotlib.style
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import os
import pandas as pd
import math
import seaborn as sns

import scipy.io
import scipy.stats

import ast

from IPython.display import HTML, display
matplotlib.rcParams.update({'font.size':19})
# matplotlib.style.use('bmh')


# In[106]:


cwd = os.getcwd()

print(cwd)


# In[107]:


ls


# Testing on my own trials.

# In[108]:


fileName = 'TestFile.csv'

laptopDf = pd.read_csv(fileName)


# In[109]:


laptopDf


# In[110]:


type(laptopDf['keyRT'][0])


# In[111]:


laptopDf.columns


# In[112]:


laptopDf = laptopDf.drop('.thisRepN', 1).drop('.thisTrialN',1).drop('.thisN',1).drop('.thisIndex',1).drop('keys',1).drop('Flag',1)
laptopDf


# In[113]:


for i, row in laptopDf.iterrows():
    print(i ,'\n', row)


# In[114]:


laptopDf


# In[115]:


laptopDf["keyDur"]


# In[116]:


laptopDf.shape[0]


# In[117]:


# for i in np.arange(laptopDf.shape[0]):
    # x = laptopDf['keyRT'][i]
    # x = ast.literal_eval(x)
    # laptopDf.at[i,'keyRT'] = x


# In[118]:


np.arange(laptopDf.shape[1])


# In[119]:


np.arange(laptopDf.shape[0])


# In[120]:


# trying another function to convert strings to lists

def string_conv(df, col):
    for i in np.arange(df.shape[0]):
        x = df[col][i]
        x = ast.literal_eval(x)
        df.at[i,col] = x


# In[121]:


string_conv(laptopDf, 'keyRT')


# In[122]:


laptopDf['keyRT'][0]


# In[123]:


string_conv(laptopDf, 'keyDur')


# In[124]:


string_conv(laptopDf, 'keyName')


# In[125]:


redDurations = []
blueDurations = []
mixedDurations = []

leftDurations = [] # 135
rightDurations = [] # 45


# In[126]:


laptopDf['keyName'][0]


# In[127]:


for i, row in laptopDf.iterrows():
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])


# In[128]:


blueDurations


# In[129]:


redDurations


# In[130]:


mixedDurations


# In[131]:


fig, ax = plt.subplots()
num_bins = 30
# the histogram of the data
n, bins, patches = ax.hist(blueDurations, num_bins, color='red', alpha=0.5, range=(0.001, 5))
n, bins, patches = ax.hist(redDurations, num_bins, color='blue', alpha=0.5, range=(0.001, 5))

ax.set_ylabel('frequency')
ax.set_xlabel('Rivalry duration (s)')


# In[132]:


for i, row in laptopDf.iterrows():
    responseLen = len(row['keyDur'])
    
responseLen


# In[133]:


for i, row in laptopDf.iterrows():
    responseLen = len(row['keyDur'])
    print(row['keyDur'])
    print(responseLen)


# In[134]:


for i, row in laptopDf.iterrows():
    redDurations = []
    blueDurations = []
    mixedDurations = []
    leftDurations = [] # 135
    rightDurations = [] # 45
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])
        
    fig, ax = plt.subplots()
    num_bins = 30
    # the histogram of the data
    n, bins, patches = ax.hist(blueDurations, num_bins, color='red', alpha=0.5, range=(0.001, 5))
    n, bins, patches = ax.hist(redDurations, num_bins, color='blue', alpha=0.5, range=(0.001, 5))

    ax.set_ylabel('frequency')
    ax.set_xlabel('Rivalry duration (s)')


# In[135]:


for i, row in laptopDf.iterrows():
    redDurations = []
    blueDurations = []
    mixedDurations = []
    leftDurations = [] # 135
    rightDurations = [] # 45
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])
            
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    if len(blueDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean, redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = 0
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(redDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = 0
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = 0
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    else:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()


# In[136]:


for i, row in laptopDf.iterrows():
    redDurations = []
    blueDurations = []
    mixedDurations = []
    leftDurations = [] # 135
    rightDurations = [] # 45
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])
            
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    if len(blueDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(redDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = 0
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = 0
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(blueDurations) == 0 & len(redDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = 0
        mixedDurationsSum = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = sum(redDurations) / len(redDurations)
        mixedDurationsSum = 0
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations) / len(blueDurations)
        redDurationsSum = 0
        mixedDurationsSum = 0
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    else:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()


# In[137]:


fileName1 = 's01_session99_2021-11-02_BRdata_U.csv'

laptopDf1 = pd.read_csv(fileName1)


# In[138]:


laptopDf1


# In[139]:


string_conv(laptopDf1, 'keyRT')


# In[140]:


string_conv(laptopDf1, 'keyDur')


# In[141]:


string_conv(laptopDf1, 'keyName')


# In[142]:


laptopDf['keyName'][0]


# In[143]:


redDurations1 = []
blueDurations1 = []
mixedDurations1 = []

leftDurations1 = [] # 135
rightDurations1 = [] # 45


# In[144]:


for i, row in laptopDf1.iterrows():
    redDurations1 = []
    blueDurations1 = []
    mixedDurations1 = []
    leftDurations1 = [] # 135
    rightDurations1 = [] # 45
    responseLen1 = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen1):
        if row['keyName'][j] == 'right': # blue
            blueDurations1.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations1.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations1.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations1.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations1.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations1.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations1.append(row['keyDur'][j])
        
    fig, ax = plt.subplots()
    num_bins = 30
    # the histogram of the data
    n, bins, patches = ax.hist(blueDurations1, num_bins, color='red', alpha=0.5, range=(0.001, 5))
    n, bins, patches = ax.hist(redDurations1, num_bins, color='blue', alpha=0.5, range=(0.001, 5))

    ax.set_ylabel('frequency')
    ax.set_xlabel('Rivalry duration (s)')


# In[145]:


# barplot of means

fig1 = plt.figure()
ax = fig1.add_axes([0,0,1,1])
titles1 = ['blue mean', 'red mean', 'mixed mean']
blueDurationsMean1 = sum(blueDurations1) / len(blueDurations1)
redDurationsMean1 = sum(redDurations1) / len(redDurations1)
mixedDurationsMean1 = sum(mixedDurations1) / len(mixedDurations1)
means1 = [blueDurationsMean1,redDurationsMean1,mixedDurationsMean1]
ax.bar(titles1,means1)
plt.show()


# In[146]:


for i, row in laptopDf1.iterrows():
    redDurations = []
    blueDurations = []
    mixedDurations = []
    leftDurations = [] # 135
    rightDurations = [] # 45
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])
            
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    if len(blueDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean, redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = 0
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(redDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = 0
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = 0
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = 0
        mixedDurationsMean = 0
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()
    else:
        titles = ['blue mean', 'red mean', 'mixed mean']
        blueDurationsMean = sum(blueDurations) / len(blueDurations)
        redDurationsMean = sum(redDurations) / len(redDurations)
        mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
        ax.bar(titles,means)
        plt.show()


# In[147]:


# barplot of sums

fig1 = plt.figure()
ax = fig1.add_axes([0,0,1,1])
titles1 = ['blue sum', 'red sum', 'mixed sum']
blueDurationsSum1 = sum(blueDurations1)
redDurationsSum1 = sum(redDurations1)
mixedDurationsSum1 = sum(mixedDurations1)
sums1 = [blueDurationsSum1,redDurationsSum1,mixedDurationsSum1]
ax.bar(titles1,sums1)
plt.show()


# In[148]:


for i, row in laptopDf1.iterrows():
    redDurations = []
    blueDurations = []
    mixedDurations = []
    leftDurations = [] # 135
    rightDurations = [] # 45
    responseLen = len(row['keyDur'])
    
    blueIs45 = 0
    
    if row['topColor'] == 'blue':
        if row['topOri'] == 45:
            blueIs45 = 1
        else:
            blueIs45 = 0
    else:
        if row['topOri'] == 45: # red is 45
            blueIs45 = 0
        else:
            blueIs45 = 1
    
    for j in range(responseLen):
        if row['keyName'][j] == 'right': # blue
            blueDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 
                rightDurations.append(row['keyDur'][j])
            else: # blue is not 45
                leftDurations.append(row['keyDur'][j])
            
        elif row['keyName'][j] == 'left': # red
            redDurations.append(row['keyDur'][j])
            
            if blueIs45: # if true blue is 45 and red is 135 (left)
                leftDurations.append(row['keyDur'][j])
            else: # blue is not 45
                rightDurations.append(row['keyDur'][j])
        elif row['keyName'][j] == 'space': # mixed
            mixedDurations.append(row['keyDur'][j])
            
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    if len(blueDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(redDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = 0
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = 0
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()
    elif len(blueDurations) == 0 & len(redDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = 0
        mixedDurationsSum = sum(mixedDurations) / len(mixedDurations)
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    elif len(blueDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = 0
        redDurationsSum = sum(redDurations) / len(redDurations)
        mixedDurationsSum = 0
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    elif len(redDurations) == 0 & len(mixedDurations) == 0:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations) / len(blueDurations)
        redDurationsSum = 0
        mixedDurationsSum = 0
        means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,means)
        plt.show()
    else:
        titles = ['blue sum', 'red sum', 'mixed sum']
        blueDurationsSum = sum(blueDurations)
        redDurationsSum = sum(redDurations)
        mixedDurationsSum = sum(mixedDurations)
        sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
        ax.bar(titles,sums)
        plt.show()


# Everything below is not applicable; it was testing different function methods.

# In[149]:


# splitRT = laptopDf['keyRT'][0].split(',')
# splitRT


# In[150]:


# testing on keyRT

# firstItem = 0
# lastItem = len(splitRT)-1
# keyRT_corrected = []
# count = 0 
# for strI in splitRT:
    # if count == firstItem:
        # thisStr = strI[1:]
        # thisStr = float(thisStr)
    # elif count == lastItem:
        # thisStr = strI[:-1]
    # else:
        # thisStr = float(strI)
        
    # thisStr = float(thisStr)
    # keyRT_corrected.append(thisStr)
    # count += 1
    
# keyRT_corrected


# In[151]:


# laptopDf.shape[0]


# In[152]:


# creating the function

# def string_conv(df, col):
    # for i in np.arange(df.shape[0]):
        # splitRT = df[col][i].split(',')
        # firstItem = 0
        # lastItem = len(splitRT)-1
        # keyRT_corrected = []
        # count = 0 
        # for strI in splitRT:
            # if count == firstItem:
                # thisStr = strI[1:]
                # thisStr = float(thisStr)
            # elif count == lastItem:
                # thisStr = strI[:-1]
            # else:
                # thisStr = float(strI)
        
            # thisStr = float(thisStr)
            # keyRT_corrected.append(thisStr)
            # count += 1
            # df.at[i, col] = thisStr


# In[153]:


# string_conv(laptopDf, 'keyDur')
# laptopDf


# In[154]:


# thisStrCopy = [1,2,3,4]
# laptopDf.at[0, 'keyDur'] = thisStrCopy
# laptopDf


# In[155]:


# laptopDf = string_conv(laptopDf, "keyRT")


# In[156]:


# laptopDf


# In[108]:


# keyRT_corrected


# In[109]:


# len(laptopDf['keyName'][0])


# In[110]:


# laptopDf['keyName'][0]

