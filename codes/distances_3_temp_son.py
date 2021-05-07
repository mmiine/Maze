#https://circuitpython.readthedocs.io/projects/mlx90614/en/latest/
import busio as io
import board
import time
import adafruit_mlx90614
import RPi.GPIO as GPIO

maxNum = 6
waitingTime = 5 # in seconds

servoOpenAngle = 90
servoCloseAngle = 0

def servoControl(angle):
    duty = angle / 18 + 3
    GPIO.output(SERVO1, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO1, False)
    
    
def controlSensor():

    pulse_end= 0
    pulse_start=0
    
    print("Waiting of exiting in control sensor!")
    timing = time.time()
    while(time.time()-timing < waitingTime):
        #time.sleep(0.0001)
        GPIO.output(TRIGCHK, True)
        time.sleep(0.01)
        GPIO.output(TRIGCHK, False)
        a = time.time()
        while GPIO.input(ECHOCHK) == 0:
            pulse_start = time.time()
            if pulse_start - a > 0.005:
                break
        a = time.time()
        while GPIO.input(ECHOCHK) == 1:
            pulse_end = time.time()
            if pulse_end - a > 0.005:
                break
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)  # in cm
     
        # get distance temperature in celsius
        if (distance < 10 and distance > 1):
            print("Someone passed!")
            return True
    print("No one passed!")
    return False

def PeopleCounting(crowd, exit=0,enter=0):
    sleepTime = 2

    isFull = True if crowd == maxNum else False
    isEmpty = True if crowd == 0 else False


    if (exit==1):
        if(isEmpty):
            print("BUILDING IS EMPTY!")
            time.sleep(sleepTime)
        else:
            print("EXITING PROCESSING")
            servoControl(servoOpenAngle)
            time.sleep(0.001)
            CONTROL = controlSensor()
            if CONTROL:
                crowd = crowd - 1
            time.sleep(1)
            servoControl(servoCloseAngle)
            print("EXITING FINISHED")


    elif (enter==1):
        if (isFull):
            print("BUILDING IS FULL!")
            time.sleep(sleepTime)

        else:
            print("ENTERING PROCESSING")
            servoControl(servoOpenAngle)
            CONTROL = controlSensor()
            if CONTROL:
                crowd = crowd + 1
            time.sleep(1)
            servoControl(servoCloseAngle)
            print("ENTERING FINISHED")
    return crowd


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIGIN = 23
ECHOIN = 24

GPIO.setup(TRIGIN, GPIO.OUT)
GPIO.setup(ECHOIN, GPIO.IN)

TRIGOUT =21
ECHOOUT =20

GPIO.setup(TRIGOUT, GPIO.OUT)
GPIO.setup(ECHOOUT, GPIO.IN)

TRIGCHK =6
ECHOCHK =5

GPIO.setup(TRIGCHK, GPIO.OUT)
GPIO.setup(ECHOCHK, GPIO.IN)

SERVO1 = 17

GPIO.setup(SERVO1, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)

# the mlx90614 must be run at 100k [normal speed]
# i2c default mode is is 400k [full speed]
# the mlx90614 will not appear at the default 400k speed
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)




GPIO.output(TRIGIN, False)
time.sleep(0.02)
a=0
crowd = 0
while True:
    print("PEOPLE INSIDE BUILDING = ", str(crowd),"\nWAITING MODE" )
    ## OUT DISTANCE SENSOR
    GPIO.output(TRIGOUT, True)
    time.sleep(0.0001)
    GPIO.output(TRIGOUT, False)
    a = time.time()
    while GPIO.input(ECHOOUT) == 0:
        pulse_start = time.time()
        if pulse_start - a > 0.005:
            break
    a = time.time()
    while GPIO.input(ECHOOUT) == 1:
        pulse_end = time.time()
        if pulse_end - a > 0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # in cm
    
    # get object temperature in celsius
    if (distance < 6):
        crowd=PeopleCounting(crowd,exit=1, enter=0)
    time.sleep(0.0001)

    ## INPUT DISTANCE SENSOR
    time.sleep(0.001)
    GPIO.output(TRIGIN, True)
    time.sleep(0.0001)
    GPIO.output(TRIGIN, False)
    a=time.time()
    while GPIO.input(ECHOIN)==0:
        pulse_start = time.time()
        if pulse_start-a >0.005:
            break
    a=time.time()
    while GPIO.input(ECHOIN)==1:
        pulse_end = time.time()
        if pulse_end-a >0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    distance = round(distance, 2) #in cm
    # get object temperature in celsius
    if(distance < 6):
        temp = mlx.object_temperature+3.5
        print("\nMeasured temperature: {:.1f}".format(temp), " distance: {:.1f}".format(distance),"\n")
        
        if temp<30:
            print("\nInvalid temperature!\n")
        elif temp<37.5:
            crowd=PeopleCounting(crowd,exit=0, enter=1)
        else:
            print("\nYour temperature is too high. Please go to a medical center!\n")

    time.sleep(0.2)