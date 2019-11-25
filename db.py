from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///demo.db')
Base = declarative_base()


class Noun(Base):
    __tablename__ = 'nouns'
    Id = Column(Integer, primary_key=True)
    Word = Column(String)
    Type = Column(String)
    TypeAlt = Column(String)


class Verb(Base):
    __tablename__ = 'verbs'
    Id = Column(Integer, primary_key=True)
    Word = Column(String)
    NounType = Column(String)
    NounTypeAlt = Column(String)
    CaseObj = Column(String)
    Aspc = Column(String)   


class Predlog(Base):
    __tablename__ = 'predlogs'
    Id = Column(Integer, primary_key=True)
    Word = Column(String)
    NounType = Column(String)
    NounCase = Column(String)


class Beginning(Base):
    __tablename__ = 'beginnings'
    Id = Column(Integer, primary_key=True)
    Word = Column(String)
    CommaAfter = Column(Boolean)
    Tense = Column(Integer)

  
class Ending(Base):
    __tablename__ = 'endings'
    Id = Column(Integer, primary_key=True)
    Word = Column(String)
    CommaAfter = Column(Boolean)
    Tense = Column(Integer)