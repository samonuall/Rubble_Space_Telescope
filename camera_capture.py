from picamera import PiCamera

def take_picture(orbit_number, index):
    with PiCamera() as camera:
        name = '/home/pi/Rubble_Space_Telescope/data_transfer/{}_{}.jpg'.format(orbit_number, index)
        camera.capture(name, quality=75)

    return name
