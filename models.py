"""
Database for Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import datetime

import config


DeclarativeBase = declarative_base()

def now():
    print "Using now func"
    return datetime.datetime.now()

def db_connect():
    return create_engine(URL(**config.DATABASE))

def create_checks_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class Check(DeclarativeBase):
    __tablename__ = "checks"
    checkid = Column('checkid', Integer, Sequence('checkid_seq'), primary_key=True, index=True)
    url = Column('url', String, unique=True, index=True)
    last_status = Column('last_status', Integer)
    content_type = Column('content_type', String)
    last_request = Column('last_request', DateTime(timezone=True), default=now)
    is_up = Column('is_up', Boolean, default=True)
    is_muted = Column('is_muted', Boolean, default=False)

engine = db_connect()
create_checks_table(engine)
