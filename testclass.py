#!/usr/bin/python3


class Cnt(object):
    def __init__(self, name, status="UNKNOWN", host="localhost"):
        self.host = host
        self.name = name
        self.status = status
    def send(self, name, msg="STATUS", host="localhost"):
        self.msg = msg
        # send via socket
        # send('%s:%s' % msg, name)
        print('%s' % msg, name)

c = Cnt("TEST")

print (c.host)
print (c.name)
print (c.status)
c.send("TEST")
