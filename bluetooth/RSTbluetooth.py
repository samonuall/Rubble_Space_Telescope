import subprocess

def sendFile(bdaddr, filepath):
    # Attempts to send a file over obexftp and returns if it was successful or not
    #
    # param:
    #   string bdaddr: the bluetooth device address to send to (must be connected and have file transfer set up to work)
    #   string filepath: the path of the file that will be transmitted
    #
    # return:
    #   True: the file was sent successfully over obexftp
    #   False: the file was not sent successfully
    transferProcess = subprocess.getoutput("obexftp -b {} -c / -p {}".format(bdaddr, filepath))
    transferProcess = transferProcess.replace("..."," ").replace(":"," ").replace("."," ").replace("\n"," ").split(" ")
    return(not "failed" in transferProcess)

def getFile(bdaddr, filepath):
    # Attempts to download a file over obexftp and returns if it was successful or not
    # The file is downloaded to the directory of the python script it is run from
    #
    # param:
    #   string bdaddr: the bluetooth device address to download from (must be connected and have file transfer set up to work)
    #   string filepath: the path of the file that will be downloaded
    #
    # return:
    #   True: the file was downloaded successfully over obexftp
    #   False: the file was not downloaded successfully
    retrieveProcess = subprocess.getoutput("obexftp -b {} -g {}".format(bdaddr, filepath))
    retrieveProcess = retrieveProcess.replace("..."," ").replace(":"," ").replace("."," ").replace("\n"," ").split(" ")
    return(not "failed" in retrieveProcess)

