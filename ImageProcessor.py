import cv2
import numpy as np
import time

class ImageProcessor():
	def __init__(self, image, person):
		global sam_blue
		global sam_red
		global hasan_blue
		global hasan_red
		global sajiv_red
		global sajiv_blue
		global kat_red
		global kat_blue
		
		sam_red = 120
		sam_blue = 60
		kat_red = 114
		kat_blue = 104
		hasan_red = 160
		hasan_blue = 110
		sajiv_red = 160
		sajiv_blue = 110
		if person == 'Sam':
			self.blue = sam_blue
			self.red = sam_red
		elif person == 'Hasan':
			self.blue = hasan_blue
			self.red = hasan_red
		elif person == 'Sajiv':
			self.blue = sajiv_blue
			self.red = sajiv_red
		elif person == 'Katrina':
			self.blue = kat_blue
			self.red = kat_red
		self.img_name = image
		self.image = cv2.imread(image)
		self.contours, self.hierarchy, self.poster_index = self.create_contours()
		#This variable will be in the form [[contour, type, color], [contour, type, color]].
		#Type and color are calculated in later functions, for now variable only holds contours
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



	"""
	Assumes that poster is the biggest contour in the image. 
	Optimal conditions:
	 - Non-reflective floor: carpet, stone, etc.
	 - Bright lighting 
	 - Relatively same lighting over all of the poster
	"""
	def create_contours(self):
		greyscaled = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.image_HSV = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
		max_val = greyscaled.item(np.argmax(greyscaled))
		
		ret, thresh = cv2.threshold(greyscaled, max_val-100, 255, cv2.THRESH_BINARY)
		cont_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE)
		
		#Create box around poster then make greyscale white around the edges of the 
		#poster board so that plastics on the edge are recognized as seperate contours
		poster_index = self.biggest_contour(contours)
		cnt = contours[poster_index]
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		contours[poster_index] = np.int0(box)
		"""cv2.drawContours(greyscaled, [contours[poster_index]], 0, 255, 5)
		
		if self.bright():
			ret, thresh = cv2.threshold(greyscaled, max_val-70, 255, cv2.THRESH_BINARY)
		else:
			ret, thresh = cv2.threshold(greyscaled, max_val-150, 255, cv2.THRESH_BINARY)
		
		cont_img, contours1, hierarchy1 = cv2.findContours(thresh, cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE)
		
		poster_index = self.biggest_contour(contours1)
		image1 = self.image.copy()
		cv2.drawContours(image1, contours, -1, (255, 0, 0), 3)
		cv2.imshow('thresh', thresh)
		cv2.waitKey(0)
		cv2.destroyAllWindows()"""
		return (contours, hierarchy, poster_index)
	
		
		
	def find_plastic_contours(self):
		hierarchy = self.hierarchy[0]
		
		self.square_areas = []
		plastic_contours = []
		for i, contour in enumerate(self.contours):
			if i == self.poster_index:
				continue
			area = cv2.contourArea(contour)
			if area < 2000:
				continue
			
			epsilon = 0.05*cv2.arcLength(contour, True)
			approx = cv2.approxPolyDP(contour, epsilon, True)
			
			if hierarchy[i][-1] == self.poster_index:
				plastic_contours.append([approx])
				self.square_areas.append(area)
		
		if len(self.square_areas) == 0:
			self.square_areas = -1
		return plastic_contours
		
	
	def find_square_types(self):
		"""
		Compares size of plastic contours to each other and designates squares
		as small, medium, or large based on their ratios to each other. For
		each contour its type will be added to its list in plastic_contours;
		0 means small, 1 means medium, and 2 means large.
		"""
		
		if self.square_areas == -1:
			return
		max_area = max(self.square_areas)
		big_small_ratio = max_area / min(self.square_areas)
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
			area = self.square_areas[0]
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
			for i, area in enumerate(self.square_areas):
				ratio = max_area / area
				if ratio >= 6:
					self.plastic_contours[i].append(0)
				elif ratio >= 2:
					self.plastic_contours[i].append(1)
				elif ratio >= 0:
					self.plastic_contours[i].append(2)
		else:
			for i, area in enumerate(self.square_areas):
				ratio = max_area / area
				if ratio > 0 and ratio < 2:
					square_type = poten_types[0]
				else:
					square_type = poten_types[1]
				if square_type == 0:
					self.plastic_contours[i].append(0)
				elif square_type == 1:
					self.plastic_contours[i].append(1)
				elif square_type == 2:
					self.plastic_contours[i].append(2)
		
		
	def calc_square_color(self, cnt, index):
		#Find center of contour and then find mean hue value of small
		#rectangle in center
		if self.square_areas == -1:
			self.plastic_contours.pop(index)
			return
		M = cv2.moments(cnt)
		if M['m00'] == 0:
			self.square_areas = -1
			return
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		length = 50 #Set length of rectangle that is being used to calculate color 
		mean_h_val = cv2.mean(self.image_HSV[cy-length:cy+length,cx-length:cx+length])[:-1]
		
		if mean_h_val[0] >= self.red:
			self.plastic_contours[index].append('Sam')
			print(mean_h_val, 'Red')
		elif mean_h_val[0] >= self.blue:
			self.plastic_contours[index].append('Blue')
			print(mean_h_val, 'Blue')
		else:
			self.plastic_contours[index].append('Green')
			print(mean_h_val, 'Green')
			
			
	def find_percentages(self):
		self.find_square_types()
		if self.square_areas == -1:
			return 'Image doesnt include poster'
		for i, cnt in enumerate(self.plastic_contours):
			self.calc_square_color(cnt[0], i)
		
		color_areas = [0, 0, 0]
		total_types = [0, 0, 0]
		areas = {0: 1, 1: 4, 2: 12.25}
		for cnt_data in self.plastic_contours:
			try:
				contour, square_type, color = cnt_data
			except:
				return 'Image Error'
			total_types[square_type] += 1
			if color is 'Red':
				color_areas[0] += areas[square_type]
			elif color is 'Green':
				color_areas[1] += areas[square_type]
			elif color is 'Blue':
				color_areas[2] += areas[square_type]
		
		name = self.img_name+'\n'
		square_sizes = 'Square sizes: {} small {} medium {} large'.format(total_types[0], 
													total_types[1], total_types[2])
		total_area = sum(color_areas)
		color_percents = 'Color percents: {}% red {}% green {}% blue'.format(color_areas[0]/total_area*100,
													color_areas[1]/total_area*100, color_areas[2]/total_area*100)
		plastic_percent = '{}% of the board has plastic on it'.format(total_area / 154 * 100)
		return name+'\n'+square_sizes+'\n'+color_percents+'\n'+plastic_percent+'\n\n'
		

def instructor_test(person, img_path):
	global sam_blue
	global sam_red
	global hasan_blue
	global hasan_red
	global sajiv_red
	global sajiv_blue
	global kat_red
	global kat_blue
	
	image_processor = ImageProcessor(img_path, person)
	print(image_processor.find_percentages())

#Testing the Functions
"""img_name = 'far_away'
img_path = '/home/pi/Rubble_Space_Telescope/test_imgs/{}.jpg'.format(img_name)
image_processor = ImageProcessor(img_path, 'Sam')
print(image_processor.find_percentages())"""

#Uncomment for instructor testing, change name to person that was in orbit for the picure,
#and change 'test.jpg' to the image pathname
#instructor_test('Sam', 'test.jpg')
