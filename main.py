from face_detector.mask_detector import detection
import os



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



os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

detection(_consts)