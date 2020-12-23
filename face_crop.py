import cv2 as cv
import argparse
from source.utils import load_images_from_folder
import  face_detection
import time
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


parser = argparse.ArgumentParser(description='face detection with cascade')
parser.add_argument('--path', help='face detection method path',default='source/haarcascade_frontalface_default.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

path = r'C:\\Users\\MMine\\Google Drive\\ben' #enter your data folder path
output_path = r'C:\\Users\\MMine\\Documents\\Face-Mask-Detection\\dataset\\crop_imp\\' #enter your output folder path !!CREATE FOLDER BEFORE USE THİS CODE!!

print("Loading images...\n")
images=load_images_from_folder(path)
print("Loaded\n")


prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv.dnn.readNet(prototxtPath, weightsPath)
j=62
start =time.time()
for image in images:
    faces_list=face_detection.detect_and_predict_face(image,faceNet)
    for face in faces_list:
        img = cv.resize(face['face'],(240,240))
        cv.imwrite(output_path+"bulduklarimiz_"+str(j)+'_cropped'+'.png',img) #change cropped file name
        
end = time.time()
print("FaceNet Time:",end-start)