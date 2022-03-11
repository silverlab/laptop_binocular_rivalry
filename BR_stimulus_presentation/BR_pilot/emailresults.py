import BR_functions_v3 as runRivalry
import os
from os import listdir
import sys
import glob
from datetime import date


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

fileName =  find_csv_filenames("Data")[0][:-4]
print(fileName)
runRivalry.sendoutputemail(fileName)


from pathlib import Path
Path("Data/" + fileName + ".csv").rename("Data/Sent/" + fileName + ".csv")