# MQTT How to use
## Install
### Install Mosquitto
```pip install paho-mqtt```
### then following the code
### Download the MQTT Dashboard app on your phone
#### 1.create a brokers
#### 2.set Broker name: LED
#### 3.set Broker address: tcp://test.mosquitto.org
#### 4.set Broker port: 1883
#### 5.save
#### 6.create a new Button
#### 7.set Button name: up
#### 8.set Button topic as your code subscribe topic 
    for example: /LED/UP or davidb1146/demo/led
#### 9.set Button payload: up
#### 10.save
#### 11.create a new Button same as before but call off

### run the code use python
```python ledmqttemu.py```
### then you can use the MQTT Dashboard app to control the LED

