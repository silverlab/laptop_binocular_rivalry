# Overview: laptop_binocular_rivalry
This project aims to run simple experiments measuring individual's binocular rivalry dynamics on a laptop. Setting up binocular rivalry (BR) experiments on a laptop allows flexibility with working with subjects outside of a lab. This can be beneficial for sensistive populations, or for frequent repeat measurements that participants can take at home. 

This project was headed by Elizabeth (Liz) Lawler in collaboration with Jen Holmberg, UC Berkeley Graduate Student, and Miranda Shen, UC Berkeley Undergraduate. 


#### Example of a simple set-up:
![laptop-BR-image](https://user-images.githubusercontent.com/19734455/151236501-85c210e1-6686-4acd-9ac1-28ee36aa0a40.png)

All a researcher needs to run, flexible BR experiments is a laptop compatibale with PsychoPy and Red/Blue anaglyph glasses. 

![laptop_schamatic_cropped](https://user-images.githubusercontent.com/19734455/151236776-fffa9a68-02d4-4135-bf68-28483e762e31.png)

Cartoon schematic of the design. When viewing the BR stimuli through Red/Blue anaglyph glasses, one eye will see the blue orientation grating while the other eye sees the red orietnation grating. 


## Contents:
This repository contains three main folder:
  - BR_stimulus_presentation: this folder contains neccessary files to run the experiment. The script to run the experiment is BR_test.py. You can use a .sh file wrapper to run the script from a desktop icon with Binocular_Rivalry_Experiment.sh
  - Analysis_Scripts: this folder contains functions to look at subject responses collected during the BR test (subject data is saved as a .csv). 
  - [ARCHIVED] oculus_rivalry: this is an archived folder that will no longer be supported. This folder has some starter code to display binocular rivalry stimulus in a Oculus Rift. It contains 1) an experimental script (in MATLAB), 2) the start of an analysis script (jupyter notebook), and 3) an example data file.
