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
# Dane Agenta
host = fields[0]
port = int(fields[1])
# Dane Proxy
proxy_host = fields[2]
proxy_port = int(fields[3])

def status(val):
    c = lxc.Container(val)
    if c.defined:
        return 'ANS %s %s %s' % (val, c.state, host)
    else:
        return 'ANS %s %s %s' % (val, "UNKNOWN", host)

def create(val):
    c = lxc.Container(val)
    if not c.defined:
        c.create("download", 0, 
                {"dist": "ubuntu", 
                    "release": "trusty", 
                    "arch": "amd64"})
    return 'ANS %s %s %s' % (val, c.state, host)

def delete(val):
    c = lxc.Container(val)
    if c.defined:
        c.destroy()
    return 'ANS %s %s %s' % (val, c.state, host)

def stop(val):
    c = lxc.Container(val)
    if c.defined:
        os.system('lxc-stop -n %s' % val)
        return 'ANS %s %s %s' % (val, c.state, host)
    else:
        return 'ANS %s %s %s' % (val, "UNKNOWN", host)

def start(val):
    c = lxc.Container(val)
    if c.definded and c.state == "STOPPED":
        os.system('lxc-start -n %s' % val)
        return 'ANS %s %s %s' % (val, c.state, host)
    else:
        return 'ANS %s %s %s' % (val, "NOTEXIST", host)

def get_ip(val):
    c = lxc.Container(val)
    if c.defined and c.state == "RUNNING":
        return 'ANS %s %s %s' % (val, str(c.get_ips()[0]), host)
    else:
        return 'ANS %s %s %s' % (val, "NOTEXIST", host)

def install_ssh(val):
    c = lxc.Container(val)
    if c.defined and c.state == "RUNNING":
        c.attach_wait(lxc.attach_run_command,["apt-get", "install", "-y", "openssh-server"])
        return 'ANS %s %s %s' % (val, c.state, host)
    else:
        return 'ANS %s %s %s' % (val, "NOTEXIST", host)

def add_user(val):
    c = lxc.Container(val)
    if c.defined and c.state == "RUNNING":
        c.attach_wait(lxc.attach_run_command,["useradd", "test-user"])
        return 'ANS %s %s %s' % (val, c.state, host)
    else:
        return 'ANS %s %s %s' % (val, "NOTEXIST", host)


mgmt = {
    "STATUS": status,
    "CREATE": create,
    "START": start,
    "STOP": stop,
    "DELETE": delete,
    "GETIP": get_ip,
    "SSH": install_ssh,
    "USERADD": add_user

    }

def exec_m(command, arg):
    print ("Executing command: %s for container: %s" % (command, arg))
    return mgmt[command](arg)

def send_back(msg, addr = proxy_host, port = proxy_port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr, port))
    s.send(pickle.dumps([msg], 0)) 
    s.close()

# Przygotowanie socketa
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    recv = pickle.loads(c.recv(1024))
# pociecie stringu na slowa
    recv = recv[0].split()
    send_back(exec_m(recv[0], recv[1]))
    c.close()

