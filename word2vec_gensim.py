#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim

inp_file = './data/clean_sentences.txt'
out_file = './data/saved_model.bin'

'''
corpus_file = open(inp_file, 'r')
raw_sentences = corpus_file.readlines()

sentences = []  #list of words of sentences
for sentence in raw_sentences:
    sentences.append(sentence.split())
word = 0
for sent in sentences:
    word += len(sent)
print "total words: ",word

bigram_transformer = gensim.models.Phrases(sentences,threshold=100.0)
bi_phrase = bigram_transformer[sentences]   #phrases with two words

model = gensim.models.Word2Vec(bi_phrase, window=1, min_count=10, workers=4, iter=20)

#model = gensim.models.Word2Vec(sentences)
model.save(out_file)



'''
#test model

model = gensim.models.Word2Vec.load(out_file)

words = model.wv.most_similar(positive=(u'কম্পিউটার').split(), negative=[], topn=5)
for w in words:
    print w[0].encode('utf-8')

