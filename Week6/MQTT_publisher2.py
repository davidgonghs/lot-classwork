import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io"

client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    randNumber = randrange(10)
    client.publish("David", randNumber)
    print("Just published " + str(randNumber) + " to topic David")
    time.sleep(1)