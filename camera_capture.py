from picamera import PiCamera
import time

def take_picture(orbit_number):
    with PiCamera() as camera:
        timestamp = time.strftime('%S')
        name = '/home/pi/Rubble_Space_Telescope/data_transfer/{}_{}.jpg'.format(orbit_number, timestamp)
        camera.capture(name, quality=75)

    return name
