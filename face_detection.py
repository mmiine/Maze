#https://docs.opencv.org/master/db/d28/tutorial_cascade_classifier.html
#https://github.com/shantnu/Webcam-Face-Detect


import cv2 as cv
import argparse
import numpy as np
import sys
import os
from source.utils import draw_rectangle
from numba import vectorize


def detect_and_predict_face(frame, faceNet):
    (h, w) = frame.shape[:2]
    blob = cv.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()
    #print(detections.shape)
    faces_list = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv.cvtColor(face, cv.COLOR_BGR2RGB)
            face = cv.resize(face, (224, 224))
            face_dict = {}
            face_dict['rect'] = [startX, startY, endX, endY]
            face_dict['face'] = frame[startY:endY, startX:endX, :]
            faces_list.append(face_dict)
    return faces_list


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
        end_x = x+w
        start_y = y
        end_y = y + h
        face_dict = {}
        face_dict['rect'] = [start_x, start_y, end_x, end_y]
        face = frame[start_y:end_y, start_x:end_x, :]
        face = cv.resize(face, (224, 224))
        face_dict['face'] = face
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
