#this sends the same image multiple times, recording the data transfer rate each time for data insight
import os
import subprocess
from picamera import PiCamera
import time

camera = PiCamera()
bdaddr = "20:16:D8:B6:BA:DD" 

kbRates = []
maxkbRate = 0.0
minkbRate = 1000000000.0

def getFileSizeInKiloBytes(filepath):
    info = os.stat(filepath)
    size = info.st_size
    return(size/1024.0)

t = time.localtime()
current_time = time.strftime("%H-%M-%S", t)

print(current_time)

#you will need to modify filepath to your own directory
folderpath = '/home/pi/bwsi_scripts/bluetoothTesting/btImages/'
filename = 'testPhoto_' + current_time + '.jpg'
filepath = folderpath + filename

customSend = int(input("Enter 0 to capture a compressed image and send\nEnter 1 to send a file from specified directory\nChoice: "))

if(customSend):
    filepath = input("Enter the filepath: ")
else:
    camera.capture(filepath)

imgFileSize = getFileSizeInKiloBytes(filepath)

iterations = int(input("How many times should the image be sent: "))
for i in range(0,iterations):
    print("Transmitting photo {}".format(i+1))
    now = time.time()
    #obexftp -b 20:16:D8:B6:BA:DD -c / -p "filepath"
    #transferProcess = subprocess.Popen(['obexftp','-b', bdaddr, '-c' , '/' , '-p', filepath])
    transferProcess = subprocess.getoutput("obexftp -b {} -c / -p {}".format(bdaddr, filepath))

    later = time.time()
    timeDiff = later-now

    kbRate = round(imgFileSize/timeDiff,2)
    kbRates.append(kbRate)

    if(kbRate < minkbRate):
        minkbRate = kbRate
    if(kbRate > maxkbRate):
        maxkbRate = kbRate

print("Finished sending all the photos")
kbSum = 0
for rate in kbRates:
    kbSum += rate
avgkbRate = round(0.0 + kbSum/len(kbRates),2)
print("Slowest rate recorded was {}, and fastest was {}".format(minkbRate, maxkbRate))
print("Average file transfer rate: {} kB/s".format(avgkbRate))
