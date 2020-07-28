import time as t
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
import imu as imu
import ImageProcessor as ip
import camera_capture as cc

bdaddr = "" #bluetooth address

time = 0
hasStarted = False
telemData = ''


def startTime():
    global time
    while True:
        t.sleep(1)
        time += 1

img_names = []
def captureOrbit():
    global telemData
    global img_names
    img_names = []
    while True:
        t.sleep(1)
        if(imu.getOrbitCount() > 10):
            return None
        if((imu.endorbit() or (time%60) < 3) or ((time%60) < 3)):
            telemData += 'Orbit completed at ' + time + '/n'
            telemData += 'ADCS good'
            bt.sendTelem()
            transferOrbit()
        if(imu.overImage()):
            #camera pic
            img_name = cc.take_picture(imu.getOrbitCount()) #orbitnumber is parameter
            img_names.append(img_name)
            processor = ip.ImageProcessor('data_transfer/{}'.format(img_name))
            telemData += processor.find_percentages()
            telemData += 'Image taken at ' + time + '\n'

def transferOrbit():
    global telemData
    bt.sendFile(bdaddr, img_name, '/BWSI2020Group5Images/')
    while True:
        return None


def sendTelem():
    global telemData
    with open('data_transfer/Ground_Comms.txt', mode='w') as f:
        f.write(telemData)
    bt.sendFile(bdaddr, 'data_transfer/Ground_Comms.txt', '/BWSI2020Group5Images/')
    ground_signal = 0
    while(ground_signal == 0):
        #Check file for number other than zero
        with open('data_transfer/ground_signal.txt', mode='r') as f:
            ground_signal = int(f.readline())
        t.sleep(.05)

    telemData = ''

telemData = imu.imuBoot() +
sendTelem()

while hasStarted == False:
    if(imu.overImage()):
        imu.setimgcnt(0)
        startTime()
        captureOrbit()
        hasStarted = True
