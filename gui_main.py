import sys
from time import sleep
from guizero import App, Text
import random
from networking.client import client, recieveClient, sendClient


def update_temp():
    temp.value = str(random.randint(20, 60))  #received data
    # recursive call
    temp.after(100, update_temp)


def update_population():
    pop.value = str(random.randint(20, 60))
    pop.after(100, update_population)


def update_mask():
    maske.value = str(random.randint(20, 60))
    maske.after(100, update_mask)


if __name__ == '__main__':
    # sys.path.append(".")
    # from main import _consts
    # data = None
    # SOCKET = client()
    # while True:
    #     try:
    #         data = recieveClient(SOCKET)
    #         print("CLIENT DATA RECIEVED: ", data)
    #     except  BlockingIOError:
    #         print("NOT RECIEVED OLD DATA: ", data)
    #
    #     data = str(data)
    #     x = data.split("_")
    #     crowd = x[0]
    #     temperature = x[1]
    #     mask_position = x[2]
        '''        
        Do GUI things        
        '''

app = App(title="Maze-Surveillance", width=720, height=480, layout="grid")  #lcd size ???
message = Text(app, text="Entrance allowed", size=25, font="Times New Roman", color="black", grid=[2, 0], align="left")

mask = Text(app, text="Proper mask :", size=25, font="Times New Roman", color="black", grid=[2, 1], align="left")
maske = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 1])
maske.after(100, update_mask)

Temperature = Text(app, text="Temperature :", size=25, font="Times New Roman", color="black", grid=[2, 2], align="left")
temp = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 2])
temp.after(100, update_temp)
Population = Text(app, text="Population :", size=25, font="Times New Roman", color="black", grid=[2, 3], align="left")
pop = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 3])
pop.after(100, update_population)

app.display()
