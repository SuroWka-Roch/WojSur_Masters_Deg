#!/usr/bin/env python3.7


from backend_module.serialInfo import serial_ports
import backend_module.back_end as back_end
import serial
import time
import re

from backend_module.back_end import rawLogClass, ConfigurationData

import backend_module.configuration

from backend_module.configuration import WAIT_AFTER_OPENING_PORT
from backend_module.configuration import READY_TO_READ
from backend_module.configuration import HANSHAKE_CONFIRM_REQUEST_CODE
from backend_module.configuration import HANSHAKE_CONFIRMATION_CODE
from backend_module.configuration import AKW_TIME_MS_CODE
from backend_module.configuration import CODE_STOPED_RESPONSE
from backend_module.configuration import COMAND_ENDING_CONST
from backend_module.configuration import SERIAL_BUFFER_SIZE
from backend_module.configuration import WAIT_FOR
from backend_module.configuration import SLEEP_TIME
from backend_module.configuration import SERIAL_SPEED
from backend_module.configuration import START_CODE, STOP_CODE


def read_chunk(ser_port):
    try:
        received = None
        #handle no information relived problem

        while ser_port.inWaiting() > 0:
            received = ser_port.read(ser_port.inWaiting())
        if received:
            return received.decode(encoding='utf-8', errors='strict')
    except Exception as e:
        print("read error at read_chunk with code of: " + str(e))


def send_and_expect(serialPort, send, expect):
    """
        @brief send comand to controler
        @param send string to send to controler
        @param expect Wait for that response, set to None if no response needed.
        @return recived information during communications.
    """
    temp_log = ""
    serialPort.write(COMAND_ENDING_CONST.encode(encoding='utf-8'))

    send += COMAND_ENDING_CONST
    expect += COMAND_ENDING_CONST

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
                print("log = {}".format(temp_log))      
                raise back_end.ExpectedResponseNotFound("No response")
    return temp_log


def test(database, akw_time):
    try:
        #open port and make sure my program is running on the Arduino
        with serial.Serial(PortName, 9600, timeout=5) as ser:
            time.sleep(2)
            string = ""

            string += send_and_expect(ser, "srt", None)
            string += send_and_expect(ser, "atm\n" +
                                      str(akw_time), str(akw_time))
            string += send_and_expect(ser, "42a", "42b")

            for _ in range(100):
                time.sleep(SLEEP_TIME)
                temp_string = read_chunk(ser)
                if temp_string:
                    string += temp_string
        seperated = back_end.CountRateData.seperate_data(string)
        database.update(seperated)
    except Exception as e:
        print('Caught Exeption of class "{}" with message of "{}"'.format(
            type(e), str(e)))


def high_test():
    akw_time = 10
    back_end_data = back_end.CountRateData(
        backend_module.back_end.CANAL_NAMES, akw_time)
    for _ in range(3):
        test(back_end_data, akw_time)
    print(back_end_data)


def try_port(Port_name, SerialObject):
    """
    Throws SerialException and CommunicationError
    """
    SerialObject.port = Port_name
    SerialObject.timeout = 5
    SerialObject.baudrate = SERIAL_SPEED
    

    try:
        if not SerialObject.is_open:
            SerialObject.open()

        time.sleep(WAIT_AFTER_OPENING_PORT)
        send_and_expect(SerialObject, HANSHAKE_CONFIRM_REQUEST_CODE,
                        HANSHAKE_CONFIRMATION_CODE)
    except Exception as e:
        print(type(e))
        raise e
        


def configure_all(serial_port, configuration, log):
    if not serial_port.is_open:
        serial_port.open()

    log.write(send_and_expect(serial_port, AKW_TIME_MS_CODE + '\n' + 
                              str(configuration["akw_time"]), str(configuration["akw_time"])))

def start(serial_port,log):
    log.write(send_and_expect(serial_port, START_CODE
                              , None))

def stop(serial_port, log):
    log.write(send_and_expect(serial_port, STOP_CODE, CODE_STOPED_RESPONSE))
if __name__ == "__main__":
    pass
