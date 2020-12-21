import cv2 as cv
import argparse
from source.utils import load_images_from_folder
import  face_detection
import time



parser = argparse.ArgumentParser(description='face detection with cascade')
parser.add_argument('--path', help='face detection method path',default='source/haarcascade_frontalface_default.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

path = 'D:\\Documents\\Lectures 2021\\EE493\\mask_dataset\\imp_new' #enter your data folder path
output_path = 'C:\\Users\\MMine\\Google Drive\\EE493\\dataset\\with_improper_mask\\' #enter your output folder path !!CREATE FOLDER BEFORE USE THİS CODE!!

print("Loading images...\n")
images1=load_images_from_folder(path)
print("Loaded\n")
src = cv.cuda_GpuMat()
print("1")
images = src.upload(images1)
print("2")
j=165

prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv.dnn.readNet(prototxtPath, weightsPath)

start =time.time()
for image in images:
    faces_list=face_detection.detect_and_predict_face(image,faceNet)
    for face in faces_list:
        img = cv.resize(face['face'],(240,240))
        cv.imwrite(output_path+str(j)+'_cropped'+'.png',img) #change cropped file name
        j+=1
    if(j==320): break
end = time.time()
print("FaceNet Time:",end-start)