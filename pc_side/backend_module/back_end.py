import json
from numpy import average

START_DATA = "<~+~>"
STOP_DATA = "~<+>~"

CANAL_NAMES = ["1A1","1A2","1A3","1A4","1A5","1A6","1A7","1A8","2A1","2A2","2A3","2A4","2A5","2A6","2A7","2A8"]

class CountRateData:
    """ 
        @brief class holding whole structure for count rate data. 
    """

    def __init__(self, canal_names, akw_time):
        """
            @param canal_names list names of output canals has to be the same that controler gives
            @param akw_time Create new object when changing akw_time 
        """
        self.akw_time = akw_time
        self.dataDict = {}
        self.canal_names = canal_names
        self.nr_of_averages = 5

        for name in canal_names:
            self.dataDict[name] = [] #create empty list for each canal

    def update(self, seperated_data):
        if type(seperated_data[0]) is not type(""):
            pass
        else:
            for string in seperated_data:
                split_canal = string.split("\n")
                try:
                    for canal_name, data in [(x.split("\t")[0],x.split("\t")[1]) for x in split_canal]:
                        if canal_name in self.canal_names:
                            self.dataDict[canal_name].append( int(data) )
                except IndexError as e:
                    print(str(e))
                    continue

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
            chunk_end = string_log.find(STOP_DATA,moving_pointer)

            if moving_pointer == -1 or chunk_end == -1:
                break

            chunk_end += ending_len

            seperated_data.append(string_log[moving_pointer+starting_len+1 :
                                                    chunk_end-ending_len-1])
            moving_pointer = chunk_end
        return seperated_data

    def dump_to(self, file_name):
        with open(file_name,"a") as JsonDumpFile:
            json.dump(self.dataDict, JsonDumpFile)

    def data_for_plot(self):
        y = []
        for canal_name in self.canal_names:
            data_len = self.nr_of_averages if len(self.dataDict[canal_name]) > self.nr_of_averages else len(self.dataDict[canal_name])
            y.append( average( self.dataDict[canal_name][-data_len:] ))
            

        return self.canal_names, y

    def change_nr_of_averages(self, new_number):
        self.nr_of_averages = new_number

    

    def __str__(self):
        return( str(self.dataDict) )
    

##########################################
#Exceptions


class CommunicationError(Exception):
    def __init__(self, arg):
        self.value = arg

    def __str__(self): 
        return( str(self.value)) 

class NoReadyToResponse(CommunicationError):
    def __init__(self, arg):
        self.value = arg

    def __str__(self): 
        return( str(self.value)) 

class ExpectedResponseNotFound(CommunicationError):
    def __init__(self, arg):
        self.value = arg

    def __str__(self): 
        return( str(self.value)) 



