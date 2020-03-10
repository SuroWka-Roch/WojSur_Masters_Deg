START_DATA = "<~+~>"
STOP_DATA = "~<+>~"


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

        if moving_pointer == -1:
            break

        chunk_end = string_log.find(STOP_DATA,moving_pointer)
        chunk_end += ending_len

        seperated_data.append(string_log[moving_pointer+starting_len :
                                                 chunk_end-ending_len])
        moving_pointer = chunk_end
    return seperated_data

#TODO get information from seperated chunks 
