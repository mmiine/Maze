import socket
from _thread import *


_connections = []

def threaded_client(i,_connections):
    connection = _connections[i]
    while True:

        data = connection.recv(1024)
        print('From client '+str(i)+': ' + str(data))
        if not data:
            break
        try:
            _connections[(i+1)%3].send(data)
        except IndexError:
            print("Next client couldn't found")

    connection.close()

def server():
    host = 'localhost'  # get local machine name
    port = 8083  # Make sure it's within the > 1024 $$ <65535 range
    ThreadCount = 0

    s = socket.socket()
    s.bind((host, port))
    print("Server is ready to connect.")
    s.listen(3)

    while True:
        Client, address = s.accept()
        _connections.append(Client)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (ThreadCount,_connections,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    s.close()

if __name__ == '__main__':
    server()


