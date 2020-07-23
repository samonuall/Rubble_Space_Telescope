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
	return index

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
	
	return (image, thresh, contours, hierarchy)

def find_extremes(cnt):
	leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
	rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
	topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
	bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
	return (leftmost, rightmost, topmost, bottommost)

def find_plastic_contours(image, contours, hierarchy):
	poster_index = biggest_contour(contours)
	print(poster_index)
	hierarchy = hierarchy[0]
	#Poster edge extremes
	
	plastic_contours = []
	for i, contour in enumerate(contours):
		if i is poster_index:
			continue
		epsilon = 0.05*cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, epsilon, True)
		
		if hierarchy[i][-1] == poster_index:
			plastic_contours.append(approx)
	
	return (plastic_contours)
	
def find_percentages(plastic_contours):
	"""
	For better measurements, first find the number of each sized plastics,
	then calculate percentage of plastic on board. Maybe compare that to
	other way of calculating percent area to double check
	"""
	for contour in plastic_contours:
		area = cv2.contourArea(contour)
		if area > 
		
	pass
	

#Example Code
img_name = 'good'
img_path = 'test_imgs/{}.jpg'.format(img_name)
image, thresh, contours, hierarchy = create_contours(img_path)
plastic_contours = find_plastic_contours(image, contours, hierarchy)
find_percentages(plastic_contours)
image = cv2.drawContours(image, plastic_contours, -1, (0, 255, 0), 3)
image2 = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
cv2.imshow('Plastic Contours', image)
cv2.imshow('All Contours', image2)
cv2.waitKey(0)  
cv2.destroyAllWindows()
