#!/usr/bin/python3
import socket
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy import Integer, Column, update, insert, String
from sqlalchemy.ext.declarative import declarative_base

# Import vars from file
file = open('proxy.cfg')
for line in file:
    fields = line.strip().split()

host = fields[0]
port = int(fields[1])

# Przygotowanie db
engine = create_engine('mysql://pz:pass@localhost:3306/lxc', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Przygotowanie socketa
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

# Strutkura tabeli
Base = declarative_base()
class Table(Base):
        __tablename__ = 'containers'

        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        status = Column(String(100))
        cnt_ip = Column(String(20))
        agnt_ip = Column(String(20))

        def __init__(self, name, status, cnt_ip, agnt_ip):
                self.name = name
                self.status = status
                self.cnt_ip = cnt_ip
                self.agnt_ip = agnt_ip

        def __repr__(self):
                return "<Table(%s, %s)>" % (self.name, self.status, self.cnt_ip, self.agnt_ip)

# Przekazanie komunikatu do Agenta
def forward_msg(msg, addr='localhost', port=5050):
    print("Forwarding message: %s for container: %s to Agent IP: %s" % (msg.split()[0], msg.split()[1], addr))
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr, port))
    s.send(pickle.dumps([msg], 0))
    s.close()

# Update bazy danych
def update_db(cmd, name, field, agnt_ip):
    if "ANSC" in cmd:
        rec = Table(name=name, status=field, cnt_ip="0.0.0.0", agnt_ip=agnt_ip)
        session.add(rec)
    if "ANSD" in cmd:
        rec = session.query(Table).filter_by(name=name)
        for r in rec:
            session.delete(r)
    elif "." not in field:
        session.query(Table).filter_by(name=name).update({"status": field, "agnt_ip": agnt_ip})
    else:
        session.query(Table).filter_by(name=name).update({"cnt_ip": field, "agnt_ip": agnt_ip})
    session.commit()

while True:
    c, addr = s.accept()
    recv = pickle.loads(c.recv(1024))
    print ("RAW MSG: %s" % recv)
    if not "ANS" in recv[0].split()[0]:
        forward_msg(recv, '192.168.56.10', port=5050)
    else:
        recv = recv[0].split()
        print("Making Query on DB for container: %s" % recv[1])
        update_db(recv[0], recv[1], recv[2], recv[3] )
    c.close()
