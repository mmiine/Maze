import RPi.GPIO as GPIO
from time import sleep

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwm=GPIO.PWM(12, 50)
pwm.start(0)

while True:
    print("in")
    SetAngle(90)
    sleep(0)
    SetAngle(45)


