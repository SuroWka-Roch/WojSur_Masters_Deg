#!/usr/bin/env python3.7

from serialInfo import serial_ports
import serial
import time

PortName = "/dev/ttyACM0"

try:
    #open port and make sure my program is running on the Arduino
    with serial.Serial(PortName, 9600, timeout=3) as ser:
        time.sleep(2)
        #handle no information relived problem
        while 1:
            received = ser.read(1)
            while received == b'':
                received = ser.read(1)
                time.sleep(0.1)
            print(received.decode(encoding='utf-8',errors='strict'),end='')
            
except Exception as e:
    print(str(e))