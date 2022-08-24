from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class Addform(FlaskForm):
    
    name = StringField('Name of puppy: ')
    submit = SubmitField('Add Puppy')
    
class Delform(FlaskForm):
    
    id = IntegerField('Id number of puppy to remove: ')
    submit = SubmitField('Remove Puppy')
    
    