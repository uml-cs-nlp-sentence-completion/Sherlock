#!/usr/bin/python
import os
import sys
import argparse
import nltk
import re

from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

from os import path

def remove_punctuation(text):
    return re.sub("[^a-zA-Z]", " ", text)

#  stem_text(text) : method to remove and replace word suffixes
#   Parameters:
#       text : a sentence or collection of sentences
#   Return: stemmed sentences
#   Usage : stem_text('Please stem this sentence.')
def stem_text(text):
    stm     = LancasterStemmer()
    tokens  = text.split()
    words   = [stm.stem(w)for w in tokens]
    snt     = ' '.join(words)

    return snt


def process_sentences(sentences, options):
    processed_sents = []
    
    for sentence in sentences:
        sentence = sentence.replace('\r\n', '').lower()
        if len(sentence) >= 1:
            for op in options:
                sentence = OPTIONS[op](sentence)
                words = [w for w in sentence.split() if len(w) > 0]
                sentence = " ".join(words)
            processed_sents.append(sentence)

    return processed_sents

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

def remove_determiner(text):
    determiners = ["a","able","about","across","after","all",
                       "almost","also","am","among","an","and","any","are",
                       "as","at","be","because","been","but","by","can","cannot",
                       "could","dear","did","do","does","either","else","ever",
                       "every","for","from","get","got","had","has","have","he",
                       "her","him","his","how","however","i","if","in",
                       "into","is","it","its","just","least","let","like",
                       "may","me","might","most","must","my","neither",
                       "no","nor","not","of","off","often","on","only","or",
                       "other","our","own","rather","said","say","says","she",
                       "should","since","so","some","than","that","the","their",
                       "them","then","there","these","they","this","tis","to",
                       "too","twas","us","was","we","were","what","when",
                       "where","which","while","who","whom","why","will","with",
                       "would","yet","you","your"]
                       
    words = [word for word in text.split() if word not in determiners]

    return " ".join(words)

def clean_text(files, output_dir, options):
    for file in files:
        if path.isfile(file):
            file_name = path.basename(file)
            fp = open(file)
            lines = fp.readlines()
            fp.close()
            
            lines = process_sentences(lines, options)
            
            out_file = open(path.join(output_dir, file_name), 'w')
            
            for line in lines:
                out_file.write(line + '\n')
            
            out_file.close()


OPTIONS = {'rp': remove_punctuation, 'ms': mark_sentence, 'rd' : remove_determiner, 'stm': stem_text}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="input", required=True, nargs="*", help="Input file names")
    parser.add_argument('-O', '--outputdir', dest="output_dir", required=True, nargs=1, help="Output dir")
    parser.add_argument('-o', '--options', dest="options", nargs="+", required=True, choices=OPTIONS, help="rp : Remove punctuations, ms: Mark Sentences with <s> and </s> tag, rd: Remove determinant, stm: Stem sentence")
    
    args            = parser.parse_args()
    all_files       = args.input
    options         = args.options
    output_dir      = args.output_dir[0]
    
    clean_text(all_files, output_dir, options)


