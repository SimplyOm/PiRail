from flask import render_template, flash, redirect
from app import app, db
from .forms import LoginForm,PNREntry
from .models import User
import RPi.GPIO as GPIO
import requests
import json
import time
import serial
import urllib2
'''
ser = serial.Serial(port = '/dev/ttyUSB0',baudrate = 9600, parity = serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
GPIO.setmode(GPIO.BCM)
state=0
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.LOW)
'''
railway_api_key='opyoo5828'

north=25.2624715
east=82.983633
location='IIT-BHU'
speed=0

@app.route('/trial')
def trial():
    return 'Done'

@app.route('/a')
def a():
    values={'aa':'Not Done'}
    return render_template('a.html',title='A',values=values)

@app.route('/trainstats')
def trainstats():
    global ser,north,east,location,speed
    string = ser.readline()
    if (string):
       print string
       if(string[0:6]=='$GPRMC'):
          string=string.split(',')
          if(string[3]!=''):
             north=float(string[3])/100
             east=float(string[5])/100
             speed=float(string[7])
    try:
    	data = urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/xml?latlng='+str(north)+','+str(east)+'&sensor=true')
    	l = []
    	for line in data.readlines():
        	l.append(line)
        location= l[5][21:-21]
    except:
        flash('Could not refresh data')
    return render_template('trainstats.html',title='Train Statistics',north=north,east=east,location=location,speed=speed);

@app.route('/control')
def control():
   global state
   if(state==0):
      cur_state='off'
      change_state='on'
   else:
      cur_state='on'
      change_state='off'
   return render_template('control.html',title='Controls',cur_state=cur_state,change_state=change_state)

@app.route('/control1')
def control1():
   global state
   if(state==0):
      GPIO.output(23,GPIO.HIGH)
      cur_state='on'
      change_state='off'
      state=1
   else:
      GPIO.output(23,GPIO.LOW)
      cur_state='off'
      change_state='on'
      state=0
   return render_template('control.html',title='Controls',cur_state=cur_state,change_state=change_state)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='WELCOME TO INDIAN RAILWAYS')


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
    return render_template('feedback.html',title='FEEDBACK',form=form)

def add_zero(x):
   if x>=10:
      return str(x)
   else:
      return '0'+str(x)

@app.route('/myyatrainfo/',methods=['GET', 'POST'])
def pnrentry():
   form=PNREntry()
   if form.validate_on_submit():
      pnr=form.pnr.data
      return redirect('/myyatrainfo/'+pnr)
   return render_template('pnrentry.html',title='MyYatraInfo',form=form)

   
@app.route('/myyatrainfo/<pnr>', methods=['GET'])
def myinfo(pnr):
   response_dict={}
   true,false=[True,False]
   try:
       pnr_res_ob=requests.get('http://api.railwayapi.com/pnr_status/pnr/'+pnr+'/apikey/'+railway_api_key)
       if pnr_res_ob.status_code==requests.codes.ok:
          pnr_res_json=pnr_res_ob.json()
          if pnr_res_json['error']:
             return render_template('myyatrainfoerror.html',title='MyYatraInfo')
          train_date=pnr_res_json['train_start_date']
          train_num=pnr_res_json['train_num']
          response_dict['pnr_info']=pnr_res_json
          doj=str(train_date['year'])+add_zero(train_date['month'])+add_zero(train_date['day'])
          try:
             live_ob=requests.get('http://api.railwayapi.com/live/train/'+train_num+'/doj/'+doj+'/apikey/'+railway_api_key)
             if live_ob.status_code==requests.codes.ok:
                live_json=live_ob.json()
                response_dict['live']=live_json
                if live_json['position'].startswith('Train has reached Destination'):
                   ended=1
                else:
                   ended=0
                response_dict['ended']=ended
                if live_json['position'].startswith('Train is currently at Source'):
                   started=0
                else:
                   started=1
                response_dict['started']=started
                tot=len(live_json['route'])
                last=tot
                for route in live_json['route']:
                   if route['no']==1:
                      response_dict['source']=route
                      print "source "+route['station']
                   if route['station']==origin:
                      response_dict['origin']=route
                      print "origin "+route['station']
                      print route['no']
                   if route['station']==dest:
                      response_dict['dest']=route
                      print "dest "+route['station']
                      print route['no']
                   if route['no']==tot:
                      response_dict['end']=route
                      print "end "+route['station']
                   if started and not ended:
                      if route['has_departed']:
                         for r in live_json['route']:
                            if not r['has_departed'] and r['no']==route['no']+1:
                               if route['no']<last:
                                  last=route['no']
                                  response_dict['last']=route
                for route in live_json['route']:
                   if route['no']==last+1:
                      response_dict['next']=route
          except requests.exceptions.RequestException as e:
             print e
   except requests.exceptions.RequestException as e:
       print e
   return render_template('myyatrainfo.html',title='MyYatraInfo',values=response_dict)


