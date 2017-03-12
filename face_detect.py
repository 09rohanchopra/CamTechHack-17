import numpy as np
import cv2
from pygame.locals import *
import pygame
import os
import numpy as np
import math
def mask_image_by_feature(image, feature):
    circle_mask_image = np.zeros(image.shape, dtype=np.uint8)
    #cv2.circle(circle_mask_image, (int(feature.pt[0]), int(feature.pt[1])), int(feature.size/2), 1, -1)
    masked_image = (image * circle_mask_image).astype(np.uint8)
    return masked_image

def find_average_brightness_of_feature(image, feature):
    feature_image = mask_image_by_feature(image, feature)
    total_value = feature_image.sum()
    area = np.pi * ((feature.size/2)**2)
    return total_value/area

def sort_features_by_brightness(image, features):
    features_and_brightnesses = [(find_average_brightness_of_feature(image, feature), feature) for feature in features]
    features_and_brightnesses.sort(key = lambda x:x[0])
    return [fb[1] for fb in features_and_brightnesses]

def draw_circle_for_feature(image, feature, color=255, thickness=0.01):
    #cv2.circle(image, (int(feature.pt[0]), int(feature.pt[1])), int(feature.size/2), color, thickness)
    print 'nice'


def find_pupil(gray_image, minsize=.1, maxsize=.5):
    detector = cv2.FeatureDetector_create('MSER')
    features_all = detector.detect(gray_image)
    features_big = [feature for feature in features_all if feature.size > gray_image.shape[0]*minsize]
    features_small = [feature for feature in features_big if feature.size < gray_image.shape[0]*maxsize]
    if len(features_small) == 0:
        return None
    features_sorted = sort_features_by_brightness(gray_image, features_small)
    pupil = features_sorted[0]
    return (int(pupil.pt[0]), int(pupil.pt[1]), int(pupil.size/2))

def circle_pupil(color_image, output_image = None):
    if output_image is None:
        output_image = color_image
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
    pupil_coords = find_pupil(gray_image)
    if pupil_coords is not None:
        cv2.circle(output_image, pupil_coords[:2], pupil_coords[2], (0,255,0),1)
    cv2.imwrite('left.jpg',output_image)
    return pupil_coords

def draw(photo):
    image_to_show = photo.copy()
    e=circle_pupil(image_to_show)
    #cv2.imshow('Image', image_to_show)
    if cv2.waitKey(10) > 0: #If we got a key press in less than 10ms
        return None
    return e




def startH():

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	pygame.init()
	cap = cv2.VideoCapture(1)

	while 1:
		
			
		ret, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		

		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			
			i=0
			pup_list=[]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			
			for (ex,ey,ew,eh) in eyes:
				temp=img[y+ey:y+ey+eh,x+ex:x+ex+ew]
				left_eye=img[y+ey:y+ey+eh,x+ex:x+ex+ew]
				if(i==0):
					right_eye=temp
				else:
					left_eye=temp
				i=i+1
					
				
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
				cv2.circle(roi_color,((2*ex+ew)/2,(2*ey+eh)/2),2,(0,255,0),1)
				pup_list.append(((2*ex+ew)/2,(2*ey+eh)/2))
				cv2.imwrite('left_eye.jpg',left_eye)
				cv2.imwrite('right_eye.jpg',right_eye)
				le=draw(left_eye)

			if len(pup_list)==2:
				cv2.line(roi_color,pup_list[0],pup_list[1],(0,255,0),1)
				p1=pup_list[0]
				p2=pup_list[1]
				distance_pixel= math.hypot(p2[0] - p1[0], p2[1] - p1[1])
				
			
			
				
				
		
	  
		cv2.imshow('img',img)
		k = cv2.waitKey(30) & 0xff
		if chr(k) == 'c':
			cv2.imwrite('face_detected.jpg',img)
			os.system('pupil_detect_left.py')
			os.system('pupil_detect_right.py')
			
			break
	return distance_pixel
	cap.release()
	cv2.destroyAllWindows()

