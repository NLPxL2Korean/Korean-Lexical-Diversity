from data_processor import typodelete
from data_reader import read_texts_into_lists
import argparse
import logging
from ld_analyser import tokenize_n_make_ld_matrix
import warnings
import numpy as np
import pandas as pd
import sys

from util import current_time_as_str

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
logging.basicConfig(level=logging.INFO)
logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
logging.getLogger("stanza").setLevel(logging.WARNING)

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputdir", required=True,
                        help="Path to the directory which includes plain text files to be analysed")
    parser.add_argument("-t", "--tokenizer", nargs='+', default=["okt"],
                        help="Tokenizers: (okt, komoran, mecab, kkma, hannanum, stanza). You can give multiple tokenizers ex) -t kkma komoran")
    parser.add_argument("-a", "--all", action="store_true",
                        help="""Do analysis on all possible combinations on the given tokenizer sets (function word True & False x parallel analysis True & False)
                             Note that the argument functionwords=false is not provided in stanza.
                             Argument --functionwords and --parallel are ignored if -a set true """)
    parser.add_argument("-f", "--functionwords", action='store_true',
                        help="""Do analysis on both function and content words. If this argument not given, do analysis only on content words.
                                Note that functionwords=false in not provided in stanza. """)
    parser.add_argument("-p", "--parallel", action='store_true', help="do parallel analysis.")
    parser.add_argument("-o", "--outputdir", default='result', help="path to store output files (log, tsv files with ld values")
    parser.add_argument("-no-typo-removal", "--notyporemoval", action='store_true', help="Note: Windows OS with Microsoft Office is required for this function.")
    args = parser.parse_args()


    # set logger
    a_logger = logging.getLogger()
    a_logger.setLevel(logging.DEBUG)
    log_file = args.outputdir + '/' + "log_" + current_time_as_str() + ".log"
    output_file_handler = logging.FileHandler(log_file)
    a_logger.addHandler(output_file_handler)

    if "stanza" in args.tokenizer and not args.functionwords: # if the user wants to exclude functionwords in stanza
        if not args.all:
            raise ValueError("Stanza does not provide functionwords=False. Please give functionwords argument for stanza tokenizer by adding -f to the command")

    # configuration information (show as log)
    logging.info("-----------Configuration----------")
    logging.info("Selected Tokenizer = %s", args.tokenizer)
    if args.all:
        logging.info("Four different analysis will be done for the selected tokenizer(s)")
        logging.info("(functionword True, False) x (Parallel analysis True, False)")
    else:
        logging.info("Include Function Words = %s", args.functionwords)
        logging.info("Parallel Analysis = %s", args.parallel)
    if args.notyporemoval:
        logging.info("Typo removal function is off: No typos will be removed.")
    logging.info("----------------------------------")

    # read and process text

    if args.notyporemoval:
        txt_id, text_list = read_texts_into_lists(args.inputdir, remove_num=False)
        data_df = pd.DataFrame(index=txt_id, columns=['processed'])
        data_df['processed'] = text_list
    else:
        txt_id, text_list = read_texts_into_lists(args.inputdir)
        data_df = typodelete(txt_id, text_list, args.outputdir)

    # tokenize and analyse
    if args.all:
        f_options = [True, False]
        p_options = [True, False]
        for tokenizer in args.tokenizer:
            for f in f_options:
                for p in p_options:
                    config = "Tokenizer: {}, Include Function Words: {}, Parallel Analysis: {}".format(tokenizer, f, p)
                    logging.info("\n\n\n================ %s =================", config)
                    tokenize_n_make_ld_matrix(data=data_df, tokenizer=tokenizer,
                                              include_function_words=f,
                                              parallel_analysis=p, output_dir=args.outputdir)


    else:
        for tokenizer in args.tokenizer:
            logging.info("\n\n\n================ tokenizer %s =================", tokenizer)
            tokenize_n_make_ld_matrix(data=data_df, tokenizer=tokenizer,
                                      include_function_words=args.functionwords, parallel_analysis=args.parallel, output_dir=args.outputdir)

    logging.info("FINISHED")
