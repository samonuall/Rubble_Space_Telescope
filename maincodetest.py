import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy as np
import math
from imu import *

print(imuBoot())
#print(cameraboot())
#print(btBoot())

while True:
    time.sleep(2)
    print(getyaw())

