from bs4 import BeautifulSoup
import re
import time
infile = open("parse.xml","r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')
print soup.prettify()
titles = soup.find_all('EquipmentParameterDetailsModel')
data = soup.find_all('ParamID')

#print titles
for EquipmentParameterDetailsModel in titles:
    x = soup.contents[0].EquipmentParameterDetailsModel
   # print x                                             #this gives me data for only ParamID=670 I want to capture the same for ParamID=671
   # print "\n"
    #for ParamID in data:    
    y = soup.contents[0].EquipmentParameterDetailsModel.ParamID
    # print y
    '''
    name_3 = EquipmentParameterDetailsModel.contents[3]
    print name_3
    print "\n"
    time.sleep(1)'''
    #print(EquipmentParameterDetailsModel.get_text())
    #print (soup.find_all(ParamID='671'))
    #print soup.EquipmentParameterDetailsModel.ParamID
    #print soup.EquipmentParameterDetailsModel.ParamName
    #print soup.EquipmentParameterDetailsModel.ParamValue
    #time.sleep(1)
    #print soup.EquipmentParameterDetailsModel.ParamID
    #print soup.EquipmentParameterDetailsModel.ParamName
    #print soup.EquipmentParameterDetailsModel.ParamValue

    #for EquipmentParameterDetailsModel in titles:
#    print(sou.equipmentparameterdetailsmodel.find)
    

#print(sou.paramlist.findAll(name="paramid"))
#print (sou.equipmentparameterdetailsmodel.find(name="paramvalue"))
    '''ID = soup.find_all('ParamID') 
    value = soup.find_all('ParamValue')
    #print ID
    for ParamID in ID:
            
            for ParamValue in value:
                print (ParamID.get_text())
                print "\t\t"
                print(ParamValue.get_text())
                print "\n\n" '''
    
        

        
        
    
    
