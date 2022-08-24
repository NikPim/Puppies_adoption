from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from training_settings import postgresql as settings

user,password,host,port,database = settings.values()

uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'
app = Flask(__name__)

app.config["SECRET_KEY"] = 'Nikita123'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):
    
    __tablename__ = 'puppies'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref = 'puppy', uselist = False)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f'Puppy name is {self.name} and owner is {self.owner[0].name}'
        else:
            return f'Puppy name is {self.name}'