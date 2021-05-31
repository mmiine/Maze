from networking.client import sendClient, client
from time import sleep
import random
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
        SERVO1 = 12
        PWM1 = None
        

    class pre:
        '''
        Predetermined Constants
        '''
        maxNum = 7
        waitingTime = 5 # in seconds

        servoOpenAngle = 0
        servoCloseAngle = 45

    class path:
        '''
        Paths
        '''
        maskNet = r"face_detector/mask_detector.model"
        prototxtPath = r"face_detector/deploy.prototxt"
        weightsPath = r"face_detector/res10_300x300_ssd_iter_140000.caffemodel"







if __name__ == '__main__':
    try:
        SOCKET = client()
    except ConnectionRefusedError:
        print("[INFO] No server is found!")
        SOCKET = None
    crowd = "none"
    temp = "none"
    maskpos = "none"
    while True:
        state = 'a'
        temp = "none"
        maskpos = "none"
        data = state+ "_" + str(crowd) + "_" + str(temp) + "_" + maskpos
        print(data)
        sendClient(data, SOCKET)
        sleep(1)
        state = 'b'
        crowd = random.randint(0,10)
        temp = random.randrange(36,42)
        maskpos= random.choice(["Proper Mask","Improper Mask","Non Mask"])
        data = state+ "_" +str(crowd) + "_" + str(temp) + "_" + maskpos
        sendClient(data, SOCKET)
        print(data)
        sleep(2)

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