import time
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy as np
import math
import imu
import RSTbluetooth as bt
from RSTbluetooth import *
from RSTbluetooth import *
from imu import *
from ImageProcessor import *
from camera_capture import *

bdaddr = "8C:85:90:A0:D6:84" #bluetooth address

telemData = imuBoot() 
sendTelem()

time = 0
hasStarted = False
telemData = ''

while hasStarted == False:
    if(overImage()):
        setimgcnt(0)
        startTime()
        captureOrbit()
        hasStarted = True

def startTime():
    global time
    while True:
        time.sleep(1)
        time += 1

def captureOrbit():
    global telemData
    while True:
        time.sleep(1)
        if(getOrbitCount() > 10):
            return None
        if((endorbit() or (time%60) < 3) or ((time%60) < 3)):
            telemData += 'Orbit completed at ' + time + '/n'
            telemData += 'ADCS good'
            sendTelem()
            transferOrbit()
        if(overImage()):
            #camera pic
            img_name = take_picture(getOrbitCount()) #orbitnumber is parameter
            processor = ImageProcessor('data_transfer/{}'.format(img_name))
            telemData += processor.find_percentages()
            telemData += 'Image taken at ' + time + '\n'

def transferOrbit():
    global telemData
    #bt code to send images
    while True:
        passing = overImage(endorbit() or ((time%60) < 3))
        return
        
def sendTelem():
    global telemData
    with open('data_transfer/Ground_Comms.txt', mode='w') as f:
        f.write(telemData)
        bt.sendFile(bdaddr, 'data_transfer/Ground_Comms.txt')
    ground_signal = 0
    while(ground_signal == 0):
        #Check file for number other than zero
        with open('data_transfer/ground_signal.txt', mode='r') as f:
            ground_signal = int(f.readline())
        time.sleep(.05)

    telemData = ''
