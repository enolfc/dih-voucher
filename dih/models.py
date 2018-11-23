import json

import dateutil.parser
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, reconstructor

import requests

from dih.database import Base

# voucher_time = timedelta(hours=2)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    epuid = Column(String(256), unique=True)
    email = Column(String(120))
    name = Column(String(256))

    def __init__(self, epuid=None, email=None, name=None):
        self.epuid = epuid 
        self.email = email
        self.name = name 
        self.init_on_load()

    @reconstructor
    def init_on_load(self):
        self.valid_through = None 
        self.status = ''

    def __repr__(self):
        return '<User %r>' % (self.epuid)


class VO(Base):
    __tablename__ = 'vos'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    used = Column(Boolean)

    def __init__(self, name=None, used=False):
        self.name = name
        self.used = used 

    def __repr__(self):
        return '<VO %r>' % (self.name)
