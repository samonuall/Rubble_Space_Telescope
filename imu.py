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

Sajiv_mag_offset = [15.15, 15.15, 15.15]
Sajiv_mag_scale = [0.97, 1, 1.03]


def imuBoot():
    global telemString
    return 'ADCS is go for launch /n' ;
def getyaw():
    global prevyaw
    global yaw
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    
    mag_x = mag_x*Sajiv_mag_scale[0] - Sajiv_mag_offset[0]
    mag_y = mag_y*Sajiv_mag_scale[1] - Sajiv_mag_offset[1]
    mag_z = mag_z*Sajiv_mag_scale[2] - Sajiv_mag_offset[2]
    
    pitch = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    pitch_corrected = 180 * numpy.arctan2(accel_x, (accel_y*accel_y + accel_z*accel_z)**0.5)/numpy.pi
    if accel_x >= 0 and accel_z >= 0 : 
        pass
    elif accel_z <= 0 and accel_x >= 0 :
        pitch_corrected = 180 - pitch
    elif accel_z <= 0 and accel_x < 0 :
        pitch_corrected = 180 - pitch
    elif accel_z >= 0 and accel_x <= 0 :
        pitch_corrected = pitch + 360

     
    roll = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    roll_corrected = (180) * numpy.arctan2(accel_y, (accel_x*accel_x + accel_z*accel_z)**0.5)/numpy.pi
    if accel_z >= 0 and accel_y < 0:
        pass
    if accel_z <= 0 and accel_y < 0:
        roll_corrected = 180 - roll
    if accel_z <= 0 and accel_y > 0:
        roll_corrected = 180 - roll
    if accel_z > 0 and accel_y >= 0:
        roll_corrected = roll + 360

    roll_rad = roll*numpy.pi/180
    pitch_rad = pitch*numpy.pi/180
    
    mag_x_comp1 = mag_x*math.cos(pitch_rad) + mag_y*math.sin(roll_rad)*math.sin(pitch_rad) + mag_z*math.cos(roll_rad)*math.sin(pitch_rad)
    mag_y_comp1 = mag_y * math.cos(roll_rad) - mag_z * math.sin(roll_rad)
    
    yaw = numpy.arctan2(-mag_y_comp1, mag_x_comp1) - 1.55
    yaw = 150*math.sin(yaw)
    nonmanipyaw = yaw
    
    if(prevyaw == 0):
        prevyaw = yaw
        #print('one')
    elif(yaw > prevyaw and yaw > 0 and yaw < 90):
        yaw = yaw
    elif(yaw < prevyaw and yaw < 90):
        yaw = 180 - yaw
    elif(yaw > prevyaw and yaw < 0):
        yaw = 360 + yaw

    prevyaw = nonmanipyaw - 1
    return yaw


def overImage():
    global yaw
    global telemString
    global imgcount
    yaw = getyaw()
    if((yaw >= 350 and yaw <= 360) or (yaw >= 0 and yaw <= 10) or (yaw >= 110 and yaw <= 130) or (yaw >= 230 and yaw <= 250)):
        print('in if')
        imgcount += 1
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


def setimgcnt(count):
    global imgcount
    imgcount = count
    


