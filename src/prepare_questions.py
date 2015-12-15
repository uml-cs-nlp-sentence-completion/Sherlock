#!/usr/bin/python

# Author : Gayas Chowdhury
'''
    Summary: Prepare the questions for skip gram model. It takes 3 arguments;
    -l/-lmfile : Path to the Holmes.lm_format.questions.txt file
    -mf/--mffile : Path to the Holmes.machine_format.questions.txt file
    -o/--ofile : Path to the output file
    '''

import argparse
import nltk
import re
import tools

from nltk.tokenize import WordPunctTokenizer
from gensim.models import Phrases

'''
    Find the missing word and the reaming words.
    Make a single sentece of all the words except missing word and missing word seperated by TAB
    '''
def process_sent_sg(sent):
    words = sent.split()[1 : -1]
    qwords    = [w for w in words if not w.startswith("[")]
    awords    = [w for w in words if w.startswith("[")]
    
    answords    = awords[0][1:-1]

    answords = process_answords(answords)
    answord  = answords[0]

    qwords = qwords + [w for w in answords[1:] if len(answords)> 1]
    qwords = process_qwords(qwords)
    
    sent = qwords + tools.TAB + answord
    
    return sent

'''
    Merge the Holmes.lm_format.questions and the sentences returned from make_sentences
    each in one line
    '''
def merge_lm_questions_qwords(lmf_questions, sg_questions):
    zipped_qustions = zip(lmf_questions, sg_questions)
    
    questions = []
    for lm_q, sg_q in zipped_qustions:
        question = lm_q + tools.TAB + sg_q
        questions.append(question)

    return questions

'''
    Apply formating to the words except missing word
    '''
def process_qwords(qwords):
    qwords      = ' '.join(qwords)
    qwords      = nltk.word_tokenize(qwords)
    
    qwords_sent = ' '.join(qwords).lower()
    qwords_sent = tools.replace_punct(qwords_sent)
    qwords_sent = tools.replace_number(qwords_sent)
    
    qwords = qwords_sent.split()
    qwords  = ' '.join([tools.START_TOKEN] + qwords + [tools.END_TOKEN])

    return qwords

'''
    Apply formating to the missing word
    '''
def process_answords(answords):
    answords        = nltk.word_tokenize(answords)
    answords_sent   = ' '.join(answords).lower()
    answords_sent   = tools.replace_punct(answords_sent)
    answords_sent   = tools.replace_number(answords_sent)
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
    parser.add_argument('-l', '--lmfile', dest="lm_file", required=True, nargs=1, help="Holmes.lm_format.questions.txt file path")
    parser.add_argument('-mf', '--mffile', dest="mf_file", required=True, nargs=1, help="Holmes.machine_format.questions.txt file path")
    parser.add_argument('-o', '--ofile', dest="output_file", required=True, nargs=1, help="Output file name")
    
    args        = parser.parse_args()
    lmf_file    = args.lm_file
    mf_file     = args.mf_file
    ofile       = args.output_file[0]
    
    lmf_questions   = tools.Sentences(lmf_file)
    mf_sentences    = tools.Sentences(mf_file)
    sg_questions    = make_sentences(mf_sentences)
    
    sentences = merge_lm_questions_qwords(lmf_questions, sg_questions)
    
    tools.write_collection(sentences, ofile)






