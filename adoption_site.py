from forms import Addform, Delform
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


class Puppy(db.Model):
    
    __tablename__ = 'puppies'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f'Puppy name is {self.name}'


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

if __name__ == '__main__':
    app.run(debug = True)