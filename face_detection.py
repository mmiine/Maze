#https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html
#https://github.com/shantnu/Webcam-Face-Detect


import cv2 as cv
import argparse
import sys
import os
from source.utils import draw_rectangle



def recognize_faces(frame):
    faces_list = []
    min_detection_confidence = 20
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    faceCascade = cv.CascadeClassifier(args.path)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return frame


def capture():
    camera_device = args.camera
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        #cv.imshow("Display window", frame)
        frame=recognize_faces(frame)
        cv.imshow("Detected window", frame)
        if cv.waitKey(10) == 27:  # esc to exit
            break



def __main__():
    capture()

parser = argparse.ArgumentParser(description='face detection with cascade')
parser.add_argument('--path', help='face detection method path',default='source/haarcascade_frontalface_default.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

__main__()

