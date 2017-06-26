from time import strftime, gmtime, localtime

#def aslocaltimestr(utc_dt):
#    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

#print(aslocaltimestr(datetime(2010,  6, 6, 17, 29, 7, 730000)))
#print(aslocaltimestr(datetime(2010, 12, 6, 17, 29, 7, 730000)))
#print(aslocaltimestr(datetime.utcnow()))

utc_Time = strftime('%H:%M', gmtime()) #UTC time
print utc_Time
utc_hr = strftime('%H',gmtime())
utc_min = strftime('%M',gmtime())
#print utc_min
lag_time = int(utc_min)-01
lag_one = str(lag_time)
length = len(lag_one)
if length < 2:
    le = '0'+lag_one
    var1 = utc_hr +":"+str(le)
    print var1
else:
    print lag_time
    var1 = (utc_hr)+":"+str(lag_time)
    print var1
