import os
from multiprocessing import Process
from cv2 import waitKey, destroyAllWindows

from face_detector.mask_detector import detection, detectionLoop
from networking.client import client, recieveClient, sendClient

from time import sleep, time, localtime

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
        SERVO1 = 18
        PWM1 = None

    class pre:
        '''
        Predetermined Constants
        '''
        maxNum = 100
        waitingTime = 5 # in seconds

        servoOpenAngle = 90
        servoCloseAngle = 45
        clientSocketS = None
        clientSocketR = None

    class path:
        '''
        Paths
        '''
        maskNet = r"face_detector/mask_detector.model"
        prototxtPath = r"face_detector/deploy.prototxt"
        weightsPath = r"face_detector/res10_300x300_ssd_iter_140000.caffemodel"

def processA(SOCKET):
    label0 = 0
    while True:
        label0 = label0 + 1
        sleep(8)
        sendClient(str(label0), SOCKET)
        print("sendtime: ",localtime())

def processB(SOCKET):
    data = None
    while True:
        try:
            data = recieveClient(SOCKET)
            print("recieve time: ", time())
            print("CLIENT DATA: ", data)
        except  BlockingIOError:
            print("Not recieved")
            print("OLD DATA:", data)

        sleep(3)



if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    path = os.getcwd()
    path = path+"/face_detector/"
    _consts.path.prototxtPath=path+"deploy.prototxt"
    _consts.path.maskNet = path + "mask_detector.model"
    _consts.path.weightsPath = path + "res10_300x300_ssd_iter_140000.caffemodel"

    _consts.pre.clientSocketS=client()
    #_consts.pre.clientSocketR = client()

    #vs, faceNet, maskNet =detection(_consts)

    #from sensor.DDSubsytem import DecisionDetection, DDLoop
    #DDTuple = DecisionDetection(_consts)
    Process(target=processB, args=(_consts.pre.clientSocketS,)).start()
    Process(target=processA, args=(_consts.pre.clientSocketS,)).start()
    '''
    while True:
        detectionLoop(vs, faceNet, maskNet, _consts.pre.clientSocketS)

        print("CLIENT DATA: ",recieveClient(_consts.pre.clientSocketS))
        #crowd = DDLoop(DDTuple, crowd, label)

        key = waitKey(1) & 0xFF
        if key == ord("q"):
            break
    destroyAllWindows()
    vs.stop()'''


#Process(target=, args=(_consts,)).start()