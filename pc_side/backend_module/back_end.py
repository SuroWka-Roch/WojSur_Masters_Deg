import json
import csv
from numpy import average
import threading

from numpy import average

import backend_module.configuration

from backend_module.configuration import START_DATA
from backend_module.configuration import STOP_DATA
from backend_module.configuration import SLEEP_TIME, DEAMON_LOOP_COUNT, COMUNICATION_TIME_MS, REPEAT_FOR


import backend_module.comunication

import time

import serial


class CountRateData(object):
    """ 
        @brief class holding whole structure for count rate data. 
    """

    def __init__(self, canal_names, akw_time):
        """
            @param canal_names list names of output canals has to be the same that controler gives
            @param ak1000w_time Create new object when changing akw_time 
        """
        self.lock = threading.RLock()
        self.akw_time = akw_time
        self.dataDict = {}
        self.canal_names = canal_names
        self.nr_of_averages = 1
        self.vis_data_pointer = 0 #how much data from beginin not to visualise

        for name in canal_names:
            self.dataDict[name] = []  # create empty list for each canal

    def update(self, seperated_data):
        if type(seperated_data[0]) is not type(""):
            pass
        else:
            with self.lock:
                for string in seperated_data:
                    split_canal = string.split("\n")
                    try:
                        for canal_name, data in [(x.split("\t")[0], x.split("\t")[1]) for x in split_canal]:
                            if canal_name in self.canal_names:
                                self.dataDict[canal_name].append(int(data))
                    except IndexError as e:
                        print(str(e))
                        continue
                    except ValueError as e:
                        print(str(e))

    @staticmethod
    def seperate_data(string_log):
        """
            @brief cut data to string of singular mesuremant.
            @param string_log data to separate.
            @return array of strings.
        """
        seperated_data = []
        ending_len = len(STOP_DATA)+1
        starting_len = len(START_DATA)+1

        moving_pointer = 0
        chunk_end = 0
        while 1:
            moving_pointer = string_log.find(START_DATA, moving_pointer)
            chunk_end = string_log.find(STOP_DATA, moving_pointer)

            if moving_pointer == -1 or chunk_end == -1:
                break

            chunk_end += ending_len

            seperated_data.append(string_log[moving_pointer+starting_len+1:
                                             chunk_end-ending_len-1])
            moving_pointer = chunk_end - starting_len
        return seperated_data, moving_pointer

    def JSON_dump_to(self, file_name):
        with self.lock:
            with open(file_name, "a") as JsonDumpFile:
                json.dump(self.dataDict, JsonDumpFile)

    def CSV_dump_to(self, file_name):
        with self.lock:
            with open(file_name, 'a') as CSV_dump_file:
                writer = csv.writer(CSV_dump_file)
                writer.writerow(self.canal_names)
                for len in range(self._shortest()):
                    line = [self.dataDict[key][len]
                            for key in self.canal_names]
                    writer.writerow(line)

    def data_for_plot(self):
        #@breief Returns data prepared for ploting
        len = self._shortest() - self.vis_data_pointer

        if self.akw_time == None or len < self.nr_of_averages:
            return None, None, None

        time_per_step = self.akw_time * 2 + COMUNICATION_TIME_MS

        if self.nr_of_averages == 1:
            x = [x * time_per_step * 0.001 for x in range(-len+1, 1)]
            y = []
            with self.lock:
                for canal in self.canal_names:
                    y.append([x/(self.akw_time/1000)
                              for x in self.dataDict[canal][-(len):]])

            return self.canal_names, x, y
        else:
            len = len // self.nr_of_averages
            x = [x * time_per_step * 0.001 *
                 self.nr_of_averages for x in range(-len+1, 1)]
            y = []
            with self.lock:
                for canal in self.canal_names:
                    canal_y = []
                    for canal_y_nr in range(len):
                        canal_y.append(sum(
                            self.dataDict[canal][canal_y_nr*self.nr_of_averages:(canal_y_nr+1)*self.nr_of_averages])/self.nr_of_averages)
                    y.append([val / (self.akw_time/1000) for val in canal_y])
            return self.canal_names, x, y

    def _shortest(self):
        short = min([len(self.dataDict[key]) for key in self.dataDict.keys()])
        return short

    def set_vis_to_now(self):
        with self.lock:
            self.vis_data_pointer = self._shortest() 

    def change_nr_of_averages(self, new_number):
        with self.lock:
            self.nr_of_averages = new_number

    def last_values(self):
        if self.nr_of_averages > self._shortest():
            return [-1 for _ in range(16)]

        with self.lock:
            try:
                values = [average(self.dataDict[key][-(self.nr_of_averages):]) /
                          (self.akw_time/1000) for key in self.canal_names]
                return values
            except IndexError as e:
                return [-1 for _ in range(16)]
            except TypeError as e:
                return [-1 for _ in range(16)]

    def clear(self, file_name="exit_data"):
        with self.lock:
            self.dataDict = {}
            for name in self.canal_names:
                self.dataDict[name] = []  # create empty list for each canal

    def set_akw_time(self, time):
        with self.lock:
            self.akw_time = time

    def is_empty(self):
        with self.lock:
            if self._shortest() == 0:
                return True
            else:
                return False

    def __getitem__(self, item):
        return self.dataDict[item]

    def __str__(self):
        return(str(self.dataDict))


class CountRateDataSingleShoot(CountRateData):

    def ready(self):
        for value in self.dataDict.values():
            if not value:
                break
        else:
            return True

        return False

    def data_for_plot(self):
        y = []
        with self.lock:
            for canal_name in self.canal_names:
                y.append((self.dataDict[canal_name]
                          [-1] / (self.akw_time / 1000)))

        return y


class ConfigurationData(object):
    """
    Holds configuration data
    keys in dictionary:
    akw_time, nr_of_averages, save_period, save_location, save_type, port_name, low_rate, ENBLR
    """

    def __init__(self, akw_time, nr_of_averages, save_period, save_location, save_type, port_name, low_rate, ENBLR):
        self.empty = False
        self.data = {}
        self.data["akw_time"] = akw_time
        self.data["nr_of_averages"] = nr_of_averages
        self.data["save_period"] = save_period  # in secends
        self.data["save_location"] = save_location
        self.data["save_type"] = save_type
        self.data["port_name"] = port_name
        self.data["vis_log_scale"] = False
        self.data["low_rate"] = 0 if low_rate == "Low" else 1
        self.data["ENBLR"] = 0 if ENBLR == "Low" else 1

    @staticmethod
    def create_empty():
        temp_obj = ConfigurationData(0, 0, 0, 0, 0, 0, 0, 0)
        temp_obj.empty = True
        return temp_obj

    def update_and_drop_diferances(self, next_iteration):
        self.empty = False
        differences = []
        for key in self.data:
            if not self.data[key] == next_iteration.data[key]:
                differences.append(key)
                self.data[key] = next_iteration.data[key]
        return differences

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        return(str(self.data))


class rawLogClass():
    def __init__(self):
        self.log_string = ""
        self.new_info_pointer = 0
        self.lock = threading.RLock()

    def write(self, msg):
        self.lock.acquire()
        self.log_string += msg
        self.lock.release()

    def set_pointer(self, new_place):
        with self.lock:
            self.new_info_pointer = new_place

    def return_chunk(self):
        temp_string = None
        self.lock.acquire()
        temp_string = self.log_string[self.new_info_pointer:]
        self.new_info_pointer = len(self.log_string)
        self.lock.release()
        return temp_string

    def __str__(self):
        return self.log_string

#############################################
#functions


def back_end_deamon(count_rate_data, semaphore, log, serial_port):
    while True:
        time.sleep(SLEEP_TIME)
        if serial_port.is_open:
            string = ""
            for _ in range(DEAMON_LOOP_COUNT):
                with semaphore:
                    time.sleep(SLEEP_TIME)
                    temp_string = backend_module.comunication.read_chunk(
                        serial_port)
                    if temp_string:
                        string += temp_string
            log.write(string)


def update_count_data(count_data, log):
    log_chunk = log.return_chunk()
    data, end_pointer = CountRateData.seperate_data(log_chunk)
    if data:
        count_data.update(data)
        log.set_pointer(end_pointer)


def get_ss_mesurement(serial_port, port_semaphore, log, ss_count_data):
    with port_semaphore:
        repeat(lambda:
               backend_module.comunication.set_akw_time(serial_port, ss_count_data.akw_time, log))
        repeat(lambda:
               backend_module.comunication.start(serial_port, log))
        while not ss_count_data.ready():
            time.sleep(SLEEP_TIME)
            if serial_port.is_open:
                string = ""
                for _ in range(DEAMON_LOOP_COUNT):
                    time.sleep(SLEEP_TIME)
                    temp_string = backend_module.comunication.read_chunk(
                        serial_port)
                    if temp_string:
                        string += temp_string
                log.write(string)
            update_count_data(ss_count_data, log)
        repeat(lambda:
               backend_module.comunication.stop(serial_port, log, no_expected=True))


def repeat(fun, times=REPEAT_FOR):
    e = None
    for _ in range(times):
        try:
            fun()
            return
        except CommunicationError as er:
            e = er
    else:
        raise e


##########################################
#Exceptions


class CommunicationError(Exception):
    def __init__(self, arg):
        self.value = arg

    def __str__(self):
        return(str(self.value))


class NoReadyToResponse(CommunicationError):
    def __init__(self, arg):
        self.value = arg

    def __str__(self):
        return(str(self.value))


class ExpectedResponseNotFound(CommunicationError):
    def __init__(self, arg):
        self.value = arg

    def __str__(self):
        return(str(self.value))
