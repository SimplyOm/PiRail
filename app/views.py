from flask import render_template, flash, redirect,session,request
from app import app, db, models
from .forms import LoginForm,PNREntry,ImmediateForm
from .models import User,Chart
from collections import deque
import RPi.GPIO as GPIO
import requests
import json
import time
import serial
import urllib2

'''
ser1 = serial.Serial(port = '/dev/ttyUSB0',baudrate = 9600, parity = serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
ser2 = serial.Serial(port = '/dev/ttyACM0',baudrate = 115200, parity = serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
'''

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.output(2,GPIO.LOW)
GPIO.setup(3,GPIO.OUT)
GPIO.output(3,GPIO.LOW)

state=0
railway_api_key='opyoo5828'

north=25.2624715
east=82.983633
location='Semi Cir Rd Number 5, Banaras Hindu University Campus,Varanasi, Uttar Pradesh 221005, India'
speed=0
humidity=0
temperature=0
ac=0

true=True
false=False
dic=[{},{"actdep": "10:30", "station": "DDN", "status": "0 mins late", "has_departed": true, "schdep": "10:30", "has_arrived": false, "day": 0, "actarr": "00:00", "distance": 0, "actarr_date": "29 Feb 2016", "station_": {"code": "DDN", "name": "DEHRADUN"}, "no": 1, "scharr": "Source", "scharr_date": "29 Feb 2016", "latemin": 0}, {"actdep": "11:39", "station": "DWO", "status": "36 mins late", "has_departed": true, "schdep": "11:03", "has_arrived": true, "day": 0, "actarr": "11:37", "distance": 19, "actarr_date": "29 Feb 2016", "station_": {"code": "DWO", "name": "DOIWALA"}, "no": 2, "scharr": "11:01", "scharr_date": "29 Feb 2016", "latemin": 36}, {"actdep": "12:10", "station": "RWL", "status": "33 mins late", "has_departed": true, "schdep": "11:37", "has_arrived": true, "day": 0, "actarr": "12:08", "distance": 40, "actarr_date": "29 Feb 2016", "station_": {"code": "RWL", "name": "RAIWALA"}, "no": 3, "scharr": "11:35", "scharr_date": "29 Feb 2016", "latemin": 33}, {"actdep": "12:21", "station": "MOTC", "status": "30 mins late", "has_departed": true, "schdep": "11:51", "has_arrived": true, "day": 0, "actarr": "12:19", "distance": 47, "actarr_date": "29 Feb 2016", "station_": {"code": "MOTC", "name": "MOTICHUR"}, "no": 4, "scharr": "11:49", "scharr_date": "29 Feb 2016", "latemin": 30}, {"actdep": "12:55", "station": "HW", "status": "15 mins late", "has_departed": true, "schdep": "12:45", "has_arrived": true, "day": 0, "actarr": "12:30", "distance": 51, "actarr_date": "29 Feb 2016", "station_": {"code": "HW", "name": "HARIDWAR JN"}, "no": 5, "scharr": "12:15", "scharr_date": "29 Feb 2016", "latemin": 15}, {"actdep": "13:03", "station": "JWP", "status": "11 mins late", "has_departed": true, "schdep": "12:52", "has_arrived": true, "day": 0, "actarr": "13:01", "distance": 55, "actarr_date": "29 Feb 2016", "station_": {"code": "JWP", "name": "JWALAPUR"}, "no": 6, "scharr": "12:50", "scharr_date": "29 Feb 2016", "latemin": 11}, {"actdep": "14:30", "station": "LRJ", "status": "15 mins late", "has_departed": true, "schdep": "14:25", "has_arrived": true, "day": 0, "actarr": "14:15", "distance": 78, "actarr_date": "29 Feb 2016", "station_": {"code": "LRJ", "name": "LAKSAR JN"}, "no": 7, "scharr": "14:00", "scharr_date": "29 Feb 2016", "latemin": 15}, {"actdep": "14:52", "station": "RK", "status": "5 mins late", "has_departed": true, "schdep": "14:50", "has_arrived": true, "day": 0, "actarr": "14:50", "distance": 97, "actarr_date": "29 Feb 2016", "station_": {"code": "RK", "name": "ROORKEE"}, "no": 8, "scharr": "14:45", "scharr_date": "29 Feb 2016", "latemin": 5}, {"actdep": "16:05", "station": "SRE", "status": "14 mins late", "has_departed": true, "schdep": "16:05", "has_arrived": true, "day": 0, "actarr": "15:49", "distance": 131, "actarr_date": "29 Feb 2016", "station_": {"code": "SRE", "name": "SAHARANPUR"}, "no": 9, "scharr": "15:35", "scharr_date": "29 Feb 2016", "latemin": 14}, {"actdep": "17:32", "station": "DBD", "status": "44 mins late", "has_departed": true, "schdep": "16:48", "has_arrived": true, "day": 0, "actarr": "17:30", "distance": 166, "actarr_date": "29 Feb 2016", "station_": {"code": "DBD", "name": "DEOBAND"}, "no": 10, "scharr": "16:46", "scharr_date": "29 Feb 2016", "latemin": 44}, {"actdep": "18:29", "station": "MOZ", "status": "71 mins late", "has_departed": true, "schdep": "17:17", "has_arrived": true, "day": 0, "actarr": "18:27", "distance": 190, "actarr_date": "29 Feb 2016", "station_": {"code": "MOZ", "name": "MUZAFFARNAGAR"}, "no": 11, "scharr": "17:16", "scharr_date": "29 Feb 2016", "latemin": 71}, {"actdep": "19:05", "station": "KAT", "status": "78 mins late", "has_departed": true, "schdep": "17:47", "has_arrived": true, "day": 0, "actarr": "19:03", "distance": 212, "actarr_date": "29 Feb 2016", "station_": {"code": "KAT", "name": "KHATAULI"}, "no": 12, "scharr": "17:45", "scharr_date": "29 Feb 2016", "latemin": 78}, {"actdep": "19:34", "station": "MUT", "status": "83 mins late", "has_departed": true, "schdep": "18:11", "has_arrived": true, "day": 0, "actarr": "19:32", "distance": 241, "actarr_date": "29 Feb 2016", "station_": {"code": "MUT", "name": "MEERUT CANT"}, "no": 13, "scharr": "18:09", "scharr_date": "29 Feb 2016", "latemin": 83}, {"actdep": "20:05", "station": "MTC", "status": "83 mins late", "has_departed": true, "schdep": "19:10", "has_arrived": true, "day": 0, "actarr": "19:48", "distance": 245, "actarr_date": "29 Feb 2016", "station_": {"code": "MTC", "name": "MEERUT CITY"}, "no": 14, "scharr": "18:25", "scharr_date": "29 Feb 2016", "latemin": 83}, {"actdep": "20:25", "station": "MDNR", "status": "57 mins late", "has_departed": true, "schdep": "19:28", "has_arrived": true, "day": 0, "actarr": "20:23", "distance": 265, "actarr_date": "29 Feb 2016", "station_": {"code": "MDNR", "name": "MODINAGAR"}, "no": 15, "scharr": "19:26", "scharr_date": "29 Feb 2016", "latemin": 57}, {"actdep": "20:38", "station": "MUD", "status": "57 mins late", "has_departed": true, "schdep": "19:41", "has_arrived": true, "day": 0, "actarr": "20:36", "distance": 275, "actarr_date": "29 Feb 2016", "station_": {"code": "MUD", "name": "MURADNAGAR"}, "no": 16, "scharr": "19:39", "scharr_date": "29 Feb 2016", "latemin": 57}, {"actdep": "20:54", "station": "GZN", "status": "57 mins late", "has_departed": false, "schdep": "19:57", "has_arrived": false, "day": 0, "actarr": "20:53", "distance": 286, "actarr_date": "29 Feb 2016", "station_": {"code": "GZN", "name": "N GHAZIABAD"}, "no": 17, "scharr": "19:56", "scharr_date": "29 Feb 2016", "latemin": 57}, {"actdep": "21:05", "station": "GZB", "status": "38 mins late", "has_departed": true, "schdep": "20:27", "has_arrived": true, "day": 0, "actarr": "21:03", "distance": 292, "actarr_date": "29 Feb 2016", "station_": {"code": "GZB", "name": "GHAZIABAD"}, "no": 18, "scharr": "20:25", "scharr_date": "29 Feb 2016", "latemin": 38}, {"actdep": "21:15", "station": "SBB", "status": "38 mins late", "has_departed": false, "schdep": "20:37", "has_arrived": false, "day": 0, "actarr": "21:13", "distance": 299, "actarr_date": "29 Feb 2016", "station_": {"code": "SBB", "name": "SAHIBABAD"}, "no": 19, "scharr": "20:35", "scharr_date": "29 Feb 2016", "latemin": 38}, {"actdep": "22:50", "station": "NZM", "status": "60 mins late", "has_departed": true, "schdep": "21:55", "has_arrived": true, "day": 0, "actarr": "22:15", "distance": 320, "actarr_date": "29 Feb 2016", "station_": {"code": "NZM", "name": "HAZRAT NIZAMUDDIN"}, "no": 20, "scharr": "21:15", "scharr_date": "29 Feb 2016", "latemin": 60}, {"actdep": "23:21", "station": "TKD", "status": "60 mins late", "has_departed": true, "schdep": "22:20", "has_arrived": true, "day": 0, "actarr": "23:18", "distance": 330, "actarr_date": "29 Feb 2016", "station_": {"code": "TKD", "name": "TUGLAKABAD"}, "no": 21, "scharr": "22:18", "scharr_date": "29 Feb 2016", "latemin": 60}, {"actdep": "23:38", "station": "FDB", "status": "60 mins late", "has_departed": true, "schdep": "22:38", "has_arrived": true, "day": 0, "actarr": "23:36", "distance": 341, "actarr_date": "29 Feb 2016", "station_": {"code": "FDB", "name": "FARIDABAD"}, "no": 22, "scharr": "22:36", "scharr_date": "29 Feb 2016", "latemin": 60}, {"actdep": "23:50", "station": "BVH", "status": "58 mins late", "has_departed": false, "schdep": "22:52", "has_arrived": false, "day": 0, "actarr": "23:48", "distance": 349, "actarr_date": "29 Feb 2016", "station_": {"code": "BVH", "name": "BALLABGARH"}, "no": 23, "scharr": "22:50", "scharr_date": "29 Feb 2016", "latemin": 58}, {"actdep": "00:22", "station": "PWL", "status": "42 mins late", "has_departed": true, "schdep": "23:40", "has_arrived": true, "day": 1, "actarr": "00:20", "distance": 370, "actarr_date": "1 Mar 2016", "station_": {"code": "PWL", "name": "PALWAL"}, "no": 24, "scharr": "23:38", "scharr_date": "29 Feb 2016", "latemin": 42}, {"actdep": "00:56", "station": "KSV", "status": "46 mins late", "has_departed": true, "schdep": "00:10", "has_arrived": true, "day": 1, "actarr": "00:54", "distance": 412, "actarr_date": "1 Mar 2016", "station_": {"code": "KSV", "name": "KOSI KALAN"}, "no": 25, "scharr": "00:08", "scharr_date": "1 Mar 2016", "latemin": 46}, {"actdep": "01:40", "station": "MTJ", "status": "5 mins late", "has_departed": true, "schdep": "01:35", "has_arrived": true, "day": 1, "actarr": "01:35", "distance": 453, "actarr_date": "1 Mar 2016", "station_": {"code": "MTJ", "name": "MATHURA JN"}, "no": 26, "scharr": "01:30", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "02:15", "station": "BTE", "status": "5 mins late", "has_departed": true, "schdep": "02:15", "has_arrived": true, "day": 1, "actarr": "02:10", "distance": 487, "actarr_date": "1 Mar 2016", "station_": {"code": "BTE", "name": "BHARATPUR JN"}, "no": 27, "scharr": "02:05", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "02:50", "station": "BXN", "status": "8 mins late", "has_departed": true, "schdep": "02:45", "has_arrived": true, "day": 1, "actarr": "02:48", "distance": 529, "actarr_date": "1 Mar 2016", "station_": {"code": "BXN", "name": "BAYANA JN"}, "no": 28, "scharr": "02:40", "scharr_date": "1 Mar 2016", "latemin": 8}, {"actdep": "03:09", "station": "FSP", "status": "4 mins late", "has_departed": true, "schdep": "03:05", "has_arrived": true, "day": 1, "actarr": "03:07", "distance": 548, "actarr_date": "1 Mar 2016", "station_": {"code": "FSP", "name": "FATEH SINGHPURA"}, "no": 29, "scharr": "03:03", "scharr_date": "1 Mar 2016", "latemin": 4}, {"actdep": "03:27", "station": "HAN", "status": "10 mins late", "has_departed": true, "schdep": "03:20", "has_arrived": true, "day": 1, "actarr": "03:25", "distance": 562, "actarr_date": "1 Mar 2016", "station_": {"code": "HAN", "name": "HINDAUN CITY"}, "no": 30, "scharr": "03:15", "scharr_date": "1 Mar 2016", "latemin": 10}, {"actdep": "03:42", "station": "SMBJ", "status": "10 mins late", "has_departed": true, "schdep": "03:32", "has_arrived": true, "day": 1, "actarr": "03:40", "distance": 572, "actarr_date": "1 Mar 2016", "station_": {"code": "SMBJ", "name": "SHRI MAHABIRJI"}, "no": 31, "scharr": "03:30", "scharr_date": "1 Mar 2016", "latemin": 10}, {"actdep": "04:25", "station": "GGC", "status": "-7 mins late", "has_departed": true, "schdep": "04:25", "has_arrived": true, "day": 1, "actarr": "04:08", "distance": 606, "actarr_date": "1 Mar 2016", "station_": {"code": "GGC", "name": "GANGAPUR CITY"}, "no": 32, "scharr": "04:15", "scharr_date": "1 Mar 2016", "latemin": -7}, {"actdep": "04:45", "station": "NNW", "status": "2 mins late", "has_departed": true, "schdep": "04:43", "has_arrived": true, "day": 1, "actarr": "04:43", "distance": 623, "actarr_date": "1 Mar 2016", "station_": {"code": "NNW", "name": "NRYNPUR TATWAR"}, "no": 33, "scharr": "04:41", "scharr_date": "1 Mar 2016", "latemin": 2}, {"actdep": "05:03", "station": "MLZ", "status": "4 mins late", "has_departed": true, "schdep": "04:59", "has_arrived": true, "day": 1, "actarr": "05:01", "distance": 639, "actarr_date": "1 Mar 2016", "station_": {"code": "MLZ", "name": "MALARNA"}, "no": 34, "scharr": "04:57", "scharr_date": "1 Mar 2016", "latemin": 4}, {"actdep": "05:35", "station": "SWM", "status": "10 mins late", "has_departed": true, "schdep": "05:25", "has_arrived": true, "day": 1, "actarr": "05:30", "distance": 669, "actarr_date": "1 Mar 2016", "station_": {"code": "SWM", "name": "SAWAI MADHOPUR"}, "no": 35, "scharr": "05:20", "scharr_date": "1 Mar 2016", "latemin": 10}, {"actdep": "06:07", "station": "IDG", "status": "11 mins late", "has_departed": true, "schdep": "05:55", "has_arrived": true, "day": 1, "actarr": "06:04", "distance": 706, "actarr_date": "1 Mar 2016", "station_": {"code": "IDG", "name": "INDARGARH"}, "no": 36, "scharr": "05:53", "scharr_date": "1 Mar 2016", "latemin": 11}, {"actdep": "06:20", "station": "LKE", "status": "13 mins late", "has_departed": true, "schdep": "06:07", "has_arrived": true, "day": 1, "actarr": "06:18", "distance": 717, "actarr_date": "1 Mar 2016", "station_": {"code": "LKE", "name": "LAKHERI"}, "no": 37, "scharr": "06:05", "scharr_date": "1 Mar 2016", "latemin": 13}, {"actdep": "06:44", "station": "KPZ", "status": "14 mins late", "has_departed": true, "schdep": "06:30", "has_arrived": true, "day": 1, "actarr": "06:42", "distance": 744, "actarr_date": "1 Mar 2016", "station_": {"code": "KPZ", "name": "KAPREN"}, "no": 38, "scharr": "06:28", "scharr_date": "1 Mar 2016", "latemin": 14}, {"actdep": "07:05", "station": "KPTN", "status": "15 mins late", "has_departed": true, "schdep": "06:50", "has_arrived": true, "day": 1, "actarr": "07:03", "distance": 764, "actarr_date": "1 Mar 2016", "station_": {"code": "KPTN", "name": "KESHORAI PATAN"}, "no": 39, "scharr": "06:48", "scharr_date": "1 Mar 2016", "latemin": 15}, {"actdep": "07:17", "station": "GQL", "status": "16 mins late", "has_departed": true, "schdep": "07:00", "has_arrived": true, "day": 1, "actarr": "07:15", "distance": 772, "actarr_date": "1 Mar 2016", "station_": {"code": "GQL", "name": "GURLA"}, "no": 40, "scharr": "06:59", "scharr_date": "1 Mar 2016", "latemin": 16}, {"actdep": "08:00", "station": "KOTA", "status": "0 mins late", "has_departed": true, "schdep": "07:50", "has_arrived": true, "day": 1, "actarr": "07:30", "distance": 777, "actarr_date": "1 Mar 2016", "station_": {"code": "KOTA", "name": "KOTA JN"}, "no": 41, "scharr": "07:30", "scharr_date": "1 Mar 2016", "latemin": 0}, {"actdep": "08:24", "station": "DKNT", "status": "13 mins late", "has_departed": true, "schdep": "08:08", "has_arrived": true, "day": 1, "actarr": "08:20", "distance": 787, "actarr_date": "1 Mar 2016", "station_": {"code": "DKNT", "name": "DAKANIYA TALAV"}, "no": 42, "scharr": "08:07", "scharr_date": "1 Mar 2016", "latemin": 13}, {"actdep": "08:53", "station": "DARA", "status": "15 mins late", "has_departed": true, "schdep": "08:39", "has_arrived": true, "day": 1, "actarr": "08:52", "distance": 825, "actarr_date": "1 Mar 2016", "station_": {"code": "DARA", "name": "DARA"}, "no": 43, "scharr": "08:37", "scharr_date": "1 Mar 2016", "latemin": 15}, {"actdep": "09:22", "station": "MKX", "status": "15 mins late", "has_departed": true, "schdep": "08:55", "has_arrived": true, "day": 1, "actarr": "09:08", "distance": 839, "actarr_date": "1 Mar 2016", "station_": {"code": "MKX", "name": "MORAK"}, "no": 44, "scharr": "08:53", "scharr_date": "1 Mar 2016", "latemin": 15}, {"actdep": "09:44", "station": "RMA", "status": "32 mins late", "has_departed": true, "schdep": "09:10", "has_arrived": true, "day": 1, "actarr": "09:40", "distance": 850, "actarr_date": "1 Mar 2016", "station_": {"code": "RMA", "name": "RAMGANJ MANDI"}, "no": 45, "scharr": "09:08", "scharr_date": "1 Mar 2016", "latemin": 32}, {"actdep": "10:18", "station": "JHW", "status": "34 mins late", "has_departed": true, "schdep": "09:25", "has_arrived": true, "day": 1, "actarr": "09:57", "distance": 861, "actarr_date": "1 Mar 2016", "station_": {"code": "JHW", "name": "JHALAWAR ROAD"}, "no": 46, "scharr": "09:23", "scharr_date": "1 Mar 2016", "latemin": 34}, {"actdep": "11:13", "station": "BWM", "status": "87 mins late", "has_departed": true, "schdep": "09:45", "has_arrived": true, "day": 1, "actarr": "11:10", "distance": 878, "actarr_date": "1 Mar 2016", "station_": {"code": "BWM", "name": "BHAWANI MANDI"}, "no": 47, "scharr": "09:43", "scharr_date": "1 Mar 2016", "latemin": 87}, {"actdep": "11:33", "station": "GOH", "status": "87 mins late", "has_departed": true, "schdep": "10:05", "has_arrived": true, "day": 1, "actarr": "11:30", "distance": 900, "actarr_date": "1 Mar 2016", "station_": {"code": "GOH", "name": "GAROT"}, "no": 48, "scharr": "10:03", "scharr_date": "1 Mar 2016", "latemin": 87}, {"actdep": "11:42", "station": "SGZ", "status": "73 mins late", "has_departed": true, "schdep": "10:30", "has_arrived": true, "day": 1, "actarr": "11:41", "distance": 911, "actarr_date": "1 Mar 2016", "station_": {"code": "SGZ", "name": "SHAMGARH"}, "no": 49, "scharr": "10:28", "scharr_date": "1 Mar 2016", "latemin": 73}, {"actdep": "11:50", "station": "SVA", "status": "67 mins late", "has_departed": true, "schdep": "10:44", "has_arrived": true, "day": 1, "actarr": "11:49", "distance": 924, "actarr_date": "1 Mar 2016", "station_": {"code": "SVA", "name": "SUWASRA"}, "no": 50, "scharr": "10:42", "scharr_date": "1 Mar 2016", "latemin": 67}, {"actdep": "12:00", "station": "CMU", "status": "61 mins late", "has_departed": true, "schdep": "11:00", "has_arrived": true, "day": 1, "actarr": "11:59", "distance": 940, "actarr_date": "1 Mar 2016", "station_": {"code": "CMU", "name": "CHAU MAHLA"}, "no": 51, "scharr": "10:58", "scharr_date": "1 Mar 2016", "latemin": 61}, {"actdep": "12:18", "station": "THUR", "status": "52 mins late", "has_departed": false, "schdep": "11:26", "has_arrived": false, "day": 1, "actarr": "12:16", "distance": 954, "actarr_date": "1 Mar 2016", "station_": {"code": "THUR", "name": "THURIA"}, "no": 52, "scharr": "11:24", "scharr_date": "1 Mar 2016", "latemin": 52}, {"actdep": "12:19", "station": "VMA", "status": "30 mins late", "has_departed": true, "schdep": "11:50", "has_arrived": true, "day": 1, "actarr": "12:18", "distance": 962, "actarr_date": "1 Mar 2016", "station_": {"code": "VMA", "name": "VIKRAMGARH ALOT"}, "no": 53, "scharr": "11:48", "scharr_date": "1 Mar 2016", "latemin": 30}, {"actdep": "12:26", "station": "LNR", "status": "21 mins late", "has_departed": false, "schdep": "12:05", "has_arrived": false, "day": 1, "actarr": "12:24", "distance": 975, "actarr_date": "1 Mar 2016", "station_": {"code": "LNR", "name": "LUNI RICHHA"}, "no": 54, "scharr": "12:03", "scharr_date": "1 Mar 2016", "latemin": 21}, {"actdep": "12:34", "station": "MEP", "status": "4 mins late", "has_departed": false, "schdep": "12:30", "has_arrived": false, "day": 1, "actarr": "12:32", "distance": 985, "actarr_date": "1 Mar 2016", "station_": {"code": "MEP", "name": "MAHIDPUR ROAD"}, "no": 55, "scharr": "12:28", "scharr_date": "1 Mar 2016", "latemin": 4}, {"actdep": "13:40", "station": "NAD", "status": "30 mins late", "has_departed": true, "schdep": "13:15", "has_arrived": true, "day": 1, "actarr": "13:35", "distance": 1002, "actarr_date": "1 Mar 2016", "station_": {"code": "NAD", "name": "NAGDA JN"}, "no": 56, "scharr": "13:05", "scharr_date": "1 Mar 2016", "latemin": 30}, {"actdep": "13:58", "station": "KUH", "status": "28 mins late", "has_departed": true, "schdep": "13:33", "has_arrived": true, "day": 1, "actarr": "13:56", "distance": 1016, "actarr_date": "1 Mar 2016", "station_": {"code": "KUH", "name": "KHACHROD"}, "no": 57, "scharr": "13:28", "scharr_date": "1 Mar 2016", "latemin": 28}, {"actdep": "14:09", "station": "RNH", "status": "25 mins late", "has_departed": true, "schdep": "13:44", "has_arrived": true, "day": 1, "actarr": "14:08", "distance": 1026, "actarr_date": "1 Mar 2016", "station_": {"code": "RNH", "name": "RUNKHERA"}, "no": 58, "scharr": "13:43", "scharr_date": "1 Mar 2016", "latemin": 25}, {"actdep": "14:18", "station": "BOD", "status": "25 mins late", "has_departed": true, "schdep": "13:53", "has_arrived": true, "day": 1, "actarr": "14:17", "distance": 1034, "actarr_date": "1 Mar 2016", "station_": {"code": "BOD", "name": "BANGROD"}, "no": 59, "scharr": "13:52", "scharr_date": "1 Mar 2016", "latemin": 25}, {"actdep": "14:40", "station": "RTM", "status": "15 mins late", "has_departed": true, "schdep": "14:25", "has_arrived": true, "day": 1, "actarr": "14:30", "distance": 1047, "actarr_date": "1 Mar 2016", "station_": {"code": "RTM", "name": "RATLAM JN"}, "no": 60, "scharr": "14:15", "scharr_date": "1 Mar 2016", "latemin": 15}, {"actdep": "15:21", "station": "RTI", "status": "17 mins late", "has_departed": true, "schdep": "14:50", "has_arrived": true, "day": 1, "actarr": "15:06", "distance": 1075, "actarr_date": "1 Mar 2016", "station_": {"code": "RTI", "name": "RAOTI"}, "no": 61, "scharr": "14:49", "scharr_date": "1 Mar 2016", "latemin": 17}, {"actdep": "15:35", "station": "BOG", "status": "31 mins late", "has_departed": true, "schdep": "15:03", "has_arrived": true, "day": 1, "actarr": "15:33", "distance": 1087, "actarr_date": "1 Mar 2016", "station_": {"code": "BOG", "name": "BHAIRONGARH"}, "no": 62, "scharr": "15:02", "scharr_date": "1 Mar 2016", "latemin": 31}, {"actdep": "15:54", "station": "BMI", "status": "42 mins late", "has_departed": true, "schdep": "15:13", "has_arrived": true, "day": 1, "actarr": "15:53", "distance": 1094, "actarr_date": "1 Mar 2016", "station_": {"code": "BMI", "name": "BAMNIA"}, "no": 63, "scharr": "15:11", "scharr_date": "1 Mar 2016", "latemin": 42}, {"actdep": "15:59", "station": "AGR", "status": "39 mins late", "has_departed": true, "schdep": "15:20", "has_arrived": true, "day": 1, "actarr": "15:58", "distance": 1098, "actarr_date": "1 Mar 2016", "station_": {"code": "AGR", "name": "AMARGARH"}, "no": 64, "scharr": "15:19", "scharr_date": "1 Mar 2016", "latemin": 39}, {"actdep": "16:12", "station": "PCN", "status": "39 mins late", "has_departed": true, "schdep": "15:33", "has_arrived": true, "day": 1, "actarr": "16:11", "distance": 1107, "actarr_date": "1 Mar 2016", "station_": {"code": "PCN", "name": "PANCH PIPILA"}, "no": 65, "scharr": "15:32", "scharr_date": "1 Mar 2016", "latemin": 39}, {"actdep": "16:23", "station": "THDR", "status": "36 mins late", "has_departed": true, "schdep": "15:47", "has_arrived": true, "day": 1, "actarr": "16:21", "distance": 1121, "actarr_date": "1 Mar 2016", "station_": {"code": "THDR", "name": "THANDLA RD"}, "no": 66, "scharr": "15:45", "scharr_date": "1 Mar 2016", "latemin": 36}, {"actdep": "16:33", "station": "MGN", "status": "31 mins late", "has_departed": true, "schdep": "16:02", "has_arrived": true, "day": 1, "actarr": "16:31", "distance": 1129, "actarr_date": "1 Mar 2016", "station_": {"code": "MGN", "name": "MEGHNAGAR"}, "no": 67, "scharr": "16:00", "scharr_date": "1 Mar 2016", "latemin": 31}, {"actdep": "16:46", "station": "ANAS", "status": "31 mins late", "has_departed": true, "schdep": "16:15", "has_arrived": true, "day": 1, "actarr": "16:45", "distance": 1143, "actarr_date": "1 Mar 2016", "station_": {"code": "ANAS", "name": "ANAS"}, "no": 68, "scharr": "16:14", "scharr_date": "1 Mar 2016", "latemin": 31}, {"actdep": "16:55", "station": "BIO", "status": "32 mins late", "has_departed": true, "schdep": "16:23", "has_arrived": true, "day": 1, "actarr": "16:54", "distance": 1151, "actarr_date": "1 Mar 2016", "station_": {"code": "BIO", "name": "BORDI"}, "no": 69, "scharr": "16:22", "scharr_date": "1 Mar 2016", "latemin": 32}, {"actdep": "17:10", "station": "DHD", "status": "30 mins late", "has_departed": true, "schdep": "16:40", "has_arrived": true, "day": 1, "actarr": "17:05", "distance": 1162, "actarr_date": "1 Mar 2016", "station_": {"code": "DHD", "name": "DAHOD"}, "no": 70, "scharr": "16:35", "scharr_date": "1 Mar 2016", "latemin": 30}, {"actdep": "17:41", "station": "LMK", "status": "32 mins late", "has_departed": true, "schdep": "17:08", "has_arrived": true, "day": 1, "actarr": "17:39", "distance": 1196, "actarr_date": "1 Mar 2016", "station_": {"code": "LMK", "name": "LIMKHEDA"}, "no": 71, "scharr": "17:07", "scharr_date": "1 Mar 2016", "latemin": 32}, {"actdep": "17:48", "station": "PPD", "status": "31 mins late", "has_departed": true, "schdep": "17:18", "has_arrived": true, "day": 1, "actarr": "17:47", "distance": 1204, "actarr_date": "1 Mar 2016", "station_": {"code": "PPD", "name": "PIPLOD JN"}, "no": 72, "scharr": "17:16", "scharr_date": "1 Mar 2016", "latemin": 31}, {"actdep": "17:59", "station": "SAT", "status": "30 mins late", "has_departed": true, "schdep": "17:30", "has_arrived": true, "day": 1, "actarr": "17:58", "distance": 1216, "actarr_date": "1 Mar 2016", "station_": {"code": "SAT", "name": "SANT ROAD"}, "no": 73, "scharr": "17:28", "scharr_date": "1 Mar 2016", "latemin": 30}, {"actdep": "18:35", "station": "GDA", "status": "-13 mins late", "has_departed": true, "schdep": "18:35", "has_arrived": true, "day": 1, "actarr": "18:17", "distance": 1236, "actarr_date": "1 Mar 2016", "station_": {"code": "GDA", "name": "GODHRA JN"}, "no": 74, "scharr": "18:30", "scharr_date": "1 Mar 2016", "latemin": -13}, {"actdep": "18:50", "station": "KRSA", "status": "2 mins late", "has_departed": true, "schdep": "18:48", "has_arrived": true, "day": 1, "actarr": "18:49", "distance": 1247, "actarr_date": "1 Mar 2016", "station_": {"code": "KRSA", "name": "KHARSALIYA"}, "no": 75, "scharr": "18:47", "scharr_date": "1 Mar 2016", "latemin": 2}, {"actdep": "19:04", "station": "DRL", "status": "4 mins late", "has_departed": true, "schdep": "19:00", "has_arrived": true, "day": 1, "actarr": "19:02", "distance": 1259, "actarr_date": "1 Mar 2016", "station_": {"code": "DRL", "name": "DEROL"}, "no": 76, "scharr": "18:58", "scharr_date": "1 Mar 2016", "latemin": 4}, {"actdep": "19:17", "station": "CPN", "status": "5 mins late", "has_departed": true, "schdep": "19:13", "has_arrived": true, "day": 1, "actarr": "19:16", "distance": 1272, "actarr_date": "1 Mar 2016", "station_": {"code": "CPN", "name": "CHAMPANER RD JN"}, "no": 77, "scharr": "19:11", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "19:29", "station": "SMLA", "status": "5 mins late", "has_departed": true, "schdep": "19:24", "has_arrived": true, "day": 1, "actarr": "19:27", "distance": 1283, "actarr_date": "1 Mar 2016", "station_": {"code": "SMLA", "name": "SAMLAYA JN"}, "no": 78, "scharr": "19:22", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "20:10", "station": "BRC", "status": "5 mins late", "has_departed": true, "schdep": "20:05", "has_arrived": true, "day": 1, "actarr": "20:00", "distance": 1310, "actarr_date": "1 Mar 2016", "station_": {"code": "BRC", "name": "VADODARA JN"}, "no": 79, "scharr": "19:55", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "20:34", "station": "MYG", "status": "6 mins late", "has_departed": true, "schdep": "20:28", "has_arrived": true, "day": 1, "actarr": "20:33", "distance": 1340, "actarr_date": "1 Mar 2016", "station_": {"code": "MYG", "name": "MIYAGAM KARJAN"}, "no": 80, "scharr": "20:27", "scharr_date": "1 Mar 2016", "latemin": 6}, {"actdep": "21:12", "station": "BH", "status": "5 mins late", "has_departed": true, "schdep": "21:07", "has_arrived": true, "day": 1, "actarr": "21:10", "distance": 1380, "actarr_date": "1 Mar 2016", "station_": {"code": "BH", "name": "BHARUCH JN"}, "no": 81, "scharr": "21:05", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "21:23", "station": "AKV", "status": "5 mins late", "has_departed": true, "schdep": "21:18", "has_arrived": true, "day": 1, "actarr": "21:21", "distance": 1389, "actarr_date": "1 Mar 2016", "station_": {"code": "AKV", "name": "ANKLESHWAR JN"}, "no": 82, "scharr": "21:16", "scharr_date": "1 Mar 2016", "latemin": 5}, {"actdep": "21:40", "station": "KSB", "status": "7 mins late", "has_departed": true, "schdep": "21:34", "has_arrived": true, "day": 1, "actarr": "21:39", "distance": 1408, "actarr_date": "1 Mar 2016", "station_": {"code": "KSB", "name": "KOSAMBA JN"}, "no": 83, "scharr": "21:32", "scharr_date": "1 Mar 2016", "latemin": 7}, {"actdep": "22:38", "station": "ST", "status": "-17 mins late", "has_departed": true, "schdep": "22:38", "has_arrived": true, "day": 1, "actarr": "22:13", "distance": 1439, "actarr_date": "1 Mar 2016", "station_": {"code": "ST", "name": "SURAT"}, "no": 84, "scharr": "22:30", "scharr_date": "1 Mar 2016", "latemin": -17}, {"actdep": "23:58", "station": "NVS", "status": "54 mins late", "has_departed": true, "schdep": "23:05", "has_arrived": true, "day": 1, "actarr": "23:56", "distance": 1468, "actarr_date": "1 Mar 2016", "station_": {"code": "NVS", "name": "NAVSARI"}, "no": 85, "scharr": "23:02", "scharr_date": "1 Mar 2016", "latemin": 54}, {"actdep": "00:24", "station": "BIM", "status": "61 mins late", "has_departed": true, "schdep": "23:23", "has_arrived": true, "day": 2, "actarr": "00:22", "distance": 1489, "actarr_date": "2 Mar 2016", "station_": {"code": "BIM", "name": "BILIMORA JN"}, "no": 86, "scharr": "23:21", "scharr_date": "1 Mar 2016", "latemin": 61}, {"actdep": "00:43", "station": "BL", "status": "46 mins late", "has_departed": true, "schdep": "23:55", "has_arrived": true, "day": 2, "actarr": "00:39", "distance": 1507, "actarr_date": "2 Mar 2016", "station_": {"code": "BL", "name": "VALSAD"}, "no": 87, "scharr": "23:53", "scharr_date": "1 Mar 2016", "latemin": 46}, {"actdep": "01:07", "station": "VAPI", "status": "29 mins late", "has_departed": true, "schdep": "00:38", "has_arrived": true, "day": 2, "actarr": "01:05", "distance": 1532, "actarr_date": "2 Mar 2016", "station_": {"code": "VAPI", "name": "VAPI"}, "no": 88, "scharr": "00:36", "scharr_date": "2 Mar 2016", "latemin": 29}, {"actdep": "02:13", "station": "PLG", "status": "21 mins late", "has_departed": true, "schdep": "02:02", "has_arrived": true, "day": 2, "actarr": "02:11", "distance": 1615, "actarr_date": "2 Mar 2016", "station_": {"code": "PLG", "name": "PALGHAR"}, "no": 89, "scharr": "01:50", "scharr_date": "2 Mar 2016", "latemin": 21}, {"actdep": "03:00", "station": "VR", "status": "-16 mins late", "has_departed": true, "schdep": "02:58", "has_arrived": true, "day": 2, "actarr": "02:40", "distance": 1646, "actarr_date": "2 Mar 2016", "station_": {"code": "VR", "name": "VIRAR"}, "no": 90, "scharr": "02:56", "scharr_date": "2 Mar 2016", "latemin": -16}, {"actdep": "03:32", "station": "BVI", "status": "-10 mins late", "has_departed": true, "schdep": "03:32", "has_arrived": true, "day": 2, "actarr": "03:17", "distance": 1672, "actarr_date": "2 Mar 2016", "station_": {"code": "BVI", "name": "BORIVALI"}, "no": 91, "scharr": "03:27", "scharr_date": "2 Mar 2016", "latemin": -10}, {"actdep": "00:00", "station": "BDTS", "status": "-10 mins late", "has_departed": false, "schdep": "Destination", "has_arrived": true, "day": 2, "actarr": "04:10", "distance": 1690, "actarr_date": "2 Mar 2016", "station_": {"code": "BDTS", "name": "BANDRA TERMINUS"}, "no": 92, "scharr": "04:20", "scharr_date": "2 Mar 2016", "latemin": -10}]
stops=[1,14,26,41,60,79,92]
stop_time=['0','10','12','15','5','15']
'''
1 DEHRADUN
14 MEERUT CITY
26 MATHURA JN
41 KOTA JN
60 RATLAM JN
79 Vadodara
92 Bandra
'''

counter,st_index,end_index,nexts=[1,26,79,1]    #nexts stores next station number
last,board,depart,end,information,nextt=['','','','','','']

food,medicine,secu,clean=[[],[],[],[]]


@app.route('/simulation')
def sim():
    global counter
    counter=1
    return render_template('simulation.html',title='Simulation')

@app.route('/updatesimulation')
def updatesim():
    global counter,st_index,end_index,nextt,last,board,source,depart,end,information,nexts,stops,stop_time
    information=''
    tot=len(dic)        #total number of stations
    if counter>tot:
        counter=tot
    if counter==1:
        last='The train is at source station '+dic[1]['station_']['name']+'('+dic[1]['station_']['code']+') and is at a distance '+str(dic[st_index]['distance'])+'km from your boarding point.'
    elif counter<=st_index:
        last='The train was last seen at '+dic[counter-1]['station_']['name']+' and is '+dic[counter-1]['status']+'. It is at a distance '+str(dic[st_index]['distance']-dic[counter-1]['distance'])+'km from your boarding point.'
    elif counter<=end_index:
        last='The train was last seen at '+dic[counter-1]['station_']['name']+' and is '+dic[counter-1]['status']+'. You have covered a distance '+str(dic[counter-1]['distance']-dic[st_index]['distance'])+'km from your boarding point.'        
    else:
        last='The train was last seen at '+dic[counter-1]['station_']['name']+' and is '+dic[counter-1]['status']+'.'
    if counter==1:
        information='The Journey Begins!!!'
    if counter<st_index:
        board='The train is scheduled to arrive at your boarding station '+dic[st_index]['station_']['name']+'('+dic[st_index]['station_']['code']+') on '+dic[st_index]['scharr_date']+' at '+dic[st_index]['actarr']+' '+dic[st_index]['status']+'.'
    elif counter==st_index:
        information='Welcome to Indian Railways. Team PiRail wishes you a very happy journey!'
        board='The train has arrived at your boarding station '+dic[st_index]['station_']['name']+'('+dic[st_index]['station_']['code']+') on '+dic[st_index]['scharr_date']+' at '+dic[st_index]['actarr']+' '+dic[st_index]['status']+'.'
    else:
        board='The train has departed from your boarding station '+dic[st_index]['station_']['name']+'('+dic[st_index]['station_']['code']+') on '+dic[st_index]['scharr_date']+' at '+dic[st_index]['actarr']+' '+dic[st_index]['status']+'.'
    if counter<=st_index:
        depart='The train is scheduled to arrive at your destination '+dic[end_index]['station_']['name']+'('+dic[end_index]['station_']['code']+') on '+dic[end_index]['scharr_date']+' at '+dic[end_index]['actarr']+' '+dic[end_index]['status']+'. You journey distance is '+str(dic[end_index]['distance']-dic[st_index]['distance'])+'km.'
    elif counter<end_index:
        depart='The train is scheduled to arrive at your destination '+dic[end_index]['station_']['name']+'('+dic[end_index]['station_']['code']+') on '+dic[end_index]['scharr_date']+' at '+dic[end_index]['actarr']+' '+dic[end_index]['status']+'. You have more '+str(dic[end_index]['distance']-dic[counter-1]['distance'])+'km to cover.'
    elif counter==end_index:
        information='Your destination has arrived. Hope you had a wonderful time using PiRail!'
        depart='The train has arrived at your destination '+dic[end_index]['station_']['name']+'('+dic[end_index]['station_']['code']+') on '+dic[end_index]['scharr_date']+' at '+dic[end_index]['actarr']+' '+dic[end_index]['status']+'.'
    else:
        depart='The train has departed from your destination '+dic[end_index]['station_']['name']+'('+dic[end_index]['station_']['code']+') on '+dic[end_index]['scharr_date']+' at '+dic[end_index]['actarr']+' '+dic[end_index]['status']+'. You covered a total journey of '+str(dic[end_index]['distance']-dic[st_index]['distance'])+'km.'
    if counter<tot-1:
        end='The train is scheduled to reach its final stop '+dic[tot-1]['station_']['name']+'('+dic[tot-1]['station_']['code']+') on '+dic[tot-1]['scharr_date']+' at '+dic[tot-1]['actarr']+' '+dic[tot-1]['status']+'.'
    else:
        information='The journey is over!!! Thank you.'
        end='The train reached its final stop '+dic[tot-1]['station_']['name']+'('+dic[tot-1]['station_']['code']+') on '+dic[tot-1]['scharr_date']+' at '+dic[tot-1]['actarr']+' '+dic[tot-1]['status']+'.'
    print dic[stops[nexts]]
    if counter<tot-1:
        nextt='The train will arrive at the next station '+dic[stops[nexts]]['station_']['name']+'('+dic[stops[nexts]]['station_']['code']+') on '+dic[stops[nexts]]['scharr_date']+' at '+dic[stops[nexts]]['actarr']+' '+dic[stops[nexts]]['status']+'. It is more '+str(dic[stops[nexts]]['distance']-dic[counter]['distance'])+'km away. It will halt for '+stop_time[nexts]+' mins.'
    else:
        nextt='The train has reached its last stop.'
    if counter==stops[nexts]:
        nexts+=1
    counter+=1
    result=information+'<br><br><br>'+last+'<br>'+nextt+'<br><br>'+board+'<br>'+depart+'<br>'+end
    return result

@app.route('/control/<state>', methods=['GET', 'POST'])
def control(state):
    if 'pnr' in session:
      login=True
    else:
      login=False
    if login==False:
         flash('Please login first to use this feature.')
         return redirect('/index')
    name=''
    seat=0
    switch=0
    passengers=models.Chart.query.all()
    for p in passengers:
         if str(p.pnr)==session['pnr']:
              name=p.name
              seat=p.seat
    if seat<=3:
       switch=2
    else:
       switch=3
    if (state=='Off' or state=='On'):
       if state=='Off':
       	  GPIO.setup(switch,GPIO.OUT)
          GPIO.output(switch,GPIO.LOW)
          cur_state='Off'
          change_state='On'
       else:
          GPIO.setup(switch,GPIO.OUT)
          GPIO.output(switch,GPIO.HIGH)
          cur_state='On'
          change_state='Off'
       return render_template('control.html',name=name,seat=seat,switch=switch,login=login,cur_state=cur_state,change_state=change_state)
    GPIO.setup(switch,GPIO.IN)
    val=GPIO.input(switch)
    if val==GPIO.HIGH:
       cur_state='On'
       change_state='Off'
    if val==GPIO.LOW:
       cur_state='Off'
       change_state='On'
    return render_template('control.html',name=name,seat=seat,switch=switch,login=login,cur_state=cur_state,change_state=change_state)



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
    if login==False:
         flash('Please login first to access Immediate page.')
         return redirect('/index')
    name=''
    seat=0
    pnr=session['pnr']
    passengers=models.Chart.query.all()
    for p in passengers:
         if str(p.pnr)==session['pnr']:
              name=p.name
              seat=p.seat
    form=ImmediateForm()
    global food,secu,medicine,clean
    if form.validate_on_submit():  
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
    return render_template('immediate.html',title='Immediate',form=form,login=login,name=name,pnr=pnr)

@app.route('/trainstats')
def trainstats():
    return render_template('trainstats.html',title='Train Statistics');

@app.route('/')
@app.route('/index')
def index():
    name=''
    seat=0
    switch=0
    if 'pnr' in session:
      users=models.Chart.query.all()
      for u in users:
          if session['pnr']==str(u.pnr):
              seat=u.seat
              name=u.name
              break
      login=True
    else:
      login=False
    return render_template('index.html',title='WELCOME TO INDIAN RAILWAYS',login=login,name=name)

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
          name=''
          users=models.Chart.query.all()
          for u in users:
              if session['pnr']==str(u.pnr):
                name=u.name
                break
          return render_template('index.html',title='WELCOME',login=True,name=name)
        else:
          return render_template('index.html',title='WELCOME',login=False,login_error_message='Wrong password provided')          
      else:
        return render_template('index.html',title='WELCOME',login=False,login_error_message='You are in the wrong train')
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
   if login==False:
         flash('Please login first to provide Feedback.')
         return redirect('/index')
   form=LoginForm()
   name=''
   seat=0
   pnr=session['pnr']
   passengers=models.Chart.query.all()
   for p in passengers:
         if str(p.pnr)==session['pnr']:
              name=p.name
              seat=p.seat
   if form.validate_on_submit():
        flash('Thank You %s for your valuable feedback' %
              (name))
        user = User(pnr=int(pnr), name=name, food=form.food.data,sanitation=form.sanitation.data,journey=form.journey.data,feedback=form.feedback.data)
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
   form=PNREntry()
   if form.validate_on_submit():
      pnr=form.pnr.data
      return redirect('/myyatrainfo/'+pnr)
   return render_template('pnrentry.html',title='MyYatraInfo',form=form,heading="MyYatraInfo",login=login)

   
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
          except Exception as e:
             print e
             return render_template('myyatrainfoerrnonet.html',title='MyYatraInfo',login=login)
   except Exception as e:
       print e
       return render_template('myyatrainfoerrnonet.html',title='MyYatraInfo',login=login)
   print response_dict
   return render_template('myyatrainfo.html',title='MyYatraInfo',values=response_dict,login=login)


