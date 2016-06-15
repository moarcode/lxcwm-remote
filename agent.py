#!/usr/bin/python3
import socket
import pickle

# MSG
# Command LXC-Name

# Import vars from file
file = open('agent.cfg')
for line in file:
    fields = line.strip().split()

host = fields[0]
port = int(fields[1])

def forward_msg(msg, addr='localhost', port=5050):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr[0], port))
    s.send(pickle.dumps([msg], 0))
    s.close()

def status(val):
    print ('status %s' % val)

def create():
    print ("create")

def delete():
    print ("delete")

def stop():
    print ("stop")

def start():
    print ("start")

def exec_msg(msg):
    msg = msg[0].split()
    mgmt = {
            "STATUS": status(msg[1]),
            "CREATE": create,
            "START": start,
            "STOP": stop,
            "DELETE": delete

            }
    func = mgmt.get(msg[0], lambda: "nothing")
    return func

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    recv = pickle.loads(c.recv(1024))
    c.send('100'.encode())
    print (recv)
    exec_msg(recv)
    c.close()

