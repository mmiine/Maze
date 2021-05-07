

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DIGITOUT=19
DIGITIN =13
GPIO.setup(DIGITOUT,GPIO.OUT)
GPIO.setup(DIGITIN,GPIO.IN)
a=0
b=0
c=0
while True:
     GPIO.output(DIGITOUT, True)
     a=GPIO.input(DIGITIN)
     print(a)
#     while False:
#         print("olcum")
#         a=GPIO.input(DIGITIN)
#         print(a)
#         time.sleep(0.0001) 
#         
#     print("olcum")
#     a=GPIO.input(DIGITIN)       
#     GPIO.output(DIGITOUT, False)    
#     time.sleep(0.0005)  
#     b=GPIO.input(DIGITIN)        
#     print(a)       
#     print(b)        
#     print(c)
#  
# 