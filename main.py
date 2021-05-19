
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

    class path:
        '''
        Paths
        '''
        maskNet = r"face_detector/mask_detector.model"
        prototxtPath = r"face_detector/deploy.prototxt"
        weightsPath = r"face_detector/res10_300x300_ssd_iter_140000.caffemodel"









'''
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
'''