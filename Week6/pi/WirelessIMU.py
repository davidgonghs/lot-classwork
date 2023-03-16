import socket, traceback
from EmulatorGUI import GPIO
import time

#Define GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

#set host IP address
#host = '192.168.1.220'
host = '172.20.10.5'
#port number 
port = 5555

#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Associates a socket with a local endpoint 
s.bind((host, port))

while 1:
    try:
        #receive message from phone 
	#recvform(the number of bytes to be read from the UDP socket) 
        message, address = s.recvfrom(1024)
        #print message
        print ("---------------------------------")

        var1=str(message)
        var2=var1.split(",")
        temp2=var2[2].strip(",")
        #print temp2
        temp3=float(temp2)
        print (temp3)

        #Control LED
        if temp3>0:
            print ("LED ON")
            GPIO.output(18, GPIO.HIGH)
        elif temp3<0:
            print ("LED OFF")
            GPIO.output(18,GPIO.LOW)
        else:
            print ("------")


    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
