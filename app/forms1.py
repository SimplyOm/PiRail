from flask.ext.wtf import Form
from wtforms import StringField,TextAreaField, BooleanField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    pnr = StringField('pnr', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    radio_food = RadioField('radio_food', choices=[('excellent','excellent'),('good','good'),('poor','poor')])
    radio_sanitation=RadioField('radio_sanitation', choices=[('excellent,excellent'),('good','good'),('poor','poor')])
    radio_journey=RadioField('radio_journey',choices=[('pleasant','pleasant'),('satisfactory','satisfactory'),('unsatisfactory','unsatisfactory')])
    feedback=TextAreaField('feedback')

