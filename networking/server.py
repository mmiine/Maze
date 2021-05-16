import socket
from _thread import *
import queue

Q = []

_connections = []

def threaded_client(i,_connections):
    connection = _connections[i]
    while True:

        data = connection.recv(1024)
        Q[i].put(data)
        print('From client '+str(i)+': ' + str(data))
        if not data:
            break
        try:
            _connections[(i+1)%3].send(Q[i].get())
            with Q[i].mutex:
                Q[i].queue.clear()
        except IndexError:
            print("Next client couldn't found")

    connection.close()

def server():
    host = 'localhost'  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range
    ThreadCount = 0

    s = socket.socket()
    s.bind((host, port))
    print("Server is ready to connect.")
    s.listen(3)

    while True:
        Client, address = s.accept()
        _connections.append(Client)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        Q.append(queue.LifoQueue())
        start_new_thread(threaded_client, (ThreadCount,_connections,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    s.close()

if __name__ == '__main__':
    server()


