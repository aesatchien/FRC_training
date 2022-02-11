# FRC_training
Notebooks and how-tos for python and robotpy
Everything is meant to be run in Jupyter (links below for installing) with the robotpy libraries installed.  **HOWEVER**, since git is jupyter-aware, you can just browse the notebooks in the directories here for quick checks.

### Contents
* notebooks - Jupyter notebooks 
  * python_tutorials
    * python_intro_basics.ipynb - a super-quick intro to python using Jupyter (requires Jupyter)
    * advanced_concepts.ipynb  - so far: lambdas, args, kwargs
  * cad - several tools for generating cam for machining
    * bearing_shift.ipynb - tell it the XY center of the bearing you want and it writes a file for the benchmill
    * center_drill20.ipynb - give it a list of points and it will center drill them on shapeoko or spot/peck on benchmill  
  * homeworks
    * hints on assignments (currently has hints on autonomous movement commands)
  * controls
    * PID controllers, odometry
  * robot_code
    *  binding_commands - hints on how to get commands linked to robot actions
    *  robot_examples - more hints on commands V1 and V2 frameworks for the robot/subsystem/command approach to programming an FRC bot    
* data_files - TBD

Clone the git and install on your own machine:
Use "git clone https://github.com/aesatchien/FRC_training.git" from the git bash (or any git aware) shell to download.  If you don't have git and you just want to look at the code, you can download the repository from the links on the right as a zip file.

### Additional resources  
Instructions for setting up a computer with python/Jupyter/robotpy are here:
https://docs.google.com/presentation/d/1I9zLBFxzQQfoCT_rQM1h9BL_zonfC3Td5V-v-lqOAmo/edit?usp=sharing
More details, including git:
https://docs.google.com/document/d/1oS4aMhn9Rf_kpubbQ_JGEtOcRR36LoU-QbJQERZtyIU/edit?usp=sharing

Instructions for running the robot simulations are here:
https://docs.google.com/presentation/d/1HtnmHYvBDK8ZrVXY4N0AWA45qNpQRWV0QOrDxS_dWGc/edit?usp=sharing


  
  
