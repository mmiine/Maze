from guizero import App, Text
app: App = App(title="Hello world",)
#https://circuitpython.readthedocs.io/projects/mlx90614/en/latest/

    
import busio as io
import board
import time
import adafruit_mlx90614
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# the mlx90614 must be run at 100k [normal speed]
# i2c default mode is is 400k [full speed]
# the mlx90614 will not appear at the default 400k speed
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

GPIO.output(TRIG, False)
time.sleep(0.02)
a=0

def update_label():
    text.value = read_sensor()
    # recursive call
    text.after(1000, update_label)






while True:
   
    print("olcuyor")
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    a=time.time()
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        if pulse_start-a >0.005:
            break
    a=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        if pulse_end-a >0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    distance = round(distance, 2) #in cm
    # get object temperature in celsius
    if(distance<20):
        print("in")
        temp= mlx.object_temperature
        print("temperature: ",str(temp)," distance: ", str(distance))
        
        entrance_denied_ = Text(app, text="Body Temperature = {:.1f}".format(temp), size=98, font="Times New Roman", color="red",)
        text.value = read_sensor()
        # recursive call
        text.after(1000, update_label)
    app.full_screen=1
    app.display()
    time.sleep(0.01)
