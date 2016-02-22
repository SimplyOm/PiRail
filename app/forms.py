from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    pnr = StringField('pnr', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    food = StringField('food')
    sanitation=StringField('sanitation')
    journey=StringField('radio_journey')
    feedback=TextAreaField('feedback')

class PNREntry(Form):
    pnr = StringField('pnr', validators=[DataRequired()])

    

