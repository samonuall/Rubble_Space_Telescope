import subprocess
import time
import os

def getSizeKB(filepath):
    return(os.path.getsize(filepath)/1024.0)

def sendFile(bdaddr, filepath, toDir="/"):
    # Attempts to send a file over obexftp and returns if it was successful or not
    #
    # param:
    #   string bdaddr: the bluetooth device address to send to (must be connected and have file transfer set up to work)
    #   string filepath: the path of the file that will be transmitted to the device
    #
    # return:
    #   boolean successfulTransfer: True or False value representing whether or not the file was successfully sent
    #   float fileSize: the size of the file being sent in kB
    #   int secondsToSend: the time in seconds that it took to send the file
    preTransfer = time.time()
    transferProcess = subprocess.getoutput("obexftp -b {} -c {} -p {}".format(bdaddr, toDir, filepath))
    postTransfer = time.time()
    transferProcess = transferProcess.replace("..."," ").replace(":"," ").replace("."," ").replace("\n"," ").split(" ")

    successfulTransfer = not "failed" in transferProcess
    fileSize = getSizeKB(filepath)
    secondsToSend = postTransfer - preTransfer
    if(successfulTransfer):
        return successfulTransfer, fileSize, secondsToSend
    else:
        return(successfulTransfer, None, None)

def getFile(bdaddr, filepath, toDir=None):
    # Attempts to download a file over obexftp and returns if it was successful or not
    # The file is downloaded to the directory the script was run from, and if specified, is moved to a different directory
    #
    # param:
    #   string bdaddr: the bluetooth device address to download from (must be connected and have file transfer set up to work)
    #   string filepath: the path of the file that will be downloaded from the device
    #   string toDir: the path to the directory the file should be moved to (ex. "path/to/directory/")
    #
    # return:
    #   boolean successfulRetrieval: True or False value representing whether or not the file was retrieved successfully
    #   float fileSize: the size of the file retrieved in kB
    #   int secondsToGet: the time in seconds that it took to retrieve the file
    preRetrieve = time.time()
    retrieveProcess = subprocess.getoutput("obexftp -b {} -g {}".format(bdaddr, filepath))
    postRetrieve = time.time()

    secondsToGet = None
    fileSize = None
    filename = filepath.split("/")[-1]
    fileExists = os.path.isfile(filename)

    if(fileExists):
        if(toDir!=None):
            toDir = toDir + filename
            os.rename(filename, toDir)
        secondsToGet = postRetrieve - preRetrieve
        fileSize = getSizeKB(toDir)
    return(fileExists, fileSize, secondsToGet)
