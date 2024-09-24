import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor
import adafruit_dht
import board
import time
import os
import random
from datetime import datetime

dht_device = adafruit_dht.DHT11(board.D16)
ultrasonic = DistanceSensor(echo =  6, trigger = 5)


TempList = []
DisList = []


broker_url = "50c69f01d2b349de8f734066b3b5a261.s1.eu.hivemq.cloud"  
broker_port = 8883  


topic2 = "DHT"  

client = mqtt.Client()


client.username_pw_set("Test1", "Test1234")


client.tls_set()
client.connect(broker_url, broker_port)


try :
    while True:

#        print("Temp")
        temperature_c = dht_device.temperature
        distance = ultrasonic.distance
        
        message1 = distance * 100
        message2 = temperature_c
        
#        print("Published")
        client.publish(topic1, message1,qos=1)
        client.publish(topic2, message2,qos=1)
        
#        print("Temp#2")
#        TempList.append(temperature_c)
#       DisList.append(distance)
        
        print(f"Temperature: {temperature_c}\u00b0C")
        print(f"Distance : {distance} cm")
        
        
        #print(f"Message '{message1}' published to topic '{topic1}' on broker '{broker_url}'")
        print(f"Message '{message2}' published to topic '{topic2}' on broker '{broker_url}'")
        
        
       client.loop_forever()
#        print("Sleep")
        time.sleep(10)

except KeyboardInterrupt:
    print("Done")