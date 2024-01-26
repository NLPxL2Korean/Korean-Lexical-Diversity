from konlpy.tag import Okt, Komoran, Kkma, Hannanum

try:
    import mecab_ko as MeCab
except:
    print("mecab_ko is not installed. If you want to use the mecab tokenizer, please install the package.")
    pass

try:
    import stanza
except:
    print("stanza is not installed. If you want to use the stanza tokenizer, please install the package.")
    pass

OKT_STOPWORDS = ["Punctuation", "Foreign", "Alpha", "Number", "Unknown", "KoreanParticle", "Hashtag", "ScreenName",
                 "Email", "URL"]
KOMORAN_STOPWORDS = ["SF", "SE", "SS", "SP", "SO", "SW", "SH", "SL", "SN", "NF", "NV", "NA"]

MECAB_STOPWORDS = ["SF", "SE", "SSO", "SSC", "SC", "SY", "SH", "SL", "SN"]

KKMA_STOPWORDS = ["SF", "SE", "SS", "SP", "SO", "SW", "OH", "OL", "ON", "UN"]

HANNANUM_STOPWORDS = ['S', 'F']

STANZA_STOPWORDS = ['PUNCT', 'SYM', 'X']

OKT_FUNCTIONWORDS = ["Josa", "PreEomi", "Eomi", "Suffix"]

KOMORAN_FUNCTIONWORDS = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JC", "JX", "EP", "EF", "EC", "ETN", "ETM",
                         "XPN", "XSN", "XSV", "XSA"]

MECAB_FUNCTIONWORDS = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JC", "JX", "EP", "EF", "EC", "ETN", "ETM",
                       "XPN", "XSN", "XSV", "XSA"]

KKMA_FUNCTIONWORDS = ["JKS", "JKC", "JKG", "JKO", "JKM", "JKI", "JKQ", "JC", "JX", "EPH", "EPT", "EPP", "EFN", "EFQ",
                      "EFO", "EFA", "EFI", "EFR", "ECE", "ECS", "ECD", "ETN", "ETD", "XPN", "XPV", "XSN", "XSV", "XSA"]

HANNANUM_FUNCTIONWORDS = ["J", "E", "X"]


def remove_pos(token_pos_tuple, pos_list):
    """
    Remove given POSs in the tokenized tuple
    :param token_pos_tuple: list of tuple consisting of token and POS [('열심히', 'Adverb'), ('코딩', 'Noun')...]
    :param pos_list: list of POS to be removed
    :return: cleaned tuple of ('token', 'Part-Of-Speech') as list
    """
    pos_tuple_cleaned = []

    for index, pair in enumerate(token_pos_tuple):
        if pair[1] not in pos_list:
            pos_tuple_cleaned.append(pair)

    return pos_tuple_cleaned


def tokenize(tokenizer, text):
    """
    tokenize sequences using konlpy tokenizer.
    :param tokenizer: str, possible options: (okt, komoran, mecab, kkma, hannanum, stanza)
    :param text: str, raw text
    :return: tuple (pos_tuple_all, pos_tuple_cleaned, tokens_cleaned)
            where pos_tuple_all consists of tuple ('token', 'Part-Of-Speech') of all raw tokens (including stopwords like punctuation, numbers, URL ...)
                  pos_tuple_cleaned consists of tuple ('token', 'Part-Of-Speech') of contents words (+ function words if the param include_function_words=True)
                  tokens_cleaned is a list of stopword removed tokens (if the param include_function_words=True, function words are also included)
    """

    if tokenizer == 'okt':
        tagger = Okt()
        stopwords = OKT_STOPWORDS
    elif tokenizer == 'komoran':
        tagger = Komoran()
        stopwords = KOMORAN_STOPWORDS
    elif tokenizer == 'mecab':
        tagger = MeCab.Tagger()
        stopwords = MECAB_STOPWORDS
    elif tokenizer == 'kkma':
        tagger = Kkma()
        stopwords = KKMA_STOPWORDS
    elif tokenizer == 'hannanum':
        tagger = Hannanum()
        stopwords = HANNANUM_STOPWORDS
    elif tokenizer == 'stanza':
        tagger = stanza.Pipeline('ko', processors='tokenize,pos', package='gsd')
        stopwords = STANZA_STOPWORDS
    else:
        raise ValueError("tokenizer must be one of these options: (okt, komoran, mecab, kkma, hannanum, stanza)")

    # tokenize
    if tokenizer == 'stanza':
        doc = tagger(text)
        pos_tuple_all = [(word.text, word.upos) for sent in doc.sentences for word in sent.words]
    elif tokenizer == 'mecab':
        tmp_mecab = tagger.parse(text)
        tmp_mecab = tmp_mecab.split("\n")
        tmp_mecab = tmp_mecab[:-2] # mecab_ko has an [EOS] symbol. remove this
        tmp_mecab = [item.split("\t") for item in tmp_mecab]
        pos_tuple_all = [(item[0], item[1].split(",")[0]) for item in tmp_mecab]
    else:
        pos_tuple_all = tagger.pos(text)

    # remove stopwords
    pos_tuple_cleaned = remove_pos(pos_tuple_all, pos_list=stopwords)

    # separate lists for tokens
    tokens_cleaned = [item[0] for item in pos_tuple_cleaned]

    return pos_tuple_all, pos_tuple_cleaned, tokens_cleaned


def remove_function_words(pos_tuple, tokenizer):
    """
    Remove function words from tokenized pos tuple
    include this if main argument functionwords=False
    :param pos_tuple: ('token', 'Part-Of-Speech')
    :param tokenizer: str, available options: okt, komoran, mecab, kkma, hannanum
    :return:
    """

    functionwords = []

    if tokenizer == 'okt':
        functionwords = OKT_FUNCTIONWORDS
    elif tokenizer == 'komoran':
        functionwords = KOMORAN_FUNCTIONWORDS
    elif tokenizer == 'mecab':
        functionwords = MECAB_FUNCTIONWORDS
    elif tokenizer == 'kkma':
        functionwords = KKMA_FUNCTIONWORDS
    elif tokenizer == 'hannanum':
        functionwords = HANNANUM_FUNCTIONWORDS

    pos_tuple_cleaned = remove_pos(pos_tuple, pos_list=functionwords)

    # separate lists for tokens
    tokens_cleaned = [item[0] for item in pos_tuple_cleaned]

    return pos_tuple_cleaned, tokens_cleaned
