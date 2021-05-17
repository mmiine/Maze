
from networking.client import client, recieveClient, sendClient

from board import SCL, SDA
from busio import I2C
import RPi.GPIO as GPIO
from adafruit_mlx90614 import MLX90614
from time import time, sleep
import sys
from sensor.temperatureSensor import temperatureCalibration


def servoControl(angle, SERVOPIN, pwm):
    duty = angle / 18 + 3
    GPIO.output(SERVOPIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(SERVOPIN, False)
    #if(angle==45):
    pwm.ChangeDutyCycle(0)


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
        if (distance < 10 and distance > 1):
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

    SERVOPIN, pwm = _consts.pin.SERVO1, _consts.pin.PWM1
    sleepTime = 2

    isFull = True if crowd == maxNum else False
    isEmpty = True if crowd == 0 else False


    if (exit==1):
        if(isEmpty):
            print("BUILDING IS EMPTY!")
            sleep(sleepTime)
        else:
            print("EXITING PROCESSING")
            servoControl(servoOpenAngle,SERVOPIN,pwm)
            sleep(0.001)
            CONTROL = controlSensor(_consts)
            if CONTROL:
                crowd = crowd - 1
            sleep(1)
            servoControl(servoCloseAngle,SERVOPIN,pwm)
            print("EXITING FINISHED")


    elif (enter==1):
        if (isFull):
            print("BUILDING IS FULL!")
            sleep(sleepTime)

        else:
            print("ENTERING PROCESSING")
            servoControl(servoOpenAngle,SERVOPIN,pwm)
            CONTROL = controlSensor(_consts)
            if CONTROL:
                crowd = crowd + 1
            sleep(1)
            servoControl(servoCloseAngle,SERVOPIN,pwm)
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


    # the mlx90614 must be run at 100k [normal speed]
    # i2c default mode is is 400k [full speed]
    # the mlx90614 will not appear at the default 400k speed
    i2c = I2C(SCL, SDA, frequency=100000)
    mlx = MLX90614(i2c)

    GPIO.output(TRIGIN, False)
    sleep(0.02)

    DDTuple = (TRIGIN, TRIGOUT, ECHOIN, ECHOOUT, mlx, _consts )
    return DDTuple

def DDLoop(DDTuple,crowd,maskpos):
    pulse_start = 0
    pulse_end = 0
    TRIGIN, TRIGOUT,ECHOIN,ECHOOUT,mlx,_consts = DDTuple
    sleep(0.0001)
    print("PEOPLE INSIDE BUILDING = ", str(crowd), "\nWAITING MODE")
    ## OUT DISTANCE SENSOR
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
    
    # get object temperature in celsius
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
            crowd = PeopleCounting(crowd, _consts, exit=1, enter=0)
    sleep(0.0001)

    ## INPUT DISTANCE SENSOR
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
    # get object temperature in celsius
    temp = None
    try:
        maskpos = maskpos[0:11]
    except:
        maskpos = maskpos
    if (distance < 6):
        temp = temperatureCalibration(mlx.object_temperature)
        print("\nMeasured temperature: {:.1f}".format(temp), " from distance: {:.1f}".format(distance), "\n")
        print("Maskwear is ", maskpos)
        if temp < 30:
            print("\nInvalid temperature!\n")
        elif temp < 37.5:
            if maskpos == "Proper Mask":
                crowd = PeopleCounting(crowd, _consts, exit=0, enter=1)
        else:
            print("\nYour temperature is too high. Please go to a medical center!\n")
    if temp == None: temp="None"
    if maskpos == None: maskpos="None"
    data = str(crowd) + "_"+str(temp)+"_"+maskpos
    return data,crowd

if __name__ == '__main__':
    sys.path.append(".")
    from main import _consts
    DDTuple = DecisionDetection(_consts)

    label = None
    crowd = 0
    SOCKET = client()
    while True:
        try:
            label = recieveClient(SOCKET)
            print("CLIENT DATA RECIEVED: ", label)
        except  BlockingIOError:
            print("NOT RECIEVED OLD DATA: ", label)
        data,crowd = DDLoop(DDTuple, crowd, label)
        sendClient(data, SOCKET)

