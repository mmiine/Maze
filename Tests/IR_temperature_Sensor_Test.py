import random
import xlsxwriter
from time import sleep, time
import sys
from board import SCL, SDA
from busio import I2C
import RPi.GPIO as GPIO
from adafruit_mlx90614 import MLX90614
import keyboard 

def temperatureCalibration(x,y):
    """
    x: distance
    y: measured temperature
    """
    if(y<28 or y>35):
        return y
    if(x>7):
        return y
    p00 = 195.4
    p10 = -12.7
    p01 = -15.83
    p20 = 0.07593
    p11 = 0.8362
    p02 = 0.4491
    p21 = -0.002277
    p12 = -0.01361
    p03 = -0.004415
    val = p00 + p10 * x + p01 * y + p20 * x ** 2 + p11 * x * y + p02 * y ** 2 + p21 * x ** 2 * y+ p12 * x * y ** 2 + p03 * y ** 3

    return val + y

def distanceMeasurement(TRIG, ECHO):
    pulse_end=pulse_start=0

    sleep(0.001)
    GPIO.output(TRIG, True)
    sleep(0.0001)
    GPIO.output(TRIG, False)
    a = time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time()
        if pulse_start - a > 0.005:
            break
    a = time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time()
        if pulse_end - a > 0.005:
            break
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # in cm
    return distance


TRIG =23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

i2c = I2C(SCL, SDA, frequency=100000)
mlx = MLX90614(i2c)

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Tests.xlsx')
worksheet = workbook.add_worksheet('IRTest')


# Some data we want to write to the worksheet.

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

worksheet.write(row, 1, 'Real Body')
worksheet.write(row, 1, 'Distance')
worksheet.write(row, 2, 'Measured Temperature')
worksheet.write(row, 3, 'Fitted Temperature')

row = row+1

realBody = float(input("Enter real measured body temperature: "))
inp = 0
# Iterate over the data and write it out row by row.
while True:
    try:
        #realBody = float(input("Enter real measured body temperature: "))
        inp = input("Enter real measured body temperature: ")
        if(type(inp)==float):
           realBody=inp
        else:
            if inp == 'q':
                break
            else:
                print("measuring")
                sleep(0.1)
                distance=distanceMeasurement(TRIG, ECHO)
                measured=  mlx.object_temperature           
                temperature = temperatureCalibration(distance,  measured)
                print("Distance: ", distance)
                print("Measured Temp: ", measured)
                print("Fitted Temp: ", temperature)
                worksheet.write(row, 0, realBody)
                worksheet.write(row, 1, distance)
                worksheet.write(row, 2, measured)
                worksheet.write(row, 3, temperature)
                row += 1
                sleep(0.2)
    except ValueError:
        print("exiting")
        break

workbook.close()