from forms import Addform, Delform, AddOwner
from flask import Flask, render_template,url_for,redirect
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
        return f'{self.name} is a new owner'
    
class Puppy(db.Model):
    
    __tablename__ = 'puppies'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref = 'puppy', uselist = False)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f'Puppy name is {self.name} and owner is {self.owner.name}'
        else:
            return f'Puppy name is {self.name} and id for adoption is {self.id}'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods = ['GET', 'POST'])
def add_puppy():
    
    form = Addform()
    
    if form.validate_on_submit():
        name = form.name.data
        new_puppy = Puppy(name)
        
        db.session.add(new_puppy)
        db.session.commit()
        
        return redirect(url_for('list_pup'))
    
    return render_template('add.html', form = form)

@app.route('/list')
def list_pup():
    
    puppies = Puppy.query.all()
    return render_template('list.html', puppies = puppies)

@app.route('/delete', methods = ['GET', 'POST'])
def del_puppy():
    
    form = Delform()
    
    if form.validate_on_submit():
        id = form.id.data
        puppy = Puppy.query.get(id)
        db.session.delete(puppy)
        db.session.commit()
        
        return redirect(url_for('list_pup'))
    
    return render_template('delete.html', form = form)

@app.route('/add_owner',methods = ['GET', 'POST'])
def add_owner():
    
    form = AddOwner()
    
    if form.validate_on_submit():
        
        name = form.name.data
        puppy_id = form.puppy_id.data
        
        new_owner = Owner(name, puppy_id)
        
        db.session.add(new_owner)
        db.session.commit()
        
        return redirect(url_for('list_pup'))
    
    return render_template('add_owner.html', form = form)

if __name__ == '__main__':
    app.run(debug = True)