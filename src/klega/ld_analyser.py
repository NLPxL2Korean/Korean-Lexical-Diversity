from korean_tokenizer import tokenize, remove_function_words
from taaled import parallel, lexdiv
import logging
from util import current_time_as_str


def tokenize_n_make_ld_matrix(data, tokenizer, include_function_words, parallel_analysis, output_dir, mx=200):
    """
    Tokenize and calculate all files in the df data and write output as tsv
    (This code includes partial modification of TAALED package source code)
    :param output_dir: str, output directory to store result files
    :param data: df, dataframe with three columns: text id, raw text, processed (typo removed) text, where df index is text file name
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum, stanza)
    :param include_function_words: bool
                                    if set True: tokenize content + function words
                                    if set False: tokenize only content words
    :param parallel_analysis: bool
                        if set True: do parallel analysis
                        if set False: no parallel analysis
    :param mx: int, minimum length of a text for parallel analysis
    :return: none
    """

    # filter out stanza with include_function_words=False
    if tokenizer == 'stanza' and not include_function_words:
        return

    logging.info("Start LD analysis . . .")
    # indexes
    loi = ["ntokens", "ntypes", "mtld", "mtldo", "mattr", "ttr", "rttr", "lttr", "maas", "msttr", "hdd"]

    # set file name
    if include_function_words:
        file_name = output_dir + "/" + tokenizer + "_all_words.tsv"
        if parallel_analysis:
            file_name = output_dir + "/" + tokenizer + "_all_words_prll.tsv"
    else:
        file_name = output_dir + "/" + tokenizer + "_content_only.tsv"
        if parallel_analysis:
            file_name = output_dir + "/" + tokenizer + "_content_only_prll.tsv"

    outf = open(file_name, "w", encoding='utf-8')
    if parallel_analysis:
        outf.write("filename" + '\t' + "length" + '\t' + '\t'.join(loi))
    else:
        outf.write("filename" + '\t' + '\t'.join(loi))

    text_id = data.index
    text_processed = data['processed']
    skipped = 0
    skippedl = []

    for i, text in enumerate(text_processed):
        _, pos_tuple, tokens_cleaned = tokenize(tokenizer, text)
        if not include_function_words:
            _, tokens_cleaned = remove_function_words(pos_tuple, tokenizer)
        if len(tokens_cleaned) < 1:  # nothing to analysis
            logging.info("%s has no analysable tokens. Skipping", text_id[i])
            skipped += 1
            skippedl.append(text_id[i])
            continue
        if parallel_analysis:
            if len(tokens_cleaned) < mx:  # in case the text is too short for parallel analysis
                skipped += 1
                skippedl.append(text_id[i])
                continue
            ld_lists = parallel(text=tokens_cleaned, clss=True, functd=None, funct=lexdiv, loi=loi, mx=mx).ldvals
            for length in ld_lists:  # iterate through text slices
                outl = [text_id[i], str(length)]  # list of items to write, will add each index below
                for index in loi:  # iterate through index list:
                    outl.append(str(ld_lists[length][index]))  # add index to outr list (in same order as loi list)
                outf.write("\n" + '\t'.join(outl))  # write row to file
        else:  # no parallel analysis
            ldout = lexdiv(tokens_cleaned).vald  # get dictionary version of lexical diversity output
            outl = [text_id[i]]  # list of items to write, will add each index below
            for index in loi:  # iterate through index list:
                outl.append(str(ldout[index]))  # add index to outr list (in same order as loi list)
            outf.write("\n" + '\t'.join(outl))  # write row to file

    outf.flush()
    outf.close()

    logging.info("Analysis on %s files completed successfully", len(text_id) - skipped)
    logging.info("The result is saved as: %s", file_name)

    if skipped:
        logging.info("%s files are skipped due to length problem", skipped)
        logging.info("List of skipped files: ")
        logging.info("%s", skippedl)
