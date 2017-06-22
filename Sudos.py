from suds.client import Client
import requests
from bs4 import BeautifulSoup
url="http://maven.geohems.com/mvts/AssetTrackingObjWebService.asmx?WSDL"
client = Client(url)
#print client ## shows the details of this service
payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetEquipmentEngineMonitoringReport xmlns=\"http://tempuri.org/\">\n      <APIKey>J12CM751YTU</APIKey>\n      <EquipmentId>Govind-Paritwadi-CP2</EquipmentId>\n      <StartDate>21-Jun-2017 05:34</StartDate>\n      <EndDate>21-Jun-2017 05:35</EndDate>\n    </GetEquipmentEngineMonitoringReport>\n  </soap:Body>\n</soap:Envelope>\n\n"
headers = {
    'content-type': "text/xml; charset=utf-8",
    'soapaction': "http://tempuri.org/GetEquipmentEngineMonitoringReport",
    } 
response = requests.post(url,data=payload,headers=headers)
print response.content
data = response.content
#required_dict = Client.dict(suds_object)
#print required_dict
fp = open("parse.xml","w")
fp.write(data)
fp.close()

'''soup = BeautifulSoup(data, 'html.parser')
searchTerms= ['Time','ParamID','ParamName','Paramvalue']
for st in searchTerms:
    print st+'\t'
    print soup.find(st.lower()).contents'''
