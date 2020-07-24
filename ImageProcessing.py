import cv2
import numpy as np
import time

class ImageProcessor():
	def __init__(self, image):
		self.image = cv2.imread(image)
		self.contours, self.hierarchy, self.poster_index = self.create_contours()
		self.plastic_contours = self.find_plastic_contours()
	
	@staticmethod
	def biggest_contour(contours):
		max_area = -1
		for i, cnt in enumerate(contours):
			area = cv2.contourArea(cnt)
			if area > max_area:
				max_area = area
				index = i
		return index

	
	def bright(self):
		saturation = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)[..., 1]
		mean = np.mean(saturation)
		return mean > 88


	"""
	Assumes that poster is the biggest contour in the image. 
	Optimal conditions:
	 - Non-reflective floor: carpet, stone, etc.
	 - Bright lighting 
	 - Relatively same lighting over all of the poster
	"""
	def create_contours(self):
		greyscaled = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		max_val = greyscaled.item(np.argmax(greyscaled))
		
		if self.bright():
			ret, thresh = cv2.threshold(greyscaled, max_val-70, 255, cv2.THRESH_BINARY)
		else:
			ret, thresh = cv2.threshold(greyscaled, max_val-150, 255, cv2.THRESH_BINARY)
		cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE)
		
		poster_index = self.biggest_contour(contours)
		poster_contour = contours[poster_index]
		x,y,w,h = cv2.boundingRect(poster_contour)
		poster_contour = cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2) 
		return (contours, hierarchy, poster_index)
		

	def find_plastic_contours(self):
		hierarchy = self.hierarchy[0]
		
		plastic_contours = []
		for i, contour in enumerate(self.contours):
			if i == self.poster_index:
				continue
			epsilon = 0.05*cv2.arcLength(contour, True)
			approx = cv2.approxPolyDP(contour, epsilon, True)
			
			if hierarchy[i][-1] == self.poster_index:
				plastic_contours.append(approx)
		
		return plastic_contours
		
	
	def find_square_types(self):
		"""
		For better measurements, first find the number of each sized plastics,
		then calculate percentage of plastic on board. Maybe compare that to
		other way of calculating percent area to double check
		"""
		square_areas = []
		for contour in self.plastic_contours:
			area = cv2.contourArea(contour)
			if area > 2000:
				square_areas.append(area)
		
		max_area = max(square_areas)
		big_small_ratio = max_area / min(square_areas)
		#0 is small, 1 is medium, 2 is large
		#Organized by ratio number, first spot is outcome if the ratio is same, second for 
		#not same. Same key is set below
		square_types = {'Small-Large': (-1,), 'Small-Medium': (1, 0), 'Medium-Large': (2, 1), 'Same': (-1, -1)}
		if big_small_ratio >= 6:
			#Large and small, possibly medium
			key = 'Small-Large'
		elif big_small_ratio >= 3.5:
			#Medium and small only
			key = 'Small-Medium'
		elif big_small_ratio >= 2:
			#Large and medium only
			key = 'Medium-Large'
		elif big_small_ratio >= 0:
			#Only one size
			key = 'Same'
			area = square_areas[0]
			if area >= 40000:
				square_types['Same'] = (2, 2)
			elif area >= 10000:
				square_types['Same'] = (1, 1)
			else:
				square_types['Same'] = (0, 0)
		
		num_small = 0
		num_medium = 0
		num_large = 0
		poten_types = square_types[key]
		if poten_types[0] == -1:
			for area in square_areas:
				ratio = max_area / area
				if ratio >= 6:
					num_small += 1
				elif ratio >= 2:
					num_medium += 1
				elif ratio >= 0:
					num_large += 1
		else:
			for area in square_areas:
				ratio = max_area / area
				if ratio > 0 and ratio < 2:
					square_type = poten_types[0]
				else:
					square_type = poten_types[1]
				if square_type == 0:
					num_small += 1
				elif square_type == 1:
					num_medium += 1
				elif square_type == 2:
					num_large += 1
			
		return (num_small, num_medium, num_large)


#Testing the Functions
img_name = 'bright'
img_path = 'test_imgs/{}.jpg'.format(img_name)
image_processor = ImageProcessor(img_path)
print(image_processor.find_square_types())
