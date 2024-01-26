from datetime import datetime


def current_time_as_str():
    """
    read current time and process it to string to be used in a file name.
    :return: str, current time value
    """
    dateNtime = str(datetime.now()).replace(" ", '')
    date = dateNtime[2:10].replace("-", "")
    time = dateNtime[10:-10].replace(":", "")

    return date + "_" + time


def flatten_list(txts):
    """
    flatten list of texts by concatenating
    :param txts: str, list of texts
    :return: str, flattened text as string
    """
    flatten = str()
    for txt in txts:
        flatten = flatten + txt
    return flatten
