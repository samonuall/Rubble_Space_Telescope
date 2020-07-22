import cv2
import numpy as np
import time

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
	return std < 50


"""
Assumes that poster is the biggest contour in the image. 
Optimal conditions:
 - Non-reflective floor: carpet, stone, etc.
 - Bright lighting 
 - Relatively same lighting over all of the poster
"""
def create_contours(image):
	image = cv2.imread(image)
	greyscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	with open('timer.txt', mode='r') as f:
		prev_dt = float(f.readline())
		
	if same_brightness(image) or prev_dt > 30:
		max_val = greyscaled.item(greyscaled.argmax())
		ret, thresh = cv2.threshold(greyscaled, max_val-80, 255, cv2.THRESH_BINARY)
	else:
		thresh = cv2.adaptiveThreshold(greyscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
									cv2.THRESH_BINARY, 11, 2)
	t0 = time.process_time()
	cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
									cv2.CHAIN_APPROX_SIMPLE)
	
	if prev_dt <=30:
		dt = time.process_time() - t0
		with open('timer.txt', mode='w') as f:
			f.write(str(round(dt, 2)))

	return (image, thresh, contours)

def crop_poster(image, contours):
	cnt = biggest_contour(contours)
	
	leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
	rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
	topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
	bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
	cropped_img = image[topmost[1]: bottommost[1], leftmost[0]: rightmost[0], :]
	
	return cropped_img

#Example Code
img_name = 'good'
img_path = 'test_imgs/{}.jpg'.format(img_name)
image, thresh, contours = create_contours(img_path)
cropped_img = crop_poster(image, contours)
cv2.imshow('Thresh', thresh)
cv2.imshow('Poster', cropped_img)
cv2.waitKey(0)  
cv2.destroyAllWindows()  
