from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Base

app = Flask(__name__)
app.secret_key = 'dc37f6323031813c4eef29bb3f346ee0'
app.testing = True

ENV = 'dev'
LOGIN = False
USER = ''

engine = create_engine('postgresql://postgres:0000@localhost/Players')

Base.prepare(engine, reflect=True)

session = Session(engine)