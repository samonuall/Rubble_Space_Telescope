import os
import subprocess
from picamera import PiCamera
import time

bdaddr = "E0:AC:CB:9D:3F:19" #set bluetooth address to send to

def getFileSizeInKiloBytes(filepath):
    info = os.stat(filepath)
    size = info.st_size
    return(size/1024.0)

t = time.localtime()
current_time = time.strftime("%H-%M-%S", t)

print(current_time)

#you will need to modify filepath to your own directory to save images to
folderpath = '/home/pi/Rubble_Space_Telescope/data_transfer'
filename = 'testPhoto_' + current_time + '.jpg'
filepath = folderpath + filename

customSend = int(input("Enter 0 to capture a compressed image and send\nEnter 1 to send a file from specified directory\nChoice: "))

if(customSend):
    filepath = input("Enter the filepath: ")
else:
    with PiCamera() as camera: 
        camera.capture(filepath)

imgFileSize = getFileSizeInKiloBytes(filepath)

print("Transmitting photo")
now = time.time()
#obexftp -b 20:16:D8:B6:BA:DD -c / -p "filepath"
result = subprocess.getoutput('obexftp -b {}  -c / -p {}'.format(bdaddr, filepath))
later = time.time()
timeDiff = later-now
print("Finished sending a {} kB file over {} seconds. Avg rate of {} kB/s".format(round(imgFileSize,2), round(timeDiff,2), round(imgFileSize/timeDiff,2)))
