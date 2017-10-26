# -*- coding: utf-8 -*-

import os
import csv
# encoding=utf8
import sys
import re
import pandas as pd

input_file = './data/prothomalo_2017.csv'
output_file = './data/clean_sentences.txt'
min_sentence_length = 10



whitespace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+", re.UNICODE)
bangla_digits = u"[\u09E6\u09E7\u09E8\u09E9\u09EA\u09EB\u09EC\u09ED\u09EE\u09EF]+"
english_chars = u"[a-zA-Z0-9]"
punc = u"[(),$%^&*+={}\[\]:\"|\'\~`<>/,¦!?½£¶¼©⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞⅟↉¤¿º;-]+"
bangla_fullstop = u"\u0964"  # bangla fullstop(dari)
punctSeq = u"['\"“”‘’]+|[.?!—,…]+|[:;\n]+"


def clean_bangla_text(text):
    text = text.decode('utf-8')
    text = re.sub(bangla_digits, " ", text)     #remove bangla digits
    text = re.sub(punc, " ", text)
    text = re.sub(english_chars, " ", text)     #remove english chars
    #text = re.sub(bangla_fullstop, " ", text)  #keep fullstop(dari) to parse into sentences
    text = re.sub(punctSeq, " ", text)
    text = whitespace.sub(" ", text).strip()    #squeeze whitespaces()multiple whitespaces into one
    text = re.sub(u"\n","", text)       #remove newlines

    return text

sentences_file = open(output_file, 'w')

df = pd.read_csv(open(input_file), sep=",", iterator=True, error_bad_lines=False)

linecount = 0
for data in df:

    #cleaned_text = clean_bangla_text(data['NEWS'].decode('utf-8'))
    for news in data['NEWS']:
        cleaned_news = clean_bangla_text(str(news))

        for line in cleaned_news.split(bangla_fullstop):

            if len(line)>min_sentence_length:
                sentences_file.write((line+u'\n').encode('utf-8'))
                linecount += 1

sentences_file.close()
print "total line: "+str(linecount)

