import sys
from time import sleep
from os import listdir, path
from guizero import App, Text, Picture
from networking.client import client, recieveClient, sendClient

sys.path.append(".")
from main import _consts

state = "none"
temperature = "none"
mask_position = "none"

SOCKET = client()
UPDATE_FREQUENCY = 100  # time in milliseconds (ms)
data = "none_none_none_none"

pathh = "images"
image_paths=[]
for img in listdir(pathh):
    img_path = path.join(pathh, img)
    image_paths.append(img_path)

print(image_paths)
def recieve_data():
    try:
        data = recieveClient(SOCKET)
        print("CLIENT DATA RECIEVED: ", data)  # received data
    except  BlockingIOError:
        print("NOT RECIEVED RETURNING")
        return
    x = data.split("_")
    state = x[0]
    crowd = x[1]
    temperature = x[2]
    mask_position = x[3]

    print("state: ", state, "pop: ", crowd, " temp: ", temperature, " mask: ", mask_position)
    if (crowd == "none"):
        return
    crowd = int(crowd)
    if (crowd >= _consts.pre.maxNum):
        message.text_color = "blue"
        message.value = "Building has reached population limit\nPopulation inside building: {}".format(crowd)
        picpath = 7
    elif state == 'a':  # waiting state
        message.text_color = "blue"
        message.value = "Please bring your hand over to the sensor\nPopulation inside building: {}".format(crowd)
        picpath = 6

    elif (state == 'b'):  # entering process started
        crowd = int(crowd)
        temperature = float(temperature)
        temperature = temperature

        if crowd < _consts.pre.maxNum and temperature > 35 and temperature < 37.5 and mask_position == "Proper Mask":
            message.text_color = "green"
            message.value = "Enterance Allowed\nYour temperature is {:.1f} celcius degrees".format(temperature)
            picpath = 0

        elif temperature > 37.5 and mask_position == "Proper Mask":
            picpath = 1
            message.text_color = "red"
            message.value = "Your temperature is too high!\nYour temperature is {:.1f} celcius degrees".format(
                temperature)

        elif temperature > 37.5 and mask_position == "Improper Mask":
            picpath = 3
            message.text_color = "red"
            message.value = "You are not wearing your face mask properly!\nYour temperature is too high!\nYour temperature is {:.1f} celcius degrees".format(
                temperature)

        elif temperature > 37.5 and mask_position == "Non Mask":
            picpath = 5
            message.text_color = "red"
            message.value = "You are not wearing your face mask!\nYour temperature is too high!\nYour temperature is {:.1f} celcius degrees".format(
                temperature)

        elif temperature < 37.5 and temperature > 35 and mask_position == "Improper Mask":
            picpath = 2
            message.text_color = "red"
            message.value = "You are not wearing your face mask properly!\nYour temperature is {:.1f} celcius degrees".format(
                temperature)

        elif temperature < 37.5 and temperature > 35 and mask_position == "Non Mask":
            picpath = 4
            message.text_color = "red"
            message.value = "You are not wearing your face mask!\nYour temperature is {:.1f} celcius degrees".format(
                temperature)

        elif temperature < 35:
            picpath = 8
            message.text_color = "red"
            message.value = "Invalid temperature! \nYour temperature is {:.1f} celcius degrees".format(temperature)

    elif state == 'c':  # exiting process started
        message.text_color = "blue"
        message.value = "Exit process is started"
    else:
        picpath = 6
        message.text_color = "blue"
        message.value = "Please bring your hand over to the sensor\nPopulation inside building: {}".format(crowd)
    # message.value = ("Population inside building: {} \n temp ={} mask ={}".format(crowd,temperature,mask_position))

    picture.value = image_paths[picpath]


if __name__ == '__main__':

    app = App(title="Maze-Surveillance", width=720, height=480, bg='white')  # lcd size ???
    picture = Picture(app, image=image_paths[0])
    message = Text(app, "xx", size=25, font="Times New Roman", color="black", grid=[2, 0])

    # mask = Text(app, text="Proper mask :", size=25, font="Times New Roman", color="black", grid=[2, 1], align="left")
    # maske = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 1])

    # Temperature = Text(app, text="Temperature :", size=25, font="Times New Roman", color="black", grid=[2, 2], align="left")
    # temp = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 2])

    # Population = Text(app, text="Population :", size=25, font="Times New Roman", color="black", grid=[2, 3], align="left")
    # pop = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 3])

    app.repeat(UPDATE_FREQUENCY, recieve_data)

    try:
        app.full_screen = 1
        app.display()
    except KeyboardInterrupt:
        exit()