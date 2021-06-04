import random
import xlsxwriter
import keyboard
from time import sleep, time
import sys
from board import SCL, SDA
from busio import I2C
import RPi.GPIO as GPIO
from adafruit_mlx90614 import MLX90614


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


sys.path.append(".")
from main import _consts

TRIG = _consts.pin.TRIGIN
ECHO = _consts.pin.ECHOIN

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

worksheet.write(row, 0, 'Real Body Temperature')
worksheet.write(row, 1, 'Distance')
worksheet.write(row, 2, 'Measured Temperature')
worksheet.write(row, 3, 'Real Object Temperature')

row = row+1


# Iterate over the data and write it out row by row.
while True:
    try:
        realBody = float(input("Enter real measured object temperature: "))
        realObject = float(input("Enter real measured object temperature: "))
        print("measuring")
        for _ in range(3):
            distance=distanceMeasurement(TRIG, ECHO)
            temperature = mlx.object_temperature
            worksheet.write(row, 0, realBody)
            worksheet.write(row, 1, distance)
            worksheet.write(row, 2, temperature)
            worksheet.write(row, 3, realObject)
            row += 1
        sleep(0.5)
    except ValueError:
        print("exiting")
        break

workbook.close()