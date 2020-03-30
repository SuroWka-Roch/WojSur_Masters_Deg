#!/usr/bin/env python3.7


from backend_module.serialInfo import serial_ports
import backend_module.back_end as back_end
import serial
import time
import re

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

        while ser_port.inWaiting() > 0:
            received = ser_port.read(ser_port.inWaiting())
        if received:
            return received.decode(encoding='utf-8', errors='strict')
    except Exception as e:
        print( "read error at read_chunk with code of: " + str(e))


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
    reg = re.compile(READY_TO_READ)
    while not reg.search(temp_log):
        time.sleep(SLEEP_TIME)
        temp_string = read_chunk(serialPort)
        if temp_string:
            temp_log += temp_string
        waited_for_response += 1
        if waited_for_response > WAIT_FOR:
            raise back_end.NoReadyToResponse("No 'Ready to read' response")

    serialPort.write(send.encode(encoding='utf-8'))

    if expect:
        waited_for_response = 0
        reg = re.compile(expect)
        while not reg.search(temp_log):
            time.sleep(SLEEP_TIME)
            temp_string = read_chunk(serialPort)
            if temp_string:
                temp_log += temp_string
            waited_for_response += 1
            if waited_for_response > WAIT_FOR:
                raise back_end.ExpectedResponseNotFound("No response")


    return temp_log


def test(database, akw_time):
    try:
        #open port and make sure my program is running on the Arduino
        with serial.Serial(PortName, 9600, timeout=5) as ser:
            time.sleep(2)
            string = ""


            string += send_and_expect(ser, "srt\n", None)
            string += send_and_expect(ser, "atm\n"+ str(akw_time) +"\n", str(akw_time) + "\n")
            string += send_and_expect(ser, "42a\n", "42b\n")

            
            for _ in range(100):
                time.sleep(SLEEP_TIME)
                temp_string = read_chunk(ser)
                if temp_string:
                    string += temp_string
        seperated = back_end.CountRateData.seperate_data(string)
        database.update(seperated)
    except Exception as e:
        print('Caught Exeption of class "{}" with message of "{}"'.format(type(e),str(e)))


def high_test():
    akw_time = 10
    back_end_data = back_end.CountRateData(back_end.CANAL_NAMES, akw_time)
    for _ in range(3):
        test(back_end_data, akw_time)
    print(back_end_data)

if __name__ == "__main__":
    print("Running back end module independenty")