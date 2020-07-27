from picamera import PiCamera
import time

def take_picture(orbit_number):
	with PiCamera() as camera:
		print('Brightness', camera.brightness)
		print('Saturation', camera.saturation)
		print('Contrast', camera.contrast)
		print('Sharpness', camera.sharpness)
		timestamp = time.strftime('%M:%s')[:-8]
		name = 'data_transfer/{}_{}.jpg'.format(orbit_number, timestamp)
		#camera.capture(name, quality=100)

	return name
#Test function
take_picture(1)
