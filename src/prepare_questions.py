#!/usr/bin/python

# Author : Gayas Chowdhury

import argparse
import nltk
import re
import tools

from nltk.tokenize import WordPunctTokenizer
from gensim.models import Phrases

def process_sent_sg(sent):
    words = sent.split()[1 : -1]
    qwords    = [w for w in words if not w.startswith("[")]
    awords    = [w for w in words if w.startswith("[")]
    
    answords    = awords[0][1:-1]
    
    i = 0
    for word in words:
        if word in awords:
            words[i] = word[1:-1]
        i = i + 1

    sent = ' '.join([tools.START_TOKEN] + words + [tools.END_TOKEN])

    answords = process_answords(answords)
    answord  = answords[0]

    qwords = qwords + [w for w in answords[1:] if len(answords)> 1]
    qwords = process_qwords(qwords)
    
    sent = sent + tools.TAB + qwords + tools.TAB + answord
    
    return sent

def process_qwords(qwords):
    qwords      = ' '.join(qwords)
    qwords      = nltk.word_tokenize(qwords)
    
    qwords_sent = ' '.join(qwords)
    qwords_sent = tools.replace_punct(qwords_sent)
    qwords_sent = tools.replace_number(qwords_sent.lower())
    
    qwords = qwords_sent.split()
    qwords  = ' '.join([tools.START_TOKEN] + qwords + [tools.END_TOKEN])

    return qwords

def process_answords(answords):
    answords        = nltk.word_tokenize(answords)
    answords_sent   = ' '.join(answords)
    answords_sent   = tools.replace_punct(answords_sent)
    answords_sent   = tools.replace_number(answords_sent.lower())
    answords        = answords_sent.split()

    return answords

def make_sentences(sentences):
    sents = []
    
    for sent in sentences:
        sent = process_sent_sg(sent)
        sents.append(sent)
    
    return sents

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ifile', dest="input_file", required=True, nargs=1, help="Input file name")
    parser.add_argument('-o', '--ofile', dest="output_file", required=True, nargs=1, help="Output file name")
    
    args    = parser.parse_args()
    ifile   = args.input_file
    ofile   = args.output_file[0]
    
    sentences = tools.Sentences(ifile)
    sentences = make_sentences(sentences)

    tools.write_collection(sentences, ofile)






