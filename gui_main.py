import sys
from time import sleep
from guizero import App, Text
import random
from networking.client import client, recieveClient, sendClient

temperature="none"
mask_position="none"
crowd = "none"
# 
# def update_temp(temperature):
#     temp.value = str(temperature)  #received data
#     # recursive call
#     temp.after(100, update_temp(temperature))
# 
# 
# def update_population(crowd):
#     pop.value = str(crowd)
#     pop.after(100, update_population(crowd))
# 
# 
# def update_mask(mask_position):
#     maske.value = str(mask_position)
#     maske.after(100, update_mask(mask_position))


if __name__ == '__main__':
        
#     app = App(title="Maze-Surveillance", width=720, height=480, layout="grid")  #lcd size ???
#     message = Text(app, text="Entrance allowed", size=25, font="Times New Roman", color="black", grid=[2, 0], align="left")
# 
#     mask = Text(app, text="Proper mask :", size=25, font="Times New Roman", color="black", grid=[2, 1], align="left")
#     maske = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 1])
#     maske.after(100, update_mask(mask_position))
# 
#     Temperature = Text(app, text="Temperature :", size=25, font="Times New Roman", color="black", grid=[2, 2], align="left")
#     temp = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 2])
#     temp.after(100, update_temp(temperature))
#     Population = Text(app, text="Population :", size=25, font="Times New Roman", color="black", grid=[2, 3], align="left")
#     pop = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 3])
#     pop.after(100, update_population(crowd))
# 
#     app.display()
    sys.path.append(".")
    from main import _consts
    data = "none_none_none"
    SOCKET = client()
    while True:
        try:
            data = recieveClient(SOCKET)
            print("CLIENT DATA RECIEVED: ", data)
        except  BlockingIOError:
            print("NOT RECIEVED OLD DATA: ", data)
            data = str(data)
            if(data==None):
                pass
            x = data.split("_")
            crowd = x[0]
            temperature = x[1]
            mask_position = x[2]
            print("pop: ",crowd," temp: ",temperature," mask: ",mask_position)
             
'''
Do GUI things        
'''

