from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.traversals import COMPARE_FAILED
from dataclasses import dataclass


Base = automap_base()

@dataclass
class User(Base):
    __tablename__ = 'user'

    id: int
    username: str
    password: str

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String)
    password = Column('password', String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@dataclass
class Player(Base):
    __tablename__ = 'player'

    id: int
    name: str
    surname: str
    age: int
    nationality: str
    club: str

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    age = Column('age', Integer)
    nationality = Column('nationality', String)
    club = Column('club', String)

    def __init__(self, name, surname, age, nationality, club):
        self.name = name
        self.surname = surname
        self.age = age
        self.nationality = nationality
        self.club = club

