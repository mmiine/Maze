import os
from multiprocessing import Process
from cv2 import waitKey, destroyAllWindows

from face_detector.mask_detector import detection, detectionLoop




class _consts:

    class pin:
        '''
        Pin Assigments
        '''
        TRIGIN = 23
        ECHOIN = 24
        TRIGOUT = 21
        ECHOOUT = 20
        TRIGCHK = 6
        ECHOCHK = 5
        SERVO1 = 17
        PWM1 = None

    class pre:
        '''
        Predetermined Constants
        '''
        maxNum = 100
        waitingTime = 5 # in seconds

        servoOpenAngle = 90
        servoCloseAngle = 0

    class path:
        '''
        Paths
        '''
        maskNet = r"face_detector\mask_detector.model"
        prototxtPath = r"face_detector\deploy.prototxt"
        weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"





if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    try:
        import RPi.GPIO as gpio
        raspberry = True
    except (ImportError, RuntimeError):
        raspberry = False

    vs, faceNet, maskNet =detection(_consts)

    if (raspberry):
        from sensor.DDSubsytem import DecisionDetection, DDLoop
        DDTuple = DecisionDetection(_consts)

    while True:
        label = detectionLoop(vs, faceNet, maskNet)
        if label == "Proper Mask":
            print("\n",label,"\n")
        if (raspberry): crowd = DDLoop(DDTuple, crowd, label)

        key = waitKey(1) & 0xFF
        if key == ord("q"):
            break
    destroyAllWindows()
    vs.stop()

#Process(target=, args=(_consts,)).start()