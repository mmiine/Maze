import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

TRIG1 = 16
ECHO1 = 26

LEDG = 5
LEDR = 6

counter = 0
print("HC-SR04 mesafe sensoru")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)

GPIO.setup(LEDG,GPIO.OUT)
GPIO.setup(LEDR,GPIO.OUT)



while True:

    GPIO.output(TRIG, False)
    time.sleep(0.00001)
    #print("olculuyor")
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > 1 and distance < 8:
        #print ("Counted in:",distance - 0.5,"cm")
        counter = (counter + 1)
        if counter<101:
            print("People inside building: ",counter)
            GPIO.output(LEDG, True)
            time.sleep(2)
            GPIO.output(LEDG, False)
        else:
            print("Building is full!")
            counter = 100
        
        
        
    #else:
        #print("No one entered:",distance - 0.5,"cm")
    
    
    GPIO.output(TRIG1, False)
    time.sleep(0.00001)
    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)

    while GPIO.input(ECHO1)==0:
        pulse_start = time.time()


    while GPIO.input(ECHO1)==1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > 1 and distance < 8:
        #print ("Counted out:",distance - 0.5,"cm")
        counter = (counter - 1)
        if (counter<0): counter=0
        print("People inside building: ",counter)
        GPIO.output(LEDR, True)
        time.sleep(2)
        GPIO.output(LEDR, False)
        
