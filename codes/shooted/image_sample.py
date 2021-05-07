import imutils
import os
import cv2
from imutils.video import VideoStream


vs = VideoStream(src=0).start()
i=65
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("t"):
        i=i+1
        cv2.imwrite("rpiphoto_"+str(i)+".png",frame)