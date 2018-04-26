#import azure
import time

#%%
import sys
#import os
#import datetime
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
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    failgpio=12
    warngpio=16
    goodgpio=21
    stat2gpio={}
    stat2gpio['good']=goodgpio
    stat2gpio['fail']=failgpio
    stat2gpio['warn']=warngpio
    for pin in stat2gpio.values():
        GPIO.setup(pin,GPIO.OUT)


def getazuredata():
    #tempdata=tablesvc.query_entities(temptable, filter=filtertxt.format(device,querytime),select=querytxt.format(metric))
    data=tablesvc.query_entities(temptable,filter="PartitionKey eq 'SBUX-LAB'")
    temp=data.items[0]['TempF']
    return (temp)

def light(status):
    GPIO.output(stat2gpio[status],True)
    for key in stat2gpio.keys():
        if key != status:
            GPIO.output(stat2gpio[key],False)

def off():
    for key in stat2gpio.keys():
        GPIO.output(stat2gpio[key],False)

if not devstubs:
    while True:
        (temp,hum)=getazuredata()
        if temp > 105:
            status='fail'
        elif temp > 95:
            status='warm'
        elif temp <=85:
            status='good'
        light(status)
        time.sleep (1)
                
