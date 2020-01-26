from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import os

Base = declarative_base()
engine = create_engine(os.environ[' '])
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    tense = Column(String)
    gender = Column(String)


if not engine.dialect.has_table(engine, 'users'):
    Base.metadata.create_all(engine)


def create_new_user(session, username):
    if not session.query(User).filter(User.username == username).first():
        user = User(username=username)
        session.add(user)
        session.commit()


def check_if_user_exists(session, username):
    if not session.query(User).filter(User.username == username).first():
        return False
    return True
