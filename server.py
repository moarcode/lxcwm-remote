#!/usr/bin/python       

import socket               # Import socket module
import pickle
import os, sys

s = socket.socket()         # Create a socket object
host = 'localhost' # Get local machine name
port = 5050                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   #print c.recv(1024)
   dic = pickle.loads(c.recv(1024))
   print dic
   c.send('100')
   c.close()                # Close the connection

