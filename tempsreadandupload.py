import Adafruit_DHT
import azure
import time


# Info on my specific sensors
DHT_TYPE = Adafruit_DHT.DHT11
DHT_PIN  = 4

def getdata(DHT_TYPE, DHT_PIN):
#	while True:
	humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
		#sometimes it sucks, particularly during high load. if at first you do not succeed...
#		if humidity == None or temp == None:
#			time.sleep(5)
#			continue
	return (temp, humidity)

def convceltofar(tempcel):
	return (tempcel*1.8)+32

while True:
        print("getting data")
        (tempreading, humidityreading)=getdata(11,4)
        print("temperature is:",tempreading)
        print("humidity is:",humidityreading)
        if humidityreading == None or tempreading == None:
                print ("since temp and humidity were blank, will sleep and try again")
                time.sleep(2)
                continue
        else:
                print("this would be me uploading to the azures")
                print("temperature to upload:",convceltofar(tempreading))
                print("humidity to upload:",humidityreading)
                break
                
