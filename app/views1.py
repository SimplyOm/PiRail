from flask import render_template, flash, redirect
from app import app, db
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='WELCOME TO INDIAN RAILWAYS')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Thank You %s for your valuable feedback' %
              (form.name.data))
        user = User(pnr=form.pnr.data, name=form.name.data, food=form.food.data,sanitation=form.sanitation.data,journey=form.journey.data,feedback=form.feedback.data)
	db.session.add(user)
	db.session.commit()
        return redirect('/index')
    return render_template('feedback.html',
                           title='FEEDBACK',
                           form=form)

