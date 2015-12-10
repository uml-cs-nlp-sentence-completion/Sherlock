#!/usr/bin/python

# Author : Gayas Chowdhury

# Summary :
# This program preprocess raw text corpus for different models
# It removes all the meta data, and make them ready for feeding into Language models
# It takes 2 parameters. They are, f/files, and o/outputdir
# -f/--files    : path to files for preprocessing
# -o/outputdir  : location for storing preprocessed files
# Usage :
# python preprocessing.py -f file01.txt file02.txt -o output_dir
# python preprocessing.py -f corpus/* -o output_dir

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import argparse
import nltk
import re
import tools
import string

from os import path
from nltk.tokenize import WordPunctTokenizer

end_tags = ["End of Project Gutenberg's Etext", "End of Project Gutenberg Etext", "End of the Project Gutenberg Etext", "End of the Project Gutenberg eText"]

#Remove the metadata
def preprocess_text(input_path):
    end_tag = "*END*"
    seen_end_tag = False
    
    content = ""
    in_file = open(input_path)
    
    for line in in_file:
        line = unicode(line, errors='ignore')
        if not seen_end_tag:
            if end_tag not in line:
                continue
            else:
                seen_end_tag = True
                continue
    
        reached_end = False
        for tag in end_tags:
            if tag in line:
                reached_end = True
                break

        if reached_end:
            continue
        if not line.strip():
            continue
        content = content + line

    in_file.close()

    return content

#Make file contents as collection of sentences
def make_sententens(content):
    content     = content.decode('utf8');
    sentences   = nltk.sent_tokenize(content)
    
    sents = []
    for sent in sentences:
        sent = process_sentence(sent)
        
        if len(sent) > 0:
            sents.append(sent)

    return sents

def process_sentence(sent):
    sent    = sent.lower()
        
    words   = nltk.word_tokenize(sent)
    sent    = ' '.join(words)
    sent    = tools.replace_punct(sent)
    sent    = tools.replace_number(sent)
    sent    = ' '.join([w.strip() for w in sent.split() if len(w.strip()) > 0]) #Remove extra spaces

    return sent


def format_text(file_content):
    file_content = file_content.replace('\r\n', ' ')
    file_content = file_content.replace('\"', ' ')
    file_content = re.sub(r'\bMr\.|mr\.\b','mr', file_content)
    file_content = re.sub(r'\bMrs\.|mrs\.\b','mrs', file_content)
    file_content = re.sub(r'\bDr\.|dr\.\b','dr', file_content)
    
    return file_content

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', dest="file_names", required=True, nargs="*", help="Input file names")
    parser.add_argument('-o', '--outputdir', dest="output_dir", required=True, nargs=1, help="Output dir")
    
    args        = parser.parse_args()
    file_names  = args.file_names
    output_dir  = args.output_dir[0]
    
    for file_name in file_names:
        if path.isfile(file_name):
            file_basename   = path.basename(file_name)
            out_file        = path.join(output_dir, file_basename)
            
            print('Processing ' + file_name)
            
            file_content    = preprocess_text(file_name)
            file_content    = format_text(file_content)
            sents           = make_sententens(file_content)
            
            tools.write_collection(sents, out_file)
        else:
            print(file_name + ' is not found')

