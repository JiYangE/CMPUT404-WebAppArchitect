#!/user/bin/env python

import socket,os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(("0.0.0.0", 4321))

serverSocket.listen(5)

while True:
    (incomingSocket, address) = serverSocket.accept()
    childPid = os.fork()
    if (childPid != 0):
        # we must be still in the connection accepting process
        continue
        # we must be in a client talking process
    outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    outgoingSocket.connect(("www.google.com", 80))

    done = False
    while not done:
        incomingSocket.setblocking(0)
        try:
            part = incomingSocket.recv(2048)
        except IOError, exception:
            if exception.errno == 11:
                part = None
            else:
                raise
        if (part):
            outgoingSocket.sendall(part)
        '''else:
            done = True'''
        outgoingSocket.setblocking(0)
        try:
            part = outgoingSocket.recv(2048)
        except IOError, exception:
            if exception.errno == 11:
                part = None
            else:
                raise
        if (part):
            incomingSocket.sendall(part)