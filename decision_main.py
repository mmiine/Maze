
from networking.client import client, recieveClient, sendClient

from board import SCL, SDA
from busio import I2C
import RPi.GPIO as GPIO
from adafruit_mlx90614 import MLX90614
from time import time, sleep
import sys
from sensor.temperatureSensor import temperatureCalibration

def encodeSendData(SOCKET,crowd,state="a", temperature="none", maskwear="none"):
    data = state + "_" + str(crowd) + "_" + str(temperature) + "_" + maskwear
    sendClient(data, SOCKET)

def servoControl(angle, SERVOPIN1, pwm1):
    duty = angle / 18 + 3
    GPIO.output(SERVOPIN1, True)
    pwm1.ChangeDutyCycle(duty)
    
    sleep(1)
    GPIO.output(SERVOPIN1, False)
    
    #if(angle==45):
    pwm1.ChangeDutyCycle(0)
    


def controlSensor(_consts ):
    TRIGCHK = _consts.pin.TRIGCHK
    ECHOCHK = _consts.pin.ECHOCHK
    waitingTime = _consts.pre.waitingTime
    pulse_end= 0
    pulse_start =0
    counter=0
    print("Waiting of exiting in control sensor!")
    timing = time()
    while(time( ) -timing < waitingTime):
        # time.sleep(0.0001)
        GPIO.output(TRIGCHK, True)
        sleep(0.01)
        GPIO.output(TRIGCHK, False)
        a = time()
        while GPIO.input(ECHOCHK) == 0:
            pulse_start = time()
            if pulse_start - a > 0.005:
                break
        a = time()
        while GPIO.input(ECHOCHK) == 1:
            pulse_end = time()
            if pulse_end - a > 0.005:
                break
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)  # in cm
        
        # get distance temperature in celsius
        if (distance < 15 and distance > 1):
            counter=counter+1
            print(distance)
        if (counter>=3):
            print("Someone passed!")
            return True
    print("No one passed!")
    return False


def PeopleCounting(crowd,_consts, exit=0 ,enter=0):
    servoOpenAngle = _consts.pre.servoOpenAngle
    servoCloseAngle =_consts.pre.servoCloseAngle
    maxNum = _consts.pre.maxNum

    SERVOPIN1, pwm1 = _consts.pin.SERVO1, _consts.pin.PWM1
    

    sleepTime = 2

    isFull = True if crowd == maxNum else False
    isEmpty = True if crowd == 0 else False


    if (exit==1):
        if(isEmpty):
            print("BUILDING IS EMPTY!")
            sleep(sleepTime)
        else:
            print("EXITING PROCESSING")
            servoControl(servoOpenAngle,SERVOPIN1,pwm1)
            sleep(0.001)
            CONTROL = controlSensor(_consts)
            if CONTROL:
                crowd = crowd - 1
            sleep(1)
            servoControl(servoCloseAngle,SERVOPIN1,pwm1)
            print("EXITING FINISHED")


    elif (enter==1):
        if (isFull):
            print("BUILDING IS FULL!")
            sleep(sleepTime)

        else:
            print("ENTERING PROCESSING")
            servoControl(servoOpenAngle,SERVOPIN1,pwm1)
            CONTROL = controlSensor(_consts)
            if CONTROL:
                crowd = crowd + 1
            sleep(1)
            servoControl(servoCloseAngle,SERVOPIN1,pwm1)
            print("ENTERING FINISHED")
    return crowd





def DecisionDetection(_consts):
    #PIN ASSIGMENTS
    TRIGIN = _consts.pin.TRIGIN
    ECHOIN = _consts.pin.ECHOIN
    TRIGOUT = _consts.pin.TRIGOUT
    ECHOOUT = _consts.pin.ECHOOUT
    TRIGCHK = _consts.pin.TRIGCHK
    ECHOCHK = _consts.pin.ECHOCHK
    SERVO1 = _consts.pin.SERVO1
    

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


    GPIO.setup(TRIGIN, GPIO.OUT)
    GPIO.setup(ECHOIN, GPIO.IN)

    GPIO.setup(TRIGOUT, GPIO.OUT)
    GPIO.setup(ECHOOUT, GPIO.IN)

    GPIO.setup(TRIGCHK, GPIO.OUT)
    GPIO.setup(ECHOCHK, GPIO.IN)

    GPIO.setup(SERVO1, GPIO.OUT)
    pwm1 = GPIO.PWM(SERVO1, 50)
    pwm1.start(0)
    _consts.pin.PWM1=pwm1
    duty = 45 / 18 + 3
    GPIO.output(SERVO1, True)
    pwm1.ChangeDutyCycle(duty)

    # the mlx90614 must be run at 100k [normal speed]
    # i2c default mode is is 400k [full speed]
    # the mlx90614 will not appear at the default 400k speed
    i2c = I2C(SCL, SDA, frequency=100000)
    mlx = MLX90614(i2c)

    GPIO.output(TRIGIN, False)
    sleep(0.02)

    DDTuple = (TRIGIN, TRIGOUT, ECHOIN, ECHOOUT, mlx, _consts )
    return DDTuple

def DDLoop(DDTuple,crowd,maskpos,SOCKET):
    state = 'a'
    pulse_start = 0
    pulse_end = 0
    TRIGIN, TRIGOUT,ECHOIN,ECHOOUT,mlx,_consts = DDTuple
    sleep(0.0001)
    print("PEOPLE INSIDE BUILDING = ", str(crowd), "\nWAITING MODE")
    ## EXITING DISTANCE SENSOR
    GPIO.output(TRIGOUT, True)
    sleep(0.0001)
    GPIO.output(TRIGOUT, False)
    a = time()
    while GPIO.input(ECHOOUT) == 0:
        pulse_start = time()
        if pulse_start - a > 0.005:
            break
    a = time()
    while GPIO.input(ECHOOUT) == 1:
        pulse_end = time()
        if pulse_end - a > 0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # in cm
    
    # EXITING DISTANCE SENSOR and DISTANCE CONTROL
    if ((distance > 1) and (distance < 6)):
        GPIO.output(TRIGOUT, True)
        sleep(0.0001)
        GPIO.output(TRIGOUT, False)
        a = time()
        while GPIO.input(ECHOOUT) == 0:
            pulse_start = time()
            if pulse_start - a > 0.005:
                break
        a = time()
        while GPIO.input(ECHOOUT) == 1:
            pulse_end = time()
            if pulse_end - a > 0.005:
                break
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)  # in cm
        
        if ((distance > 1) and (distance < 6)):
            encodeSendData(SOCKET, crowd, "c")
            crowd = PeopleCounting(crowd, _consts, exit=1, enter=0)
    sleep(0.0001)

    ## ENTERING DISTANCE SENSOR
    sleep(0.001)
    GPIO.output(TRIGIN, True)
    sleep(0.0001)
    GPIO.output(TRIGIN, False)
    a = time()
    while GPIO.input(ECHOIN) == 0:
        pulse_start = time()
        if pulse_start - a > 0.005:
            break
    a = time()
    while GPIO.input(ECHOIN) == 1:
        pulse_end = time()
        if pulse_end - a > 0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # in cm
    temp = "None"
    print(distance)
    if(distance> 6):
        encodeSendData(SOCKET, crowd,"a", maskpos)
    if ((distance < 6) and (distance > 4.5)):
        # get object temperature in celsius
        temp = temperatureCalibration(distance,mlx.object_temperature)
        print("\nMeasured temperature: {:.1f}".format(temp), " from distance: {:.1f}".format(distance), " in ", maskpos, "maskwear")
        encodeSendData(SOCKET, crowd,"b", temp, maskpos)
        if temp < 35:
            print("\nInvalid temperature!\n")
        elif temp < 37.5:
            if maskpos == "Proper Mask":
                crowd = PeopleCounting(crowd, _consts, exit=0, enter=1)
        else:
            print("\nYour temperature is too high. Please go to a medical center!\n")
        sleep(1)
    return data,crowd

if __name__ == '__main__':
    sys.path.append(".")
    from main import _consts
    DDTuple = DecisionDetection(_consts)
    data='a_none_none_none'
    label = "None"
    crowd = 0
    SOCKET = client()
    while True:
        try:
            label = recieveClient(SOCKET)
            print("CLIENT DATA RECIEVED: ", label)
        except  BlockingIOError:
            print("NOT RECIEVED OLD DATA: ", label)
        sendClient(data, SOCKET)
        data,crowd = DDLoop(DDTuple, crowd, label,SOCKET)
        sendClient(data, SOCKET)

