from datetime import *
import datetime
import time

months = ["Unknown","January","Febuary","Marchh","April","May","June","July","August","September","October","November","December"]
datetimeWrite = (time.strftime("%d-%m-%Y "))
date = time.strftime("%d")
month= time.strftime("%m")
choices = {'01': 'Jan', '02':'Feb','03':'Mar','04':'Apr','05':'May','06': 'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
result = choices.get(month, 'default')
year = time.strftime("%Y")
Date = date+"-"+result+"-"+year
print Date

year=datetime.date.today().strftime("%Y")
month=datetime.date.today().strftime("%b")
day=datetime.date.today().strftime("%d")
Date = day+"-"+month+"-"+year
print Date
