#!/user/bin/env python


import socket, os, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

<<<<<<< HEAD:Lab2/serversocket.py
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
=======
serverSocket.bind(("0.0.0.0", 12346))

serverSocket.listen(5)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>>>>>>> c4f9de3a6ced90c1261a3f898b316518d2f1d0d6:Lab2/serverdemo.py

while True:
	(incomingSocket, address) = serverSocket.accept()	
	childPid = os.fork()
	if (childPid != 0):
		# we must be still in the connection accepting process
		continue
	# we must be in a client talking process
	outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	outgoingSocket.connect(("www.google.com", 443))
	done = False
	while not done:
		# fix cpu use with poll() or select()
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
		select.select(
			[incomingSocket, outgoingSocket],
			[],
			[incomingSocket, 	outgoingSocket],
			1.0)
