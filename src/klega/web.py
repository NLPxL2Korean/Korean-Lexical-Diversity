"""
Author: Sooyeon Cho
LD Analyser class for KLEGA web application
"""
from collections import Counter
from klega.korean_tokenizer import tokenize, remove_function_words
from taaled import lexdiv


class LdAnalyser:
    def __init__(self, tokenizer, text):
        self.pos_with_frequency_content = None
        self.ldout_content = None
        self.tokens_cleaned_content = None
        self.pos_tuple_content = None
        self.pos_tuple_raw = None
        self.pos_with_frequency_all = None
        self.ldout_all = None
        self.tokens_cleaned_all = None
        self.pos_tuple_all = None
        self.tokenizer = tokenizer
        self.text = text



    def tokenize_text(self):
        # all
        self.pos_tuple_raw, self.pos_tuple_all, self.tokens_cleaned_all = tokenize(self.tokenizer, self.text)
        # content only
        self.pos_tuple_content, self.tokens_cleaned_content = remove_function_words(self.pos_tuple_all, self.tokenizer)

    def calculate_ld(self):
        # all
        self.ldout_all = lexdiv(self.tokens_cleaned_all).vald
        self.ldout_all = {key: round(self.ldout_all[key], 2) for key in self.ldout_all}
        # content only
        self.ldout_content = lexdiv(self.tokens_cleaned_content).vald
        self.ldout_content = {key: round(self.ldout_content[key], 2) for key in self.ldout_content}

    def calculate_frequency(self):
        # all
        self.pos_with_frequency_all = Counter(self.pos_tuple_all)
        self.pos_with_frequency_all = self.pos_with_frequency_all.most_common()  # sort by frequency
        # content only
        self.pos_with_frequency_content = Counter(self.pos_tuple_content)
        self.pos_with_frequency_content = self.pos_with_frequency_content.most_common()  # sort by frequency

    def ldanalyse(self):
        self.tokenize_text()
        self.calculate_ld()
        self.calculate_frequency()