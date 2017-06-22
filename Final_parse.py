from suds.client import Client
import requests
from lxml import etree
import datetime
import time
import calendar

import datetime
mydate = datetime.datetime.now()
mydate.strftime("%B") # 'December'
mydate.strftime("%b") # 'dec'
        
url="http://maven.geohems.com/mvts/AssetTrackingObjWebService.asmx?WSDL"
client = Client(url)

payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetEquipmentEngineMonitoringReport xmlns=\"http://tempuri.org/\">\n      <APIKey>J12CM751YTU</APIKey>\n      <EquipmentId>Govind-Paritwadi-CP2</EquipmentId>\n      <StartDate>"+mydate+ "09:00</StartDate>\n      <EndDate>"+mydate+"09:05</EndDate>\n    </GetEquipmentEngineMonitoringReport>\n  </soap:Body>\n</soap:Envelope>\n\n"
print payload
headers = {
    'content-type': "text/xml; charset=utf-8",
    'soapaction': "http://tempuri.org/GetEquipmentEngineMonitoringReport",
    } 
response = requests.post(url,data=payload,headers=headers)

data = response.content
print data
fp = open("parse.xml","w")
fp.write(data)
fp.close()

tree = etree.XML(data)
ns = {'default': 'http://tempuri.org/'}

centers = tree.xpath('//default:EquipmentId/text()', namespaces=ns)
times   = tree.xpath('//default:Time/text()', namespaces=ns)
ids     = tree.xpath('//default:ParamID/text()', namespaces=ns)
names   = tree.xpath('//default:ParamName/text()', namespaces=ns)
values  = tree.xpath('//default:ParamValue/text()', namespaces=ns)

#print(centers)

print(times[0])  + "\t"+(ids[0])+"\t"+(names[0])+"\t"+(values[0])
print(times[54]) + "\t"+(ids[0])+"\t"+(names[0])+"\t"+(values[54])
print(times[1])  + "\t"+(ids[1])+"\t"+(names[1])+"\t"+(values[1])
print(times[54]) + "\t"+(ids[1])+"\t"+(names[1])+"\t"+(values[54])
print(times[108])+ "\t"+(ids[0])+"\t"+(names[0])+"\t"+(values[108])
