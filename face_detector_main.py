# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from numpy import array, average, sqrt, square
import imutils

from time import time, sleep

from cv2.dnn import readNet,blobFromImage
from cv2 import cvtColor,COLOR_BGR2RGB,resize,putText,FONT_HERSHEY_SIMPLEX,rectangle
from cv2 import imshow, waitKey, destroyAllWindows

import os
import sys

from networking.client import sendClient, client


def detect_and_predict_mask(frame, faceNet, maskNet):

    (h, w) = frame.shape[:2]
    blob = blobFromImage(frame, 1.0, (224, 224),
        (104.0, 177.0, 123.0))

    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []


    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:

            box = detections[0, 0, i, 3:7] * array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")


            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))


            face = frame[startY:endY, startX:endX]
            face = cvtColor(face, COLOR_BGR2RGB)
            face = resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))


    if len(faces) > 0:

        faces = array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    return (locs, preds)


def detection(_consts):
    faceNet = readNet(_consts.path.prototxtPath, _consts.path.weightsPath)
    maskNet = load_model(_consts.path.maskNet)

    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()

    return vs, faceNet, maskNet


def detectionLoop(vs, faceNet, maskNet,SOCKET):

    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    start = time()
    # detect faces in the frame and determine if they are wearing a
    # face mask or not
    try:
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
    except:
        print("Some error occured during detect and predict phase")
        return

    label0 = "Not Found"
    # loop over the detected face locations and their corresponding
    # locations to find the closest to center
    minimum = 0
    selectedbox=None
    selectedpred=None
    width, height = frame.shape[0], frame.shape[1]
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        centerx, centery = (endX-startX)/2, (endY-startY)/2
        proximity = sqrt(square(centerx-width)+square(centery-height))
        boxArea=(endX-startX)*(endY-startY)
        if(boxArea>minimum):
            selectedbox=box
            selectedpred=pred
            minimum = boxArea
    if selectedbox == None:
        return #if no faces detected return
    (startX, startY, endX, endY) = selectedbox
    pred = selectedpred

    (improperMask, withoutMask, mask) = pred
    #print("proper: ", mask, " improper: ", improperMask, " non: ", withoutMask)
    if (mask > withoutMask and mask > improperMask):  # predicted as masked
        # proper improper comparison
        label0 = "Proper Mask"
        color = (0, 255, 0) if label0 == "Proper Mask" else (0, 255, 0)

    elif (improperMask > withoutMask and improperMask > mask):  # predicted as unmasked
        # improper unmasked comparison
        label0 = "Improper Mask"
        color = (255, 255, 0)

    elif (withoutMask > improperMask and withoutMask > mask):  # predicted as unmasked
        # improper unmasked comparison
        label0 = "Non Mask"
        color = (0, 0, 255)

    # include the probability in the label
    label = "{}: {:.2f}%".format(label0, max(mask, improperMask, withoutMask) * 100)

    # display the label and bounding box rectangle on the output
    # frame
    putText(frame, label, (startX, startY - 10),
            FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
    rectangle(frame, (startX, startY), (endX, endY), color, 2)

    end = time()
# show the output frame
    imshow("Frame", frame)

    #print("Latency in miliseconds: ", (end - start) * 1000)

    if(SOCKET != None): sendClient(label0, SOCKET)



if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    sys.path.append(".")
    from main import _consts

    try:
        SOCKET = client()
    except ConnectionRefusedError:
        print("[INFO] No server is found!")
        SOCKET = None
    vs, faceNet, maskNet =detection(_consts)
    while True:
        detectionLoop(vs, faceNet, maskNet, SOCKET)
        key = waitKey(1) & 0xFF
        if key == ord("q"):
            break
    destroyAllWindows()
    vs.stop()
