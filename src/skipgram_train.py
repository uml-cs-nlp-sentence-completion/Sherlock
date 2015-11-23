#!/usr/bin/python

#Author : Gayas Chowdhury

import os
import sys
import argparse
import nltk
import re
import logging
from gensim.models import Word2Vec

#Class for reading sentences from file
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

def build_model(sentences, model_name):
    num_features    = 640    # Word vector dimensionality
    min_word_count  = 40   # Minimum word count
    num_workers     = 4       # Number of threads to run in parallel
    context         = 5          # Context window size
    downsampling    = 1e-3   # Downsample setting for frequent words
   
    #model = Word2Vec(sentences, workers=num_workers, size=num_features, min_count = min_word_count, window = context, sample = downsampling, seed=1)
    
    model = Word2Vec(sentences, workers=num_workers, size=num_features, window = context, sample = downsampling, seed=1)
    model.init_sims(replace=True)
    model.save(model_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir', dest="indir", required=True, nargs=1, help="Input dir")
    parser.add_argument('-m', '--model', dest="model", required=True, nargs=1, help="Model name")
    
    args        = parser.parse_args()
    indir       = args.indir[0]
    model_name  = args.model[0]
    sentences   = MySentences(indir) # a memory-friendly iterator

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    build_model(sentences, model_name)



