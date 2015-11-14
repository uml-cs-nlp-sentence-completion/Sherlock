#!/usr/bin/python

# Author : Gayas Chowdhury

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import argparse
import nltk
import re

from os import path
from nltk.tokenize import WordPunctTokenizer

end_tags = ["End of Project Gutenberg's Etext", "End of Project Gutenberg Etext", "End of the Project Gutenberg Etext", "End of the Project Gutenberg eText"]

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

def write_to_file(content, filepath):
    ofile = open(filepath, 'w')
    
    content     = content.decode('utf8');
    sentences   = nltk.sent_tokenize(content)
    
    for sent in sentences:
        sent    = expand_contraction(sent.lower())
        words   = nltk.word_tokenize(sent)
        line    = ' '.join(words)
        
        print(line, file=ofile)
    
    ofile.close()


def format_text(content):
    content = content.replace('\r\n', ' ')
    content = content.replace('"', ' ')
    content = re.sub(r'\bMr\.|mr\.\b',' ', content)
    content = re.sub(r'\bMrs\.|mrs\.\b',' ', content)
    content = re.sub(r'\bDr\.|dr\.\b',' ', content)

    return content

contractions_list = { "ain't" : 'am not', "aren't" : 'are not', "can't" : 'can not', "could've": 'could have', "couldn't":	'could not', "couldn't've":	'could not have', "didn't":	'did not', "doesn't":	'does not', "don't":	'do not', "hadn't":	'had not', "hadn't've":	'had not have', "hasn't":	'has not', "haven't":	'have not', "he'd":	'he had', "he'd've":	'he would have', "he'll":	'he will', "he's":	'he is', "he'sn't":	'he is not', "how'd":	'how would', "how'll":	'how will', "how's":	'how is', "i'd":	'i would', "i'd've":	'i would have', "i'll":	'i will', "i'm":	'i am', "i've":	'i have', "i'ven't":	'i have not', "isn't":	'is not', "it'd":	'it had', "it'd've":	'it would have', "it'll":	'it will', "it's":	'it is', "it'sn't":	'it is not', "let's":	'let us', "ma'am":	'madam', "mightn't":	'might not', "mightn't've":	'might not have', "might've":	'might have', "mustn't":	'must not', "must've":	'must have', "needn't":	'need not', "not've":	'not have', "o'clock":	'of the clock', "oughtn't":	'ought not', "shan't":	'shall not', "she'd":	'she had or she would', "she'd've":	'she would have', "she'll":	'she shall or she will', "she's":	'she has or she is', "she'sn't":	'she has not or she is not', "should've":	'should have', "shouldn't":	'should not', "shouldn't've":	'should not have', "somebody'd":	'somebody had or somebody would', "somebody'd've":	'somebody would have', "somebody'dn't've":	'somebody would not have', "somebody'll":	'somebody shall or somebody will', "somebody's":	'somebody has or somebody is', "someone'd":	'someone had or someone would', "someone'd've":	'someone would have', "someone'll":	'someone shall or someone will', "someone's":	'someone has or someone is', "something'd":	'something had or something would', "something'd've":	'something would have', "something'll":	'something shall or something will', "something's":	'something has or something is', "that'll":	'that will', "that's":	'that has or that is', "there'd":	'there had or there would', "there'd've":	'there would have', "there're":	'there are', "there's":	'there has or there is', "they'd":	'they had or they would', "they'd've":	'they would have', "they'll":	'they shall or they will', "they're":	'they are', "they've":	'they have', "'twas":	'it was', "wasn't":	'was not', "we'd":	'we had or we would', "we'd've":	'we would have', "we'll":	'we will', "we're":	'we are', "we've":	'we have', "weren't":	'were not', "what'll":	'what shall or what will', "what're":	'what are', "what's":	'what has or what is or what does', "what've":	'what have', "when's":	'when has or when is', "where'd":	'where did', "where's":	'where has or where is', "where've":	'where have', "who'd":	'who would or who had', "who'd've":	'who would have', "who'll":	'who shall or who will', "who're":	'who are', "who's":	'who has or who is', "who've":	'who have', "why'll":	'why will', "why're":	'why are', "why's":	'why has or why is', "won't":	'will not', "won't've":	'will not have', "would've":	'would have', "wouldn't":	'would not', "wouldn't've":	'would not have', "y'all":	'you all', "y'all'll":	'you all will', "y'all'd've":	'you all would have', "y'all'dn't've":	'you all would not have', "you'd":	'you had or you would', "you'd've":	'you would have', "you'll":	'you shall or you will', "you're":	'you are', "you'ren't":	'you are not', "you've" :	'you have', "you'ven't": 'you have not'}


def expand_contraction(text):
    text = text.split()
    words = [contractions_list[word] if word in contractions_list else word for word in text]

    return ' '.join(words)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="input", required=True, nargs="*", help="Input file names")
    parser.add_argument('-o', '--outputdir', dest="output_dir", required=True, nargs=1, help="Output dir")
    
    args            = parser.parse_args()
    files           = args.input
    
    output_dir      = args.output_dir[0]

    for file in files:
        if path.isfile(file):
            file_name = path.basename(file)
            out_file = path.join(output_dir, file_name)
            print('Processing ' + file)
            content = preprocess_text(file)
            content = format_text(content)
            write_to_file(content, out_file)

