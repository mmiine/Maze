import cv2 as cv
import argparse
import numpy as np
import sys
import os
from source.utils import load_images_from_folder
import  face_detection



parser = argparse.ArgumentParser(description='face detection with cascade')
parser.add_argument('--path', help='face detection method path',default='source/haarcascade_frontalface_default.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

path = 'D:\\Documents\\Lectures 2021\\EE493\\mask_dataset\\fask-mask-improper\\improper-wear-dataset' #enter your data folder path
output_path = 'D:\\Documents\\Lectures 2021\\EE493\\mask_dataset\\fask-mask-improper\\improper-cropped\\' #enter your output folder path !!CREATE FOLDER BEFORE USE THİS CODE!!
j=0

images=load_images_from_folder(path)

for image in images:
    faces_list=face_detection.recognize_faces(image,args)
    for face in faces_list:
        cv.imwrite(output_path+str(j)+'_cropped'+'.png',face['face']) #change cropped file name
        j+=1
