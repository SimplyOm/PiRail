from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    food = StringField('food')
    sanitation=StringField('sanitation')
    journey=StringField('radio_journey')
    feedback=TextAreaField('feedback')

class PNREntry(Form):
    pnr = StringField('pnr', validators=[DataRequired()])

class ImmediateForm(Form):
    typ = RadioField ('typ', choices=[('Food','Food'),('Medical','Medical'),('Cleanliness','Cleanliness'),('Security','Security')], validators=[DataRequired()])
    query= TextAreaField('feedback', validators=[DataRequired()])
