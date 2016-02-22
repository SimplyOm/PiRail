from flask import render_template, flash, redirect,session,request
from app import app, db, models
from .forms import LoginForm,PNREntry,ImmediateForm
from .models import User,Chart
#import RPi.GPIO as GPIO
import requests
import json
import time
#import serial
import urllib2

'''
ser1 = serial.Serial(port = '/dev/ttyUSB0',baudrate = 9600, parity = serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
ser2 = serial.Serial(port = '/dev/ttyACM0',baudrate = 115200, parity = serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)


GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.LOW)
'''

state=0
railway_api_key='opyoo5828'

north=25.2624715
east=82.983633
location='Semi Cir Rd Number 5, Banaras Hindu University Campus,Varanasi, Uttar Pradesh 221005, India'
speed=0
humidity=0
temperature=0
ac=0

food,medicine,secu,clean=[[],[],[],[]]

@app.route('/controlroom')
def controlroom():
    return render_template('controlroom.html',title='ControlRoom')


@app.route('/updatestats')
def updatestats():
     global ser1,ser2,north,east,location,speed,humidity,temperature,ac
     '''
     string = ser1.readline()
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
     except Exception as e:
        print e
     
     string=ser2.readline()
     print string
     if string[0:2]=='OK':
          string=ser2.readline()
          print string
          string=string.split(',')
          humidity=float(string[0])
          print humidity
          temperature=float(string[1])
          ac=int(string[2])
     '''
     st='Your latitude and longitude are '+str(north)+' N '+str(east)+' E.<br>Your current detected location is '+location+'.<br> We are currently travelling at '+str(speed)+'m/s .<br> The current temperature is '+str(temperature)+' degree C.<br> The current humidity is '+str(humidity)+'.<br>The AC is set to '+str(ac)+'.'
     return st

@app.route('/trial')
def trial():
    global temp
    return str(temp)

@app.route('/senddatacontrol')
def senddatacontrol():
    global food,secu,medicine,clean
    strmain=''
    strmain+='<B><I>Food Orders:</I></B><br>'
    strmain+=''.join(food)
    strmain+='<br><br><br><br>'
    strmain+='<B><I>Medical Emergencies:</I></B><br>'
    strmain+=''.join(medicine)
    strmain+='<br><br><br><br>'
    strmain+='<B><I>Security Issues:</I></B><br>'
    strmain+=''.join(secu)
    strmain+='<br><br><br><br>'
    strmain+='<B><I>Sanitatory Problems:</I></B><br>'
    strmain+=''.join(clean)
    strmain+='<br><br><br><br>'
    return strmain
    
@app.route('/immediate', methods=['GET', 'POST'])
def immediate():
    if 'pnr' in session:
      login=True
    else:
      login=False
    form=ImmediateForm()
    global food,secu,medicine,clean
    if form.validate_on_submit():
      pnr=form.pnr.data
      print 'pnr = '+pnr
      users=models.Chart.query.all()
      flag=0
      for u in users:
          if pnr==str(u.pnr):
              seat=u.seat
              name=u.name
              flag=1
              break
      print flag
      if flag:    
          flash('Your query has been processed. Please wait while the appropriate action is being taken.')
          if form.typ.data=='Food':
              st=name+' bearing PNR no. '+pnr+' occupying seat no '+str(seat)+' has ordered food. <br> Furthur information: '+form.query.data+'<br><br>'
              food.append(st)
          if form.typ.data=='Medical':
              st=name+' bearing PNR no. '+pnr+' occupying seat no '+str(seat)+' requires medical attention. <br> Furthur information: '+form.query.data+'<br><br>'
              medicine.append(st)
          if form.typ.data=='Cleanliness':
              st=name+' bearing PNR no. '+pnr+' occupying seat no '+str(seat)+' has complaints regarding cleanliness. <br> Furthur information: '+form.query.data+'<br><br>'
              clean.append(st)
          if form.typ.data=='Security':
              st=name+' bearing PNR no. '+pnr+' occupying seat no '+str(seat)+' is having security issues. <br> Furthur information: '+form.query.data+'<br><br>'
              secu.append(st)
      else:
          flash('Please provide a valid PNR number!')
          return redirect('/immediate')
    return render_template('immediate.html',title='Immediate',form=form,login=login)

@app.route('/trainstats')
def trainstats():
    return render_template('trainstats.html',title='Train Statistics');

@app.route('/')
@app.route('/index')
def index():
    if 'pnr' in session:
      login=True
    else:
      login=False
    return render_template('index.html',title='WELCOME TO INDIAN RAILWAYS',login=login)

@app.route('/login',methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    try:
      pnr=request.form["pnr"]
    except:
      return render_template('index.html',title='WELCOME',login=False,login_error_message='No pnr entered')    
    try:  
      password=request.form['password']
    except:
      return render_template('index.html',title='WELCOME',login=False,login_error_message='No password entered')
    if len(pnr)==10:
      passengers=models.Chart.query.all()
      print passengers
      found=False
      for p in passengers:
        try:
          print int(pnr)
          if p.pnr==int(pnr):
            found=True
            break
        except:
          return render_template('index.html',title='WELCOME',login=False,login_error_message='characters not allowed in pnr')
      if found:
        if password==p.password:
          session['pnr'] = pnr
          return render_template('index.html',title='WELCOME',login=True)
        else:
          return render_template('index.html',title='WELCOME',login=False,login_error_message='Wrong password provided')          
      else:
        return render_template('index.html',title='WELCOME',login=False,login_error_message='You are in the wrong tarin')
    else:
      return render_template('index.html',title='WELCOME',login=False,login_error_message='Invalid Pnr')
  else:  
    return render_template('index.html',title='WELCOME',login=False)

@app.route('/logout')
def logout():
  if 'pnr' in session:
    session.clear()
  return render_template('index.html',title='WELCOME TO INDIAN RAILWAYS',login=False)


@app.route('/feedback', methods=['GET', 'POST'])
def feedpnrentry():
   if 'pnr' in session:
      login=True
   else:
      login=False
   form=PNREntry()
   if form.validate_on_submit():
      pnr=form.pnr.data
      users=models.Chart.query.all()
      flag=0
      for u in users:
          if pnr==str(u.pnr):
              flag=1
              break
      if flag:    
          return redirect('/feedback/'+pnr)
      else:
          flash('Please provide a valid PNR number!')
          return redirect('/feedback')
   return render_template('pnrentry.html',title='FEEDBACK',form=form,heading="Feedback",login=login)



@app.route('/feedback/<pnr>', methods=['GET', 'POST'])
def feedback(pnr):
    if 'pnr' in session:
      login=True
    else:
      login=False
    form = LoginForm()
    users=models.Chart.query.all()
    name=''
    for u in users:
        if pnr==str(u.pnr):
              name=u.name
              break
    if form.validate_on_submit():
        flash('Thank You %s for your valuable feedback' %
              (name))
        user = User(pnr=pnr, name=name, food=form.food.data,sanitation=form.sanitation.data,journey=form.journey.data,feedback=form.feedback.data)
	db.session.add(user)
	db.session.commit()
        return redirect('/index')
    return render_template('feedback.html',title='FEEDBACK',name=name,form=form,pnr=pnr,login=login)

def add_zero(x):
   if x>=10:
      return str(x)
   else:
      return '0'+str(x)

@app.route('/myyatrainfo/',methods=['GET', 'POST'])
def pnrentry():
   if 'pnr' in session:
      login=True
   else:
      login=False
   form=PNREntry()
   if form.validate_on_submit():
      pnr=form.pnr.data
      return redirect('/myyatrainfo/'+pnr)
   return render_template('pnrentry.html',title='MyYatraInfo',form=form,heading="MyYatraInfo",login=login)

   
@app.route('/myyatrainfo/<pnr>', methods=['GET'])
def myinfo(pnr):
   if 'pnr' in session:
      login=True
   else:
      login=False
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
          except Exception as e:
             print e
             return render_template('myyatrainfoerrnonet.html',title='MyYatraInfo',login=login)
   except Exception as e:
       print e
       return render_template('myyatrainfoerrnonet.html',title='MyYatraInfo',login=login)
   print response_dict
   return render_template('myyatrainfo.html',title='MyYatraInfo',values=response_dict,login=login)


