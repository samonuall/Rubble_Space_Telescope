#welcomesajiv
import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy as np
import math
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)

#all variables
yaw = 0
imgcounter = 0
time = 0
orbitCount = 1
telemString = ""

while True:
    accelX, accelY, accelZ = sensor.accelerometer
    magX, magY, magZ = sensor.magnetometer

    roll = np.arctan2((accelY),(((accelX)**2 + (accelZ)**2)**0.5))
    pitch = np.arctan2((accelX),(((accelY)**2 + (accelZ)**2)**0.5))

    mag_x = (magX * np.cos(pitch)) + (magY * np.sin(roll)*np.sin(pitch)) + (magZ*np.cos(roll)*np.sin(pitch))
    mag_y = (magY*np.cos(roll)) - (magZ*np.sin(roll))
    #Original Yaw Eq: yaw = (180/np.pi)*np.arctan2(-mag_y, mag_x)
    yaw = (180/np.pi)*np.arctan2(-mag_y, mag_x)
    #Fixing
    yaw = (yaw + 360) % 360
    pitch = (((180/np.pi) * pitch) + 360) % 360
    roll = (((180/np.pi) * roll) + 360) % 360

    #yaw to 0-360
    if yaw > 360:
        yaw -= 360
    #set orbit end
    if(imgcounter >= 3):
        endOrbit()
        imgcounter = 0
'''
the master master code needs to call functions from the IMU fuile: we determined 3 functions
1) run a test code to make sure the IMU is working
2) boot up the IMu and begin reporting readings
3) return what orbit the satteltile is on (orbit number 1, etc.)
'''

def starttest():
    return yaw
def orbitType():
    if(orbitCount == 1 or orbtiCount == 4 or completedOrbits == 7):
        return "Image"
    else:
        return "Tranfer"

def overImage():
    if((yaw in range(350,360)) or (yaw in range (0,10)) or (yaw in range (110,130)) or (yaw in range (230,250))):
        imgcounter += 1
        telemString += " Image taken at " + time
        return True
    else:
      overImage()

def endOrbit():
    orbitCount += 1
    telemString += " Starting orbit " + orbitCount
    return telemString

def starttime():
    while True:
        time.sleep(0.1)
        time += 0.1
