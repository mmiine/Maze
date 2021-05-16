import sys
from guizero import App, Text
app: App = App(title="Hello world",)

from time import sleep
from networking.client import client, recieveClient, sendClient


if __name__ == '__main__':
    sys.path.append(".")
    from main import _consts
    data = None
    SOCKET = client()
    while True:
        try:
            data = recieveClient(SOCKET)
            print("CLIENT DATA RECIEVED: ", data)
        except  BlockingIOError:
            print("NOT RECIEVED OLD DATA: ", data)

        data = str(data)
        x = data.split("_")
        crowd = x[0]
        temperature = x[1]
        mask_position = x[2]
        '''
        
        Do GUI things
        
        '''



        app.full_screen = 1
        app.display()
        sleep(0.01)
