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

def bright(image):
	saturation = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 1]
	mean = np.mean(saturation)
	print(mean)
	return mean > 88


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
	
	if bright(image) or prev_dt > 30:
		ret, thresh = cv2.threshold(greyscaled, max_val-70, 255, cv2.THRESH_BINARY)
	else:
		ret, thresh = cv2.threshold(greyscaled, max_val-150, 255, cv2.THRESH_BINARY)
	
	t0 = time.process_time()
	cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
									cv2.CHAIN_APPROX_SIMPLE)
	
	return (image, thresh, contours)

def find_extremes(cnt):
	leftmost = cnt[cnt[:,:,0].argmin()][0][0]
	rightmost = cnt[cnt[:,:,0].argmax()][0][0]
	topmost = cnt[cnt[:,:,1].argmin()][0][1]
	bottommost = cnt[cnt[:,:,1].argmax()][0][0]
	return (leftmost, rightmost, topmost, bottommost)

def find_plastic_contours(image, contours):
	cnt = biggest_contour(contours)
	#Poster edge extremes
	p_leftmost, p_rightmost, p_topmost, p_bottommost = find_extremes(cnt)
	
	plastic_contours = []
	for contour in contours:
		leftmost, rightmost, topmost, bottommost = find_extremes(contour)
		if (leftmost < p_leftmost or rightmost > p_rightmost
			or topmost < p_topmost or bottommost > p_bottommost):
			continue
		plastic_contours.append(contour)
	
	return plastic_contours
	
	

#Example Code
img_name = 'good'
img_path = 'test_imgs/{}.jpg'.format(img_name)
image, thresh, contours = create_contours(img_path)
plastic_contours = find_plastic_contours(image, contours)

image = cv2.drawContours(image, plastic_contours, -1, (0, 255, 0), 3)
image2 = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
cv2.imshow('Plastic Contours', image)
cv2.imshow('All Contours', image2)
cv2.waitKey(0)  
cv2.destroyAllWindows()
