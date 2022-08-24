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

class Owner(db.Model):
    
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))
    
    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id
        
    def __repr__(self):
        return f'{self.name} name is now owner of the puppy with id {self.puppy_id}'