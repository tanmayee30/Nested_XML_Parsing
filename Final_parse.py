from suds.client import Client                              #Soap client for webservices
import requests
from lxml import etree
import datetime
import time
import csv
import os.path
from time import strftime, gmtime, localtime

############################ Liberaries for Email ################################

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

############################ Date and Time #######################################

year  = datetime.date.today().strftime("%Y")
month = datetime.date.today().strftime("%b")
day   = datetime.date.today().strftime("%d")    
Date  = day+"-"+month+"-"+year
Time  = "10:20"#(time.strftime("%H:%M"))#"09:30"
#print Time

#time_hour = time.strftime("%H")
#time_min = time.strftime("%M")  
#time_one = int(time_min)-2
#STime = "10.15"#time_hour+":"+ str(time_one)
#print STime
#start_time = datetime.datetime.now()-datetime.timedelta(minutes=1)
#print start_time

############################# IST to GMT conversion ##############################

utc_Time = strftime('%H:%M', gmtime()) #UTC time
print utc_Time
utc_hr = strftime('%H',gmtime())
utc_min = strftime('%M',gmtime())
#print utc_min
lag_time = int(utc_min)-02
lag_one = str(lag_time)
length = len(lag_one)
if length < 2:
    le = '0'+lag_one
    var1 = utc_hr+":"+str(le)
    print var1
else:
    print lag_time
    var1 = utc_hr+":"+str(lag_time)
    print var1


############################ Email variables ######################################

emailfrom  = "promotestdata@gmail.com"                          #Senders email addr
emailto    = "vikas.gaikwad@promethean-power.com"                       #Receivers email addr
fileToSend =  Date+".csv"                                       #26-Jun-2017.csv"
username   = "**********************"
password   = "*******************"

############################ Calling URL for getting soap response ################

centre_name = ['Amul-Khadawali','Amul -Talvali','Amul-Kude','Amul-Lalthane','Amul-Musarne','Amul-Malwada','Amul Pedpargaon']
               #'Cavinkare',
               #'Device--0019',
               #'Govind-Paritwadi-CP1','Govind- Paritwadi-CP2',
               #'Mobile chiller','Mother Dairy Test',
               #'Nestle-Punjab',
               #'Promethean Lab']
url         = "http://rms.geohems.com/AssetTrackingObjWebService.asmx?WSDL"
client      = Client(url)

for i in centre_name:
    payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetEquipmentEngineMonitoringReport xmlns=\"http://tempuri.org/\">\n      <APIKey>J12CM751YTU</APIKey>\n      <EquipmentId>"+i+"</EquipmentId>\n      <StartDate>"+Date+" "+var1+"</StartDate>\n      <EndDate>"+Date+" "+utc_Time+"</EndDate>\n    </GetEquipmentEngineMonitoringReport>\n  </soap:Body>\n</soap:Envelope>\n\n"
    print payload
    headers = {
    'content-type': "text/xml; charset=utf-8",
    'soapaction': "http://tempuri.org/GetEquipmentEngineMonitoringReport",
    } 
    response = requests.post(url,data=payload,headers=headers)

    data = response.content
    #print data
    fp = open("parse.xml","w")
    fp.write(data)
    fp.close()

    tree = etree.XML(data)
    #print len(data)
    ns = {'default': 'http://tempuri.org/'}

    centers = tree.xpath('//default:EquipmentId/text()', namespaces=ns)
    times   = tree.xpath('//default:Time/text()', namespaces=ns)
    #ids     = tree.xpath('//default:ParamID/text()', namespaces=ns)
    names   = tree.xpath('//default:ParamName/text()', namespaces=ns)
    values  = tree.xpath('//default:ParamValue/text()', namespaces=ns)

    print(centers)
    print(times[0])  +"\t"+(names[0])+"\t"+(values[0])
    print(times[54]) +"\t"+(names[0])+"\t"+(values[54])
    #print(times[108])+"\t"+(names[0])+"\t"+(values[108])
    print(times[0])  +"\t"+(names[1])+"\t"+(values[1])
    print(times[54]) +"\t"+(names[1])+"\t"+(values[54])
    #print(times[108])+"\t"+(names[1])+"\t"+(values[108])

#################################### Writing in .csv file #########################################    

    file_exists = os.path.isfile("C:/Python27/"+Date+".csv")
    with open(Date+'.csv','a')as csvfile:
        headers = ['center','Time','Name','Value']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
        #writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
    
        writer.writerow({'center':centers[0],'Time':times[0],'Name':names[0],'Value':values[0]})
        writer.writerow({'center':centers[0],'Time':times[0],'Name':names[1],'Value':values[1]})

#################################### code for sending Email #######################################
       
msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "Promethean logger info"
msg.preamble = "Promethean logger info"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()
