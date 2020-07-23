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
	max_val = greyscaled.item(np.argmax(greyscaled))
	
	if bright(image):
		ret, thresh = cv2.threshold(greyscaled, max_val-70, 255, cv2.THRESH_BINARY)
	else:
		ret, thresh = cv2.threshold(greyscaled, max_val-150, 255, cv2.THRESH_BINARY)
	cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
									cv2.CHAIN_APPROX_SIMPLE)
	
	return (image, thresh, contours)

def find_extremes(cnt):
	leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
	rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
	topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
	bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
	return (leftmost, rightmost, topmost, bottommost)

def find_plastic_contours(image, contours):
	cnt = biggest_contour(contours)
	#Poster edge extremes
	p_leftmost, p_rightmost, p_topmost, p_bottommost = find_extremes(cnt)
	cv2.circle(image, p_leftmost, 5, (255, 0, 0), 3)
	cv2.circle(image, p_rightmost, 5, (255, 0, 0), 3)
	cv2.circle(image, p_bottommost, 5, (255, 0, 0), 3)
	cv2.circle(image, p_topmost, 5, (255, 0, 0), 3)
	
	plastic_contours = []
	for contour in contours:
		if contour is cnt:
			continue
		epsilon = 0.05*cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, epsilon, True)
		
		leftmost, rightmost, topmost, bottommost = find_extremes(approx)
		if (leftmost[0] < p_leftmost[0] or rightmost[0] > p_rightmost[0]
			or topmost[1] < p_topmost[1] or bottommost[1] > p_bottommost[1]):
			continue
		plastic_contours.append(approx)
	
	return (poster_contour, plastic_contours)
	
def find_percentages(poster_contour, plastic_contours):
	plastic_area = 0
	poster_area = cv2.contourArea(poster_contour)
	for contour in plastic_contours:
		plastic_area += cv2.contourArea(contour)
	area_percent = (poster_area - plastic_area) / poster_area
	

#Example Code
img_name = 'blurry'
img_path = 'test_imgs/{}.jpg'.format(img_name)
image, thresh, contours = create_contours(img_path)
plastic_contours = find_plastic_contours(image, contours)

image = cv2.drawContours(image, plastic_contours, -1, (0, 255, 0), 3)
image2 = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
cv2.imshow('Plastic Contours', image)
cv2.imshow('All Contours', image2)
cv2.waitKey(0)  
cv2.destroyAllWindows()
