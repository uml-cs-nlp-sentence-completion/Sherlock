#!/usr/bin/python

'''
    Author     : Gayas Chowdhury
    Summary    : This program trains the skip gram model using word2vec
    It takes two arguments:
    -f/-files     : name of the training files
    -m/--model    : name of the model to save. This model will be used for testing
    
    Example usage : python sg_train.py -f file01.txt file02.txt -m skip_gram_model
    
    '''
import argparse
import logging
import tools

from gensim.models import Word2Vec
from gensim.models import Phrases

#Class for reading sentences from file
class Sentences(object):
    def __init__(self, file_names):
        self.file_names = file_names
    
    def __iter__(self):
        for fname in self.file_names:
            for line in open(fname):
                yield [tools.START_TOKEN] + line.split() + [tools.END_TOKEN]

#Train and save the model
def build_model(sentences, model_name):
    num_features    = tools.SG_NUM_FEATURES   # Word vector dimensionality
    min_word_count  = 5     # Minimum word count
    num_workers     = 4     # Number of threads to run in parallel
    context         = 5     # Context window size
    downsampling    = 1e-3  # Downsample setting for frequent words
   
    model = Word2Vec(sentences, workers=num_workers, sg = 0, size=num_features, min_count = min_word_count, window = context, sample = downsampling, seed=1)
    model.init_sims(replace=True)
    model.save(model_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', dest="file_names", required=True, nargs="*", help="Training file names")
    parser.add_argument('-m', '--model', dest="model", required=True, nargs=1, help="Model name")
    
    args        = parser.parse_args()
    file_names  = args.file_names
    model_name  = args.model[0]
    sentences   = Sentences(file_names) # a memory-friendly iterator

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    build_model(sentences, model_name)



