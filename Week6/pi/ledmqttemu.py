import paho.mqtt.client as mqtt
from EmulatorGUI import GPIO

def on_connect(client, flag, userdata, rc):
    print ("Connected with rc: " + str(rc))
    client.subscribe("davidb1146/demo/led")

def on_message(client, userdata, msg):
    print ("Topic: "+ msg.topic+"\nMessage: "+str(msg.payload))
    if b"up" in msg.payload:
        print("Light on!")
        GPIO.output(11, GPIO.HIGH)
    else:
        print("Light off!")
        GPIO.output(11, GPIO.LOW)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)


client.loop_forever()
