import sys
from time import sleep
from guizero import App, Text
import random
from networking.client import client, recieveClient, sendClient

sys.path.append(".")
from main import _consts
state="none"
temperature="none"
mask_position="none"
crowd = "none"
SOCKET = client()
UPDATE_FREQUENCY = 100 #time in milliseconds (ms)
data="none_none_none_none"

def recieve_data():
    try:
        data = recieveClient(SOCKET)
        print("CLIENT DATA RECIEVED: ", data) #received data
    except  BlockingIOError:
        print("NOT RECIEVED RETURNING")
        return
    if(data==None):
        data="none_none_none_none"
    x = data.split("_")
    state = x[0]
    crowd = x[1]
    temperature = x[2]
    try:
        temperature=float(temperature)
        temperature="{:.1f}".format(temperature)
        temperature=str(temperature)
    except:
        temperature=temperature
    mask_position = x[3]
    print("state: ",state,"pop: ",crowd," temp: ",temperature," mask: ",mask_position)
    
    #temp.value = temperature
    #pop.value = crowd
    #maske.value = mask_position
    #st.value = state
    try:
        crowd = int(crowd)
        temperature = float(temperature)
        if state == 'a': #waiting state
            message.value = "Please bring your hand over to the sensor\nPopulation inside building: {}".format(crowd)
        elif state == 'b': #entering process started
            if crowd < _consts.pre.maxNum and temperature<37.5 and mask_position=="Proper Mask":
                message.value = "Enterance Allowed\nYour temperature is {} celcius degrees".format(temperature)
            elif crowd>=_consts.pre.maxNum:
                message.value = "Population limit has been reached"
            elif temperature>37.5:
                message.value = "Your temperature is too high. Please go to a medical center!\nYour temperature is {} celcius degrees".format(temperature)
            elif temperature<34:
                message.value = "Invaild temperature"
            elif mask_position=="Improper Mask" or mask_position=="Non Mask":
                message.value = "Your mask wear is not proper!"


        elif state == 'c': #exiting process started
            message.value = "Exit process is started"
    except:
        message.value = "Please bring your hand over to the sensor\nPopulation inside building: {}".format(crowd)
    #message.value = ("Population inside building: {} \n temp ={} mask ={}".format(crowd,temperature,mask_position))

    

if __name__ == '__main__':

    app = App(title="Maze-Surveillance", width=720, height=480, layout="grid")  #lcd size ???

    message = Text(app,"xx", size=25, font="Times New Roman", color="black", grid=[2, 0], align="left")


    #mask = Text(app, text="Proper mask :", size=25, font="Times New Roman", color="black", grid=[2, 1], align="left")
    #maske = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 1])


    #Temperature = Text(app, text="Temperature :", size=25, font="Times New Roman", color="black", grid=[2, 2], align="left")
    #temp = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 2])

    #Population = Text(app, text="Population :", size=25, font="Times New Roman", color="black", grid=[2, 3], align="left")
    #pop = Text(app, "xx", size=25, font="Times New Roman", grid=[3, 3])
    
    app.repeat(UPDATE_FREQUENCY, recieve_data)

    try:
        app.display()
    except KeyboardInterrupt:
        SOCKET.close()
        exit()
        
    

        
             
'''
Do GUI things     asdasd
'''

