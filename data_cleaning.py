# -*- coding: utf-8 -*-

import os
import csv
# encoding=utf8
import sys
import re
import pandas as pd

df = pd.read_csv(open('./data/ProthomAlo_2017-06-01_2017-06-05.csv'),
                     sep=",",
                     iterator=True)


whitespace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+", re.UNICODE)
bangla_digits = u"[\u09E6\u09E7\u09E8\u09E9\u09EA\u09EB\u09EC\u09ED\u09EE\u09EF]+"
english_chars = u"[a-zA-Z0-9]"
punc = u"[(),$%^&*+={}\[\]:\"|\'\~`<>/,¦!?½£¶¼©⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞⅟↉¤¿º;-]+"
bangla_fullstop = u"\u0964"     #bangla fullstop(dari)
punctSeq   = u"['\"“”‘’]+|[.?!,…]+|[:;]+"

def clean_bangla_text(text):
    text = re.sub(bangla_digits, " ", text)
    text = re.sub(punc, " ", text)
    text = re.sub(english_chars, " ", text)
    text = re.sub(bangla_fullstop, " ", text)
    text = re.sub(punctSeq, " ", text)
    text = whitespace.sub(" ", text).strip()
    
    return text

for data in df:
    cleaned_text = clean_bangla_text(data['NEWS'][0].decode('utf-8'))
    print cleaned_text


