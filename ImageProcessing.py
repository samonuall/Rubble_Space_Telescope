import cv2
import numpy as np

def biggest_contour(contours):
	max_area = -1
	for i, cnt in enumerate(contours):
		area = cv2.contourArea(cnt)
		if area > max_area:
			max_area = area
			index = i
	return contours[index]

def same_brightness(image):
	saturation = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 1]
	std = np.std(saturation)
	print(std)
	return std < 58

"""
Assumes that poster is the biggest contour in the image. 
Optimal conditions:
 - Non-reflective floor: carpet, stone, etc.
 - Bright lighting 
 - Relatively same lighting over all of the poster
"""
def crop_poster(image):
	image = cv2.imread(image)
	greyscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	if same_brightness(image):
		max_val = greyscaled.item(greyscaled.argmax())
		ret, thresh = cv2.threshold(greyscaled, max_val-80, 255, cv2.THRESH_BINARY)
	else:
		thresh = cv2.adaptiveThreshold(greyscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
									cv2.THRESH_BINARY, 11, 2)
	cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
									cv2.CHAIN_APPROX_SIMPLE)
	cnt = biggest_contour(contours)
	
	leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
	rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
	topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
	bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
	cropped_img = image[topmost[1]: bottommost[1], leftmost[0]: rightmost[0], :]

	
	return (thresh, cropped_img)

name = 'reflected_light'
thresh, cropped_img = crop_poster('test_imgs/{}.jpg'.format(name))
cv2.imshow('Thresh', thresh)
cv2.imshow('Poster', cropped_img)
cv2.waitKey(0)  
cv2.destroyAllWindows()  
