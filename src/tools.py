#!/usr/bin/python

#Author : Gayas Chowdhury

from __future__ import print_function

import os
import sys
import argparse
import nltk
import re

from nltk.corpus import stopwords
from nltk.stem.porter import *
from os import path

def remove_punctuation(text):
    return re.sub("[^a-zA-Z]", " ", text)

#  stem_text(text) : method to remove and replace word suffixes
#   Parameters:
#       text : a sentence or collection of sentences
#   Return: stemmed sentences
#   Usage : stem_text('Please stem this sentence.')
def stem_text(text):
    stm     = PorterStemmer()
    tokens  = text.split()
    words   = [stm.stem(w)for w in tokens]
    snt     = ' '.join(words)

    return snt

def mark_sentence(sent):
    return "<s> " + sent.strip() + " </s>"

# Method : remove_stopwords(text) : remove stop words from the sentences
#   Parameters:
#       text : the sentences to strip off the stop words
#   Return: the sentences
#   Usage : remove_stopwords('Remove stopwords from this sentence.')
def remove_stopwords(text):
    words       = text.split()
    stop_words  = set(stopwords.words("english"))
    
    meaningful_words = [w for w in words if not w in stop_words]
    
    return ' '.join(meaningful_words)

def process_sentence(sentence):
    sentence = stem_text(remove_punctuation(remove_stopwords(sentence)))
    if len(sentence.strip()) > 0:
        sentence = mark_sentence(sentence)
    
    return sentence


