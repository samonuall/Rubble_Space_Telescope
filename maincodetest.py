import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy as np
import math
import imu
from imu import *

print(imuBoot())
#print(cameraboot())
#print(btBoot())

hasStarted = False
while hasStarted == False:
    if(overImage()):
        print('True')

