#https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html
#https://github.com/shantnu/Webcam-Face-Detect


import cv2 as cv
import argparse
import numpy as np
import sys
import os
from source.utils import draw_rectangle



def recognize_faces(frame,args):
    faces_list = []
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
        start_x = x
        if (start_x - int(w * 0.1) > 0): start_x = start_x - int(w * 0.1)
        end_x = x+w
        if (end_x + int(w * 0.1) < frame.shape[1]): end_x = end_x + int(w * 0.1)
        start_y = y
        if (start_y - int(h * 0.1) > 0): start_y = start_y - int(h * 0.1)
        end_y = y + h
        if (end_y + int(h * 0.1) < frame.shape[0]): end_y = end_y + int(h * 0.1)
        face_dict = {}
        face_dict['rect'] = [start_x, start_y, end_x, end_y]
        face_dict['face'] = frame[start_y:end_y, start_x:end_x, :]
        faces_list.append(face_dict)

    return faces_list


def capture(args):
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
        faces=recognize_faces(frame)
        for face in faces:
            frame=draw_rectangle(frame, face)
        cv.imshow("Detected window", frame)
        if cv.waitKey(10) == 27:  # esc to exit
            break



def __main__(args):
    capture(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='face detection with cascade')
    parser.add_argument('--path', help='face detection method path',default='source/haarcascade_frontalface_default.xml')
    parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
    args = parser.parse_args()

    __main__()
