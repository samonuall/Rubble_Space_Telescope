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

#all variables
yaw = 0
prevyaw = 0
imgcount = 0
timecount = 0
orbitCount = 1
telemString = ""
#ADD YOUR VALUES BELOW HERE
Sajiv_north = 330
Sam_north = 340
Hasan_north = 0
Kat_north = -353

def imuBoot():
    global telemString
    return 'ADCS is go for launch /n' ;
def getyaw():
    global Sajiv_north
    global Sam_north
    global Hasan_north
    global Kat_north
    global prevyaw
    global yaw
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    
    pitch = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    pitch_corrected = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    """if accel_x >= 0 and accel_z >= 0 : 
        pass
    elif accel_z <= 0 and accel_x >= 0 :
        pitch_corrected = 180 - pitch
    elif accel_z <= 0 and accel_x < 0 :
        pitch_corrected = 180 - pitch
    elif accel_z >= 0 and accel_x <= 0 :
        pitch_corrected = pitch + 360"""

     
    roll = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    roll_corrected = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    '''
    if accel_z >= 0 and accel_y < 0:
        pass
    if accel_z <= 0 and accel_y < 0:
        roll_corrected = 180 - roll
    if accel_z <= 0 and accel_y > 0:
        roll_corrected = 180 - roll
    if accel_z > 0 and accel_y >= 0:
        roll_corrected = roll + 360
    '''
    roll_rad = roll*numpy.pi/180
    pitch_rad = pitch*numpy.pi/180
    
    mag_x_comp1 = mag_x*math.cos(pitch_rad) + mag_y*math.sin(roll_rad)*math.sin(pitch_rad) + mag_z*math.cos(roll_rad)*math.sin(pitch_rad)
    mag_y_comp1 = mag_y * math.cos(roll_rad) - mag_z * math.sin(roll_rad)
    
    yaw = numpy.arctan2(-mag_y_comp1, mag_x_comp1) 
    yaw = math.sin(yaw)
    yaw = yaw*360
    '''
    if(prevyaw == 0):
        prevyaw = yaw
    elif(yaw > prevyaw and yaw > 0 and yaw < 90):
        yaw = yaw
    elif(yaw < prevyaw and yaw < 90):
        yaw = 180 - yaw
    elif(yaw > prevyaw and yaw < 0):
        yaw = 360 + yaw
    '''
    #REPLACE YOUR NAME WITH MINE HERE
    if(abs(yaw - Sajiv_north) < 7.5):
        return True

    
def endOrbit():
    global orbitCount
    global imgcount
    if(imgcount >= 3):
        orbitCount += 1
        imgcount = 0
        return True
    
def getOrbitCount():
    global orbitCount
    return orbitCount


def getimgcnt():
    global imgcount
    return imgcount
