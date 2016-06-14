#!/usr/bin/python3
import socket
import pickle

# MSG
# Command LXC-Name

def forward_msg(msg, addr='localhost', port=5050):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr, port))
    s.send(pickle.dumps([msg, name], 0))
    if recv == '100':
        print("Recived OK")
    else:
        print("Did not recived OK")
    s.close()



class Cnt(object):
    def __init__(self, name, status="UNKNOWN", host="localhost"):
        self.host = host
        self.name = name
        self.status = status
    def send(self, name, msg="STATUS", host='localhost', port=5050):
        self.host = host
        self.msg = msg
        self.port = port
# przygotowanie socketa
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.host, port))
        s.send(pickle.dumps([msg, name], 0))
        recv = s.recv(1024).decode("utf-8") 
        if recv == '100':
            print("Recived OK")
        else:
            print("Did not recived OK")
        s.close()


c = Cnt("TEST")
print (c.host)
print (c.name)
print (c.status)
c.send("TEST")
c.send("TEST", msg="START")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = 'localhost'
port = 5050
s.bind(host, port)
s.listen(5)
while True:
    c, addr = s.accept()
    recv = pickle.loads(c.recv(1024))
    
