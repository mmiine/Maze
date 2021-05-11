from board import SCL, SDA
from busio import I2C
import RPi.GPIO as GPIO
from adafruit_mlx90614 import MLX90614
from time import time, sleep

from distanceSensors import PeopleCounting
from temperatureSensor import temperatureCalibration


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
    a = 0
    crowd = 0
    while True:
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
        if (distance < 6):
            crowd = PeopleCounting(crowd,_consts, exit=1, enter=0)
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
        if (distance < 6):
            temp = temperatureCalibration(mlx.object_temperature)
            print("\nMeasured temperature: {:.1f}".format(temp), " distance: {:.1f}".format(distance), "\n")

            if temp < 30:
                print("\nInvalid temperature!\n")
            elif temp < 37.5:
                crowd = PeopleCounting(crowd,_consts, exit=0, enter=1)
            else:
                print("\nYour temperature is too high. Please go to a medical center!\n")

        sleep(0.2)