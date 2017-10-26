"""
  Copyright 2013 Travis Brady All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Python port of Mikolov's word2phrase.c
From: http://word2vec.googlecode.com/svn/trunk/word2phrase.c

Edited by Tamjid Al Rahat
"""

from itertools import tee, izip_longest
from collections import defaultdict



inp_file = './data/clean_sentences.txt'
out_file = './data/sentences_with_phrases.txt'

def pairwise(iterable):
    """
    Adjacent pairs with overlap
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, None)]
    """
    a, b = tee(iterable)
    next(b)
    return izip_longest(a, b)

def learn_vocab_from_train_iter(train_iter):
    """
    Creates a frequency table mapping unigrams and bigrams to their
    count of appearances in the training set
    Analogous to LearnVocabFromTrainFile from original
    """
    vocab = defaultdict(int)
    train_words = 0
    for line in train_iter:
        if line == []:    # If there are multiple empty lines following each other, the loop is broken
          continue        # without giving any errors. That line solves the problem. (Ahmet Aksoy 20160721)
        for pair in pairwise(line):
            #print pair[0].decode('utf-8')
            vocab[pair[0]] += 1
            if None not in pair:
                vocab[pair] += 1
            train_words += 1
    return vocab, train_words

def filter_vocab(vocab, min_count):
    """
    Filter elements from the vocab occurring fewer than min_count times
    """
    return dict((k, v) for k, v in vocab.iteritems() if v >= min_count)

def train_model(train_iter, min_count=5, threshold=100.0, sep='_'):
    """
    The whole file-to-file (or in this case iterator to iterator) enchilada
    Does the same thing as Mikolov's original TrainModel in word2phrase.c
    Parameters:
    train_iter : an iterator containing tokenized documents
        Example: [['hi', 'there', 'friend'],['coffee', 'is', 'enjoyable']]
    min_count : min number of mentions for filter_vocab to keep word
    threshold : pairs of words w/ score >= threshold are marked as phrases.
        In word2phrase.c this meant the whitespace separating
        two words was replaced with '_'

    Yields:
        One list per row in input train_iter
    """
    vocab_iter, train_iter = tee(train_iter)
    vocab, train_words = learn_vocab_from_train_iter(vocab_iter)
    print "Total words: ", train_words
    print "Vocab size: ", len(vocab)

    vocab = filter_vocab(vocab, min_count)
    print "Filtered Vocab size: ", len(vocab)

    for line in train_iter:
        out_sentence = []
        pairs = pairwise(line)
        for pair in pairs:
            pa = vocab.get(pair[0])
            pb = vocab.get(pair[1])
            pab = vocab.get(pair)

            if all((pa, pb, pab)):
                score = (float(pab - min_count) / float((pa * pb))) * train_words   #error in original file.Corrected by Tamjid Al Rahat
            else:
                score = 0.0
            if score > threshold:
                next(pairs)
                out_sentence.append(sep.join(pair))
            else:
                out_sentence.append(pair[0])
        yield out_sentence

def main():
    """
    When called as a script this mimics the original word2phrase.c
    With a couple exceptions:
        1. We don't truncate words to 60 chars as in the original
        2. Whitespace handling doesn't exactly match the original
    """


    train_file = (line.split() for line in open(inp_file,'r').readlines())

    '''
    train_file = open('text8','r')
    words = []
    for line in train_file.readlines():
        line = line.decode('utf-8')
        words.append(line.split())
    '''

    min_count = 5
    threshold = 100.0
    sep = '_'
    discount = 0.05
    iters = 1   #phrase of three words

    out = train_file
    #print out
    for i in range(iters):
        this_thresh = max(threshold - (i * discount * threshold), 0.0)
        print "Iteration: %d Threshold: %6.2f" % (i+1, this_thresh)
        out = train_model(out, min_count=min_count,
                threshold=this_thresh,
                sep=sep)


    out_fh = open(out_file, 'w')
    for row in out:
        out_fh.write((' '.join(row) + '\n'))
    out_fh.close()

if __name__ == '__main__':
    main()

