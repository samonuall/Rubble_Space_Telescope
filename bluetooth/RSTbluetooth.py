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
