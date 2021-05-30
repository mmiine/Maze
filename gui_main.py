import sys
from time import sleep
from guizero import App, Text
import random
from networking.client import client, recieveClient, sendClient

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

    if state == 'a':
        message.value = "Waiting"
    else:
        message.value = ("pop ={} temp ={} mask{}".format(crowd,temperature,mask_position))

    

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

