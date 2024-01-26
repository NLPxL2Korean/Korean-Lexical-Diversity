import logging

import win32com.client
import os
import codecs
import re
import pandas as pd
from util import current_time_as_str


def typodelete(txt_id, txt_list, output_dir, save=True):
    """
    Detect typo in a list of texts using MSword and delete the typos
    :param output_dir: str, output directory to save the processed text
    :param txt_id: unique id of texts
    :param txt_list: list of texts
    :param save: boolean, if True, save the result file to excel
    :return: df, which contains raw text, typos, and typo deleted text
    """

    logging.info("Processing the raw input: typo deletion . . .")
    # make df to store results
    df_column = ['raw', 'typo', 'processed']
    output_df = pd.DataFrame(index=txt_id, columns=df_column)

    # save the raw text into ms word form to use ms word typo corrector
    current_time = current_time_as_str()
    file_path = os.path.abspath(current_time + ".txt")
    # logging.info("Concatenating files into a single .txt . . .")
    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        index = 0
        for text in txt_list:
            index += 1
            f.write(text)
            if len(txt_list) > index:  # do not add \n at the end of the file
                f.write('\n')

    # open the ms word document
    msword = win32com.client.DispatchEx('Word.Application')
    # logging.info("Loading .txt into MS Word . . .")
    doc = msword.Documents.Open(file_path)
    assert int(doc.Paragraphs.Count) == len(txt_list)

    # for each text(Paragraph in word), detect error
    # logging.info("Processing text started . . .")
    for i, p in enumerate(doc.Paragraphs):  # process per text
        tab_removed_raw = re.sub("\t", " ", txt_list[i])  # remove all tabs to store the data as tsv file
        typos = p.Range.SpellingErrors
        item = []
        typo_list = []

        for typo in typos:  # make typo list
            typo_list.append(str(typo))

        # delete typos in text
        pattern = re.compile(r'\b(?:%s)\b' % '|'.join(typo_list))
        processed = re.sub(pattern, '', tab_removed_raw)

        item.append(tab_removed_raw)
        item.append(typo_list)
        item.append(processed)
        output_df.loc[txt_id[i]] = item

        assert "\t" not in tab_removed_raw, f"File {txt_id[i]} contains tab, Please remove all tabs in the file for generating tsv file. "

    # close and delete temporary files
    doc.Close(0)
    msword.Quit(0)
    os.remove(file_path)

    if save:
        file_path = output_dir + '/' + "processed_data" + ".tsv"
        logging.info("Saving processed text file as %s . . .", file_path)
        output_df.to_csv(file_path, encoding='utf-8', sep='\t')

    logging.info("Typo deletion completed")

    return output_df

