#!/usr/bin/python3
import lxc
import socket
import pickle
import os

# MSG
# Command LXC-Name

# Import vars from file
file = open('agent.cfg')
for line in file:
    fields = line.strip().split()

host = fields[0]
port = int(fields[1])
proxy_host = fields[2]
proxy_port = int(fields[3])

def forward_msg(msg, addr='localhost', port=5050):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr[0], port))
    s.send(pickle.dumps([msg], 0))
    s.close()

def status(val):
    c = lxc.Container(val)
    return c.state

def create():
    print ("create")

def delete(val):
    print ("delete")

def stop(val):
    os.system('lxc-stop -n %s' % val)
    #c = lxc.Container(val)
    #c.stop
    #print("Container stopped. Status: %s" % c.state)

def start():
    pass
    #c = lxc.Container()
    #c.start()
    #print("Container started. Status: %s" % c.state)

mgmt = {
    "STATUS": status,
    "CREATE": create,
    "START": start,
    "STOP": stop,
    "DELETE": delete

    }

def exec_m(command, arg):
    return mgmt[command](arg)

def exec_msg(msg):
    msg = msg[0].split()
    mgmt = {
            "STATUS": status,
            "CREATE": create,
            "START": start,
            "STOP": stop(msg[1]),
            "DELETE": delete("TEST")

            }
    func = mgmt.get(msg[0], lambda: "nothing")
    return func

def send_back(addr, port, msg):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr, port))
    s.send(pickle.dumps([msg], 0)) 
    s.close()


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    recv = pickle.loads(c.recv(1024))
    c.send('100'.encode())
    print (recv)
#    exec_msg(recv)
    z = exec_m(recv[0], recv[1])
    send_back(proxy_host, proxy_port, "ANS RUNNING nazwa IP")
    c.close()

