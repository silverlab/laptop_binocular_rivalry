# Analysis Functions for displaying responses during Binocular Rivalry 
# Written by Miranda Shen, 2021

#!/usr/bin/env python
# coding: utf-8



""" Importing modules. """

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





def columnSelector(my_df):
    """ Takes in dataframe and outputs dataframe with columns 'topColor','topOri','keyDur','keyRT','keyName'. """
    my_df = my_df[['topColor','topOri','keyDur','keyRT','keyName']]




def string_conv(df, col):
    """ Takes in dataframe and column name and solves issue where the list was in a string. """
    for i in np.arange(df.shape[0]):
        x = df[col][i]
        x = ast.literal_eval(x)
        df.at[i,col] = x



def histogram_maker(my_df):
    """ Takes in dataframe and makes histogram of duration for red, blue, and mixed perceptions. """
    histogram_list = []
    for i, row in my_df.iterrows():
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
        n, bins, patches = ax.hist(blueDurations1, num_bins, color='blue', alpha=0.5, range=(0.001, 5))
        n, bins, patches = ax.hist(redDurations1, num_bins, color='red', alpha=0.5, range=(0.001, 5))

        ax.set_ylabel('frequency')
        ax.set_xlabel('Rivalry duration (s)')
        histogram_list.append(plt.gcf())
        
    return histogram_list


def barplot_mean_maker(my_df):
    """ Takes in dataframe and makes barplot of means of duration for blue, red, and mixed perceptions. """
    means_list = []
    for i, row in my_df.iterrows():
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
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean, redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        elif len(redDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = 0
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        elif len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        elif len(blueDurations) == 0 & len(redDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = 0
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        elif len(blueDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        elif len(redDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = 0
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
        else:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            plt.show()
            means_list.append(fig)
    return means_list




def barplot_sum_maker(my_df):
    """ Takes in dataframe and makes barplot of sums of duration for blue, red, and mixed perceptions. """
    sums_list = []
    for i, row in my_df.iterrows():
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
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = 0
            redDurationsSum = sum(redDurations)
            mixedDurationsSum = sum(mixedDurations)
            sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,sums,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        elif len(redDurations) == 0:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = sum(blueDurations)
            redDurationsSum = 0
            mixedDurationsSum = sum(mixedDurations)
            sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,sums,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        elif len(mixedDurations) == 0:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = sum(blueDurations)
            redDurationsSum = sum(redDurations)
            mixedDurationsSum = 0
            sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,sums,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        elif len(blueDurations) == 0 & len(redDurations) == 0:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = 0
            redDurationsSum = 0
            mixedDurationsSum = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        elif len(blueDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = 0
            redDurationsSum = sum(redDurations) / len(redDurations)
            mixedDurationsSum = 0
            means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        elif len(redDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = sum(blueDurations) / len(blueDurations)
            redDurationsSum = 0
            mixedDurationsSum = 0
            means = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
        else:
            titles = ['blue percept sum', 'red percept sum', 'mixed percept sum']
            x_pos = np.arange(len(titles))
            blueDurationsSum = sum(blueDurations)
            redDurationsSum = sum(redDurations)
            mixedDurationsSum = sum(mixedDurations)
            sums = [blueDurationsSum,redDurationsSum,mixedDurationsSum]
            ax.bar(titles,sums,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('total durations (s)')
            plt.show()
            sums_list.append(fig)
    return sums_list




def barplot_mean_maker(my_df):
    """ Takes in dataframe and makes barplot of means of duration for blue, red, and mixed perceptions. """
    means_list = []
    for i, row in my_df.iterrows():
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
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean, redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        elif len(redDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = 0
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        elif len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        elif len(blueDurations) == 0 & len(redDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = 0
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        elif len(blueDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = 0
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        elif len(redDurations) == 0 & len(mixedDurations) == 0:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = 0
            mixedDurationsMean = 0
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
        else:
            titles = ['blue percept mean', 'red percept mean', 'mixed percept mean']
            x_pos = np.arange(len(titles))
            blueDurationsMean = sum(blueDurations) / len(blueDurations)
            redDurationsMean = sum(redDurations) / len(redDurations)
            mixedDurationsMean = sum(mixedDurations) / len(mixedDurations)
            means = [blueDurationsMean,redDurationsMean,mixedDurationsMean]
            ax.bar(titles,means,color=['blue','red','purple'])
            plt.xticks(x_pos, titles, rotation=90)
            plt.ylabel('mean durations (s)')
            means_list.append(fig)
    return means_list



def repeated_percepts(df):
    """ Takes in dataframe and counts how many times left, right, and space bars are pressed after each other for 
    all trials. Returns a list of three numbers representing [left,right,space] presses."""
    counts_list = []
    left_count = 0
    right_count = 0
    space_count = 0
    count = 0

    while count < len(df['keyName']):
        for k in np.arange(1,len(df['keyName'][count])):
            if df['keyName'][count][k] == df['keyName'][count][k-1] == "left":
                left_count += 1
            if df['keyName'][count][k] == df['keyName'][count][k-1] == "right":
                right_count += 1
            if df['keyName'][count][k] == df['keyName'][count][k-1] == "mixed":
                space_count += 1
        count += 1

    counts_list.append(left_count) 
    counts_list.append(right_count) 
    counts_list.append(space_count) 

    print(counts_list)




def repeated_percepts_mixed(df):
    """ Takes in dataframe and counts how many times left and right keys are pressed before and after the space bar for 
    all trials. Returns a list of two numbers representing [left,right] presses."""


    # patterns to look for

    patternLeft = ['left', 'space', 'left']
    patternRight = ['right', 'space', 'right']
    counts_list = []
    left_count = 0
    right_count = 0
    space_count = 0

    for i, row in df.iterrows():
        thisTrial = row['keyName'] # might not be neccessary to make into a list
        for j in range(len(thisTrial)):
            if j < len(thisTrial)-2:
                chunkOfThree = [thisTrial[j], thisTrial[j+1], thisTrial[j+2]]
                # check to see if chunk is a pattern we're looking for
                if chunkOfThree == patternLeft:
                    # subject pressed 'right', 'space', 'right
                    left_count += 1
                    # add one to a count, or save the index to a list to veferify pattern and to use to  count later
                elif chunkOfThree == patternRight: 
                    # subject pressed 'left', 'space', 'left'
                    right_count += 1
                    # add to a count or save indext to a list to count later

    return [left_count,right_count]





