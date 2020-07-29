import time as t
import os
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

bdaddr = "8C:85:90:A0:D6:84" #bluetooth address
dropboxpath = '/Users/sajivshah/Dropbox/BWSI2020Group5Images'

initial_time = t.time()
hasStarted = False
telemData = ''
init_orbit = 0
orbitCount = 0


"""def startTime():
    global time
    while True:
        t.sleep(1)
        time += 1"""

#this keeps the names of the images from the last captureOrbit
img_names = []
def captureOrbit():
    global telemData
    global img_names
    global initial_time
    global init_orbit
    global orbitCount
    orbitCount += 1
    while True:
        t.sleep(1)
        if orbitCount + init_orbit > 10:
            return None
        if ((t.time() - initial_time)%19 < 3):
            print('taking image')
            img_name = cc.take_picture(imu.getOrbitCount()+init_orbit, len(img_names))
            img_names.append(img_name)
            #Change my name to yours
            #Can be Sajiv, Katrina, or Hasan
            try:
                processor = ip.ImageProcessor(img_name, 'Sajiv')
            except:
                telemdata += "Image Processor Error "
            telemData += processor.find_percentages()
            telemData += 'Image taken at ' + str(t.time() - initial_time) + '\n'
            t.sleep(5)
        if (((t.time() - initial_time)%60 < 5 and (t.time() - initial_time) > 60)  or len(img_names) >= 3):
            print('orbit end')
            telemData += 'Orbit completed at ' + str(t.time() - initial_time) + '/n'
            telemData += 'ADCS good'
            transferOrbit()
            img_names = []


def transferOrbit():
    print('enter transfer orbit')
    global telemData
    global img_names
    global init_orbit
    global orbitCount
    orbitCount += 2
    sendTelem()
    orbit_count = orbitCount + init_orbit
    #Resend image if no ground signal, put in a reboot
    #if 60 seconds have passed with no images transferred
    dt = send_images(img_names)
    if dt > 30:
        dt = send_images(img_names)
    if dt > 30:
        with open('data_transfer/Ground_Comms.txt', mode='w') as f:
            f.write(str(orbit_count)+'\n'+str(t.time() - intial_time()))
        os.system('sudo reboot')


def send_images(img_names):
    print('sending images')
    global bdaddr
    for img_name in img_names:
        successfulTransfer, fileSize, sendTime = bt.sendFile(bdaddr, img_name, dropboxpath) #Put path to your dropbox folder here
    t0 = t.process_time()
    dt = 0
    ground_signal = 0
    fail_count = 0
    while(ground_signal == 0 and dt <= 30):
        dt = t.process_time() - t0
        successfulDownload, fileSize, downloadTime = getFile(bdaddr, dropboxpath + '/ground_signal.txt', '/home/pi/Rubble_Space_Telescope/data_transfer/')
        if not successfulDownload:
            fail_count += 1
        if fail_count >= 9:
            #reboot?
            return dt
        #Put code receviing ground_signal from dropbox folder
        with open('/home/pi/Rubble_Space_Telescope/data_transfer/ground_signal.txt', mode='r') as f:
            signal = f.readline()
            if len(signal) > 0:
                ground_signal = int(signal)
        t.sleep(.05)
    return dt


def sendTelem():
    print('sending telem')
    global telemData
    global bdaddr
    with open('data_transfer/Ground_Comms.txt', mode='w') as f:
        f.write(telemData)
    successfulTransfer, fileSize, sendTime = bt.sendFile(bdaddr, 'data_transfer/Ground_Comms.txt', dropboxpath)
    ground_signal = 0

    telemData = ''

"""
Before running main code, you have to set Ground_comms.txt to 0 and then next line to 0 as well so that the code
knows you are on the first orbit. After ground receives an image, they should write a one
or other number into ground_signal.txt, ground_signal.txt must only have an int or code will error.
"""
def main():
    global init_orbit
    global initial_time
    with open('data_transfer/Ground_Comms.txt', mode='r') as f:
        init_orbit = f.readline()
        if len(init_orbit) > 0:
            init_orbit = int(init_orbit)
    global telemData
    sendTelem()

    hasStarted = False
    while hasStarted == False:
        t.sleep(0.1)
        if(imu.getyaw()):
            initial_time = t.time()
            captureOrbit()
            hasStarted = True

#Run code here
main()
