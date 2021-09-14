# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:55:48 2021

@author: elawl
"""

from __future__ import absolute_import, division, print_function
from distutils.core import setup
import py2exe


from psychopy import core, visual, event, monitors, data
import pandas as pd
import os

from builtins import range
from random import random

setup(console=['gabor_FS_test2.py'])