#!/usr/bin/env python3.7

from serialInfo import serial_ports
import serial
import time

PortName = "/dev/ttyACM0"
SERIAL_BUFFER_SIZE = 64
READY_TO_READ = "Ready to read\n"
COMAND_ENDING_CONST = '\n'
SLEEP_TIME = 0.01
WAIT_FOR = 1000


def read_chunk(ser_port):
    try:
        received = None
        #handle no information relived problem

        while ser.inWaiting() > 0:
            received = ser.read(ser.inWaiting())
        if received:
            return received.decode(encoding='utf-8', errors='strict')
    except Exception as e:
        print(str(e))


def send_and_expect(serialPort, send, expect):
    """
        @brief send comand to controler
        @param send string to send to controler
        @param expect Wait for that response, set to None if no response needed.
        @return recived information during communications.
    """
    temp_log = ""
    serialPort.write(COMAND_ENDING_CONST.encode(encoding='utf-8'))
    
    waited_for_response = 0
    while temp_log.find(READY_TO_READ) == -1:
        time.sleep(SLEEP_TIME)
        temp_string = read_chunk(serialPort)
        if temp_string:
                temp_log += temp_string
        waited_for_response += 1
        if waited_for_response > WAIT_FOR:
            return temp_log

    serialPort.write(send.encode(encoding='utf-8'))

    if expect:
        while temp_log.find(expect) == -1:
            time.sleep(SLEEP_TIME)
            temp_string = read_chunk(serialPort)
            if temp_string:
                    temp_log += temp_string
            waited_for_response += 1
            if waited_for_response > WAIT_FOR:
                return temp_log


    return temp_log



try:
    #open port and make sure my program is running on the Arduino
    with serial.Serial(PortName, 9600, timeout=5) as ser:
        time.sleep(2)
        string = ""

        string += send_and_expect(ser, "atm\n1000\n", "1000\n")
        string += send_and_expect(ser, "42a\n", "42b\n")

        
        ser.flushInput()
        for _ in range(100):
            time.sleep(0.01)
            temp_string = read_chunk(ser)
            if temp_string:
                string += temp_string
    print(string, end="")
except Exception as e:
    print(str(e))
