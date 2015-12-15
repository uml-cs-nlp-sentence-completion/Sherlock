#!/usr/bin/python

'''
    Author : Gayas Chowdhury
    Summary : It contains all tth utility functions
    
    '''

from __future__ import print_function

import os
import sys
import argparse
import nltk
import re
import string

from nltk.corpus import stopwords
from nltk.stem.porter import *
from os import path

EMPTY_LIST      = []
EMPTY_STRING    = ''
TAB             = '\t'
START_TOKEN     = '<s>'
END_TOKEN       = '</s>'
SPACE           = ' '

SG_NUM_FEATURES = 640

#Class for reading sentences from files
class Sentences(object):
    def __init__(self, file_names):
        self.file_names = file_names
    
    def __iter__(self):
        for fname in self.file_names:
            for line in open(fname):
                yield line[:-1]

# Remove punctions from text
def remove_punctuation(text, especial_puncts = EMPTY_LIST):
    words   = text.split()
    puncts  = list(string.punctuation) + especial_puncts
    words   = [w for w in words if w not in puncts]
    
    return ' '.join(words)

#Replace punctuation with specified token
def replace_punct(sent, token = ''):
    regex   = re.compile('[%s]' % re.escape(string.punctuation))
    sent    = regex.sub(token, sent)
    sent    = sent.split()
    sent    = ' '.join(sent)
    
    return sent

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

#Replace number with specified token or N
def replace_number(sentence, token = 'N'):
    pattern = r"[+-]?[\d\,]+(?:\.\d+)?(?:[eE][+-]?\d+)?" #regex for number
    
    return re.sub(pattern, token, sentence)

# Mark the sentence with <s> and </s> tokens
def mark_sentence(sent):
    return START_TOKEN + SPACE + sent.strip() + SPACE + END_TOKEN

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
    sentence = replace_number(remove_punctuation(sentence))
    
    if len(sentence.strip()) > 0:
        sentence = mark_sentence(sentence)
    
    return sentence

def write_collection(lst, file_name):
    ofile = open(file_name, 'w')
    
    for em in lst:
        print(em, file=ofile)
    
    ofile.close()

# Common Method for formating sentence
def process_sent_stem(tokenized_sent):
    sent    = replace_punct(tokenized_sent, EMPTY_STRING)
    sent    = replace_number(sent)
    sent    = stem_text(sent)
    
    sent = ' '.join([w.strip() for w in sent.split() if len(w.strip()) > 0]) #Remove extra spaces
    
    return sent

# Method for formating sentence for Skip-Gram
def process_sent(tokenized_sent):
    sent    = replace_punct(tokenized_sent, EMPTY_STRING)
    sent    = replace_number(sent)
    
    sent = ' '.join([w.strip() for w in sent.split() if len(w.strip()) > 0]) #Remove extra spaces
    
    return sent


#Contractions list used for expanding contractions
contractions_list = { "ain't" : 'am not', "aren't" : 'are not', "can't" : 'can not', "could've": 'could have', "couldn't":	'could not', "couldn't've":	'could not have', "didn't":	'did not', "doesn't":	'does not', "don't":	'do not', "hadn't":	'had not', "hadn't've":	'had not have', "hasn't":	'has not', "haven't":	'have not', "he'd":	'he had', "he'd've":	'he would have', "he'll":	'he will', "he's":	'he is', "he'sn't":	'he is not', "how'd":	'how would', "how'll":	'how will', "how's":	'how is', "i'd":	'i would', "i'd've":	'i would have', "i'll":	'i will', "i'm":	'i am', "i've":	'i have', "i'ven't":	'i have not', "isn't":	'is not', "it'd":	'it had', "it'd've":	'it would have', "it'll":	'it will', "it's":	'it is', "it'sn't":	'it is not', "let's":	'let us', "ma'am":	'madam', "mightn't":	'might not', "mightn't've":	'might not have', "might've":	'might have', "mustn't":	'must not', "must've":	'must have', "needn't":	'need not', "not've":	'not have', "o'clock":	'of the clock', "oughtn't":	'ought not', "shan't":	'shall not', "she'd":	'she had or she would', "she'd've":	'she would have', "she'll":	'she shall or she will', "she's":	'she has or she is', "she'sn't":	'she has not or she is not', "should've":	'should have', "shouldn't":	'should not', "shouldn't've":	'should not have', "somebody'd":	'somebody had or somebody would', "somebody'd've":	'somebody would have', "somebody'dn't've":	'somebody would not have', "somebody'll":	'somebody shall or somebody will', "somebody's":	'somebody has or somebody is', "someone'd":	'someone had or someone would', "someone'd've":	'someone would have', "someone'll":	'someone shall or someone will', "someone's":	'someone has or someone is', "something'd":	'something had or something would', "something'd've":	'something would have', "something'll":	'something shall or something will', "something's":	'something has or something is', "that'll":	'that will', "that's":	'that has or that is', "there'd":	'there had or there would', "there'd've":	'there would have', "there're":	'there are', "there's":	'there has or there is', "they'd":	'they had or they would', "they'd've":	'they would have', "they'll":	'they shall or they will', "they're":	'they are', "they've":	'they have', "'twas":	'it was', "wasn't":	'was not', "we'd":	'we had or we would', "we'd've":	'we would have', "we'll":	'we will', "we're":	'we are', "we've":	'we have', "weren't":	'were not', "what'll":	'what shall or what will', "what're":	'what are', "what's":	'what has or what is or what does', "what've":	'what have', "when's":	'when has or when is', "where'd":	'where did', "where's":	'where has or where is', "where've":	'where have', "who'd":	'who would or who had', "who'd've":	'who would have', "who'll":	'who shall or who will', "who're":	'who are', "who's":	'who has or who is', "who've":	'who have', "why'll":	'why will', "why're":	'why are', "why's":	'why has or why is', "won't":	'will not', "won't've":	'will not have', "would've":	'would have', "wouldn't":	'would not', "wouldn't've":	'would not have', "y'all":	'you all', "y'all'll":	'you all will', "y'all'd've":	'you all would have', "y'all'dn't've":	'you all would not have', "you'd":	'you had or you would', "you'd've":	'you would have', "you'll":	'you shall or you will', "you're":	'you are', "you'ren't":	'you are not', "you've" :	'you have', "you'ven't": 'you have not'}

#Expand contraction 
def expand_contraction(text):
    text    = text.split()
    words   = [contractions_list[word] if word in contractions_list else word for word in text]
    
    return ' '.join(words)