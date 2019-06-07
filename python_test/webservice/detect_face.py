from random import randint
import cv2
import sys
import os
from flask import Flask, jsonify
      
CASCADE="Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)

def detect_faces(image_path):
    
	print("******#*#**#*#*#*#*#*   "+image_path)
	if not "Extracted" in os.listdir("."):
		os.mkdir("Extracted")
	image=cv2.imread(image_path)
	image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(25,25),flags=0)
	imageArray=[]
    
	for x,y,w,h in faces:
	    
	    sub_img=image[y-10:y+h+10,x-10:x+w+10]
	    os.chdir("Extracted")
	    img_name =str(randint(0,10000))+".jpg"
	    cv2.imwrite(str(randint(0,10000))+".jpg",sub_img)
	    os.chdir("../")
	    cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)
	    imageArray.append(img_name)
	return (imageArray)