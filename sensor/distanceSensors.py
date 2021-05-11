from time import time, sleep
import RPi.GPIO as GPIO

def servoControl(angle,SERVOPIN,pwm):
    duty = angle / 18 + 3
    GPIO.output(SERVOPIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVOPIN, False)


def controlSensor(TRIGCHK, ECHOCHK):

    pulse_end= 0
    pulse_start =0

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
            CONTROL = controlSensor()
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
            CONTROL = controlSensor()
            if CONTROL:
                crowd = crowd + 1
            sleep(1)
            servoControl(servoCloseAngle,SERVOPIN,pwm)
            print("ENTERING FINISHED")
    return crowd