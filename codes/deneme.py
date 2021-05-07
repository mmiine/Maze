import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 18
GPIO.setup(TRIG,GPIO.OUT)
print("basladı")
GPIO.output(TRIG, True)
time.sleep(3)
#print("olculuyor")
GPIO.output(TRIG,False )
print("bitti")