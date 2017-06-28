from suds.client import Client                      #Soap client for webservices
import requests
from lxml import etree
import datetime
import time
import csv
import os.path
from time import strftime, gmtime, localtime
import pytz
import tzlocal

############################ libraries for Email ################################

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

recepients = ['tanmayee@promethean-power.com',
              'manouj@promethean-power.com',
              'bhavin@promethean-power.com',
              'vikas.gaikwad@promethean-power.com',
              'jofi@promethean-power.com']

############################ Date and Time #######################################

year  = datetime.date.today().strftime("%Y")
month = datetime.date.today().strftime("%b")
day   = datetime.date.today().strftime("%d")    
Date  = day+"-"+month+"-"+year
Time  = (time.strftime("%H:%M"))#"09:30"
#print Time

############################# IST to GMT conversion ##############################

now = datetime.datetime.utcnow()
two_min = datetime.timedelta(minutes=-2)
two_min_ago = now + two_min

p = str(now)
end = p[11:16]
q = str(two_min_ago)
start = q[11:16]
############################ Email variables ######################################

emailfrom  = "email-id"                                         #Senders email addr
#emailto    = "email-id"                                        #Receivers email addr
fileToSend =  Date+".csv"                                       #26-Jun-2017.csv"
username   = "username"
password   = "password"

############################ Calling URL for getting soap response ################

centre_name = ['Amul-Khadawali','Amul -Talvali','Amul-Kude','Amul-Lalthane','Amul-Musarne','Amul-Malwada','Amul Pedpargaon','Cavinkare','Device--0019',
               'Govind- Paritwadi-CP1','Govind-Paritwadi-CP2',
               'Mobile chiller','Mother Dairy Test','Nestle-Punjab','Promethean Lab']
               
url         = "http://rms.geohems.com/AssetTrackingObjWebService.asmx?WSDL"
client      = Client(url)

for i in centre_name:
    payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetEquipmentEngineMonitoringReport xmlns=\"http://tempuri.org/\">\n      <APIKey>J12CM751YTU</APIKey>\n      <EquipmentId>"+i+"</EquipmentId>\n      <StartDate>"+Date+" "+start+"</StartDate>\n      <EndDate>"+Date+" "+end+"</EndDate>\n    </GetEquipmentEngineMonitoringReport>\n  </soap:Body>\n</soap:Envelope>\n\n"
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
    #print(times[54]) +"\t"+(names[0])+"\t"+(values[54])
    #print(times[108])+"\t"+(names[0])+"\t"+(values[108])
    print(times[0])  +"\t"+(names[1])+"\t"+(values[1])
    #print(times[54]) +"\t"+(names[1])+"\t"+(values[54])
    #print(times[108])+"\t"+(names[1])+"\t"+(values[108])

#################################### Writing in .csv file #########################################    

    file_exists = os.path.isfile("C:/Python27/"+Date+".csv")
    with open(Date+'.csv','a')as csvfile:
        headers = ['center','Date','Time','Name','Value']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
        #writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
    
        #print times[0]
    #***********************Conversion of UTC to IST *******************************#
        date = times[0].replace('T',' ')
        print date
        x1= date[0:10]
        y1= date[11:19]
        z = x1+" "+y1
        print z
        local_timezone = tzlocal.get_localzone()
        utc_time = datetime.datetime.strptime(z, "%Y-%m-%d %H:%M:%S")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        print local_time
        q = str(local_time)
        x2= q[0:10]
        y2= q[11:16]
    #*******************************************************************************#
        
        writer.writerow({'center':centers[0],'Date':x2,'Time':y2,'Name':names[0],'Value':values[0]})
        writer.writerow({'center':centers[0],'Date':x2,'Time':y2,'Name':names[1],'Value':values[1]})
        #writer.writerow({'center':centers[0],'Time':times[0],'Name':names[0],'Value':values[0]})
        #writer.writerow({'center':centers[0],'Time':times[0],'Name':names[1],'Value':values[1]})

#################################### code for sending Email #######################################
       
msg = MIMEMultipart()
msg["From"] = emailfrom
#msg["To"] = emailto
msg["To"]= ", " .join(recepients)
msg["Subject"] = "Promethean Data Loggers"
msg.preamble = "Promethean Data Loggers"

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
server.sendmail(emailfrom, recepients, msg.as_string())
server.quit()
