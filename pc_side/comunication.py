#!/usr/bin/env python3.7

from serialInfo import serial_ports
import serial
import time

PortName = "/dev/ttyACM0"



def read_chunk(ser_port):
    try:
        received = None
        #handle no information relived problem
        bytes_waiting = ser.inWaiting()

        while bytes_waiting > 0:
            received = ser.read(bytes_waiting)
        if received:
            return received.decode(encoding='utf-8', errors='strict')
    except Exception as e:
        print(str(e))


try:
    #open port and make sure my program is running on the Arduino
    with serial.Serial(PortName, 9600, timeout=5) as ser:
        time.sleep(2)
        string = ""
        ser.flushInput()
        for _ in range(50):
            time.sleep(0.1)
            temp_string = read_chunk(ser)
            print(temp_string)  
            if temp_string:
                string += temp_string
    print(string,end="")
except Exception as e:
    print(str(e))
