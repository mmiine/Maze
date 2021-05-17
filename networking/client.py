import socket

def sendClient(result, socket):
    socket.send(result.encode('utf-8'))

def recieveClient(socket):
    result = socket.recv(1024).decode('utf-8')
    return result

def client():
    host = 'localhost'  # get local machine name
    port = 8083  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()

    s.connect((host, port))
    s.setblocking(False)
    return s


if __name__ == '__main__':
    client()