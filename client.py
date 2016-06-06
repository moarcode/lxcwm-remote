#!/usr/bin/python           
import socket               # Import socket module
import pickle

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
dic={"Hostname": "test.com", "IP": "192.168.1.1."}

s.connect((host, port))
#s.send(dic)
s.send((pickle.dumps(dic)))
print s.recv(1024)
s.close                     # Close the socket when done