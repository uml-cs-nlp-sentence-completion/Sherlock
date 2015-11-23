#!/usr/bin/python

#Author : Gayas Chowdhury

from __future__ import print_function
import os
import sys
import argparse
import nltk
from gensim.models import Word2Vec

#Instance for question
class Question(object):
    def __init__(self, line):
        self.text = line
        
        self.__qwords = []
        self.__answord = ''
        self.__buildQuestion__()
        
    def calc_score(self, model):
        score = 0
        
        for word in self.__qwords:
            score = score + model.similarity(word, self.__answord)
        
        return score

    def __buildQuestion__(self):
        words = nltk.word_tokenize(self.text.lower())[2:]
        
        indx = words.index('[')
        
        self.__qwords = words[:indx] + words[indx + 3:]
        self.__answord = words[indx + 1]

#Class for reading questions from file and making Question instance
class Questions(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            yield Question(line[: len(line) - 1])

#Calculate the score for questions and write back to the file
def write_score(questions, model, filepath):
    f = open(filepath, 'w')
    
    for q in questions:
        score = q.calc_score(model)
        text = q.text + ' ' + str(score)
        print(text, file=f)
    
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--qfile', dest="qfile", required=True, nargs=1, help="Path to the machine_format.questions file")
    parser.add_argument('-m', '--model', dest="model", required=True, nargs=1, help="Path to the Word2Vec Model")
    parser.add_argument('-a', '--ansfile', dest="ansfile", required=True, nargs=1, help="Path to the file to write answers")
    
    args    = parser.parse_args()
    qfile   = args.qfile[0]
    model   = args.model[0]
    ansfile = args.ansfile[0]

    questions   = Questions(qfile)
    model       = Word2Vec.load(model)
    
    write_score(questions, model, ansfile)


