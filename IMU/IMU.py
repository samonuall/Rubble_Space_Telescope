#welcomesajiv
import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy
import math
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)   

while True:
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer

'''
the master master code needs to call functions from the IMU fuile: we determined 3 functions
1) run a test code to make sure the IMU is working
2) boot up the IMu and begin reporting readings
3) return what orbit the satteltile is on (orbit number 1, etc.)
'''
yaw = 0
orbitCount = 0
telemString = ""
def boot():
    
def orbitType():
    if(orbitCount == 1 or orbtiCount == 4 or completedOrbits == 7):
        return "Image"
    else:
        return "Tranfer"  
        
def overImage():
    if((yaw in range(350,360)) or (yaw in range (0,10)) or (yaw in range (110,130)) or (yaw in range (230,250)):
        return True
    else:
      overImage()

def endOrbit():
    orbitCount++
    telemString += orbitCount
    return telemString
