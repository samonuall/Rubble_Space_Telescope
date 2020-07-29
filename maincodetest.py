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

bdaddr = "8C:85:90:A0:D6:84"
dropboxpath = '/Users/sajivshah/Dropbox/BWSI2020Group5Images'#bluetooth address

initial_time = t.time()
hasStarted = False
telemData = ''
init_orbit = 0


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
    img_names = []
    while True:
        t.sleep(1)
        if imu.getOrbitCount()+init_orbit > 10:
            return None
        if imu.overImage() or (t.time() - initial_time)%19 < 3:
            print('taking image')
            img_name = cc.take_picture(imu.getOrbitCount()+init_orbit)
            img_names.append(img_name)
            processor = ip.ImageProcessor(img_name)
            telemData += processor.find_percentages()
            telemData += 'Image taken at ' + str(t.time() - initial_time) + '\n'
            t.sleep(5)
        if ((t.time() - initial_time)%60 < 5):
            print('orbit end')
            telemData += 'Orbit completed at ' + str(t.time() - initial_time) + '/n'
            telemData += 'ADCS good'
            transferOrbit()
       
            
def transferOrbit():
    print('enter transfer orbit')
    global telemData
    global img_names
    global init_orbit
    orbit_count = imu.getOrbitCount() + init_orbit
    #Resend image if no ground signal, put in a reboot
    #if 60 seconds have passed with no images transferred
    for img_name in img_names:
        dt = send_images(img_names)
        for i in range(3):
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
        bt.sendFile(bdaddr, img_name, dropboxpath) #Put path to your dropbox folder here
    t0 = t.process_time()
    dt = 0
    ground_signal = 0
    while(ground_signal == 0 and dt <= 30):
        dt = t.process_time() - t0
        #Check file for number other than zero
        with open('/home/pi/Rubble_Space_Telescope/data_transfer/Ground_Comms.txt', mode='r') as f:
            ground_signal = int(f.readline())
        t.sleep(.05)
    return dt


def sendTelem():
    print('sending telem')
    global telemData
    global bdaddr
    with open('data_transfer/Ground_Comms.txt', mode='w') as f:
        f.write(telemData)
    bt.sendFile(bdaddr, 'data_transfer/Ground_Comms.txt', dropboxpath)
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
        init_orbit = int(f.readline())     
    global telemData
    sendTelem()
    
    hasStarted = False
    while hasStarted == False:
        t.sleep(0.5)
        if(imu.getyaw() >= 355 or imu.getyaw() <= 5):
            initial_time = t.time()
            captureOrbit()
            hasStarted = True

#Run code here
main()
