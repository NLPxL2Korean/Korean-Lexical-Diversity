import os
import logging
from string import digits


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
        txt = txt.replace("\n", " ")
    return txt


def read_texts_into_lists(path, remove_num=True):
    """
    read all plain text files (.txt) in the path and return text id (file name) and text contents as list
    :param remove_num: bool, if set True, remove numbers in the text.
                        default is set True. (Processing numbers are not consistent for korean tokenizers, so remove nums beforehand.)
    :param path: str, directory to the input files
    :return: tuple (txt_id, text_list)
                where (txt_id) is a list of file names
                      (text_list) is a list of file contents as string
    """
    owd = os.getcwd()
    os.chdir(path)
    text_list = list()
    txt_id = list()
    for file in os.listdir():
        if file.endswith(".txt"):
            txt = read_text_file(file)
            if len(txt) < 1:
                logging.info("%s is empty file. Skipped", file)
                continue
            txt_id.append(file)
            txt = read_text_file(file)
            text_list.append(txt)

    os.chdir(owd)

    if remove_num:   # remove number
        text_list = [txt.translate(str.maketrans('', '', digits)) for txt in text_list]

    logging.info("%s files read successfully.", len(txt_id))

    return txt_id, text_list
