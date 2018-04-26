#import azure
import time

#%%
import sys
#import os
import datetime
#import json
#import random
#import time
###############################################################################
cloudenv='tempalarm'
sys.path.append("..")
import shinythingscreds
credsdict=shinythingscreds.init(cloudenv)
sntableacctname=credsdict['tempalarmtablestorageaccountname']
sntableacctkey=credsdict['tempalarmtablestorageaccountkey']

temptable=credsdict['temptable']

###############################################################################
devstubs=True   #if not actually running on a pi

###############################################################################
from azure.cosmosdb.table.tableservice import TableService
tablesvc = TableService(account_name=sntableacctname, account_key=sntableacctkey)
###############################################################################

# Info on my specific sensors
if not devstubs:
    import Adafruit_DHT
    DHT_TYPE = Adafruit_DHT.DHT11
    DHT_PIN  = 4

def getsensordata(DHT_TYPE, DHT_PIN):
        #while True:
        if devstubs:
            return (20,50)
        else:
            humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
            #sometimes it sucks, particularly during high load. if at first you do not succeed...
            while humidity == None or temp == None:
                time.sleep(.5)
                humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
        return (temp, humidity)

def convceltofar(tempcel):
        return (tempcel*1.8)+32

def senddata(temp,hum):
    data={'PartitionKey': 'SBUX-LAB','RowKey': '123456789'}
    data['TempF']=temp
    data['Humidity']=hum
    data['ReadTime']=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    tablesvc.insert_or_replace_entity(temptable, data)
    print(data)


while True:
    print("getting data")
    (temp, hum)=getsensordata(11,4)
    senddata(convceltofar(temp),hum)
    time.sleep (1)
                
