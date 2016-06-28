from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy import Integer, Column, update, insert, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://pz:pass@localhost:3306/lxc', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

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
#new_record = Table('test', "RUNNING", "1.1.1.1", "2.2.2.2")
#session.add(new_record)
#z = update(Table).where(Table.id=="test").values(status="STOPPED")
#z.compile(dialect=mysql.dialect(), compile_kwargs=  {"literal_binds": True})
#session.execute(z)

session.query(Table).filter_by(name="test").update({"status": u"STOPPED"})
session.commit()



