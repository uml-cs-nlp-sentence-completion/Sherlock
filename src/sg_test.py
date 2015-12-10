#!/usr/bin/python

#Author : Gayas Chowdhury

# Summary:   This program calculate the score for each question
# It takes 3 parameters as input.
# -q/--qfile    : path to the questions file prepared by the prepare_qns.py program
# -m/--model    : path to the trained model prepared by sg_train_v1.py
# -a/--ansfile  : path to the file to save questions and their score
#
# Example usage : python sg_test.py -q ../data/sg_format_questions.txt -m ../data/movel -a ../data/sg_format_answers.txt

from __future__ import print_function

import argparse
import tools

from gensim.models import Word2Vec

#Instance for question
class Question(object):
    def __init__(self, line):
        self.__instance__(line)
    
    def __instance__(self, sentence):
        sent = sentence.split(tools.TAB)
        
        self.text       = sent[0] #Get the question text
        self.__qwords   = sent[1].split() #Get all the words except missing word
        self.__answord  = sent[2] #Missging word
    
    # Calculate the cossine similarities between missing word and rest of the words in the sentence, and sum all of them
    # Retun the calculated cosine similarity as score
    def calc_score(self, model):
        score = 0
        
        for word in self.__qwords:
            score = score + model.similarity(word, self.__answord)
        
        return score/(len(self.__qwords) + 1)

#Class for reading questions from file and making Question instance
class Questions(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for line in open(self.filename):
            yield Question(line[: - 1])

#Calculate the score for questions and write back to the file
def write_score(questions, model, filepath):
    f = open(filepath, 'w')
    
    for q in questions:
        score   = q.calc_score(model)
        text    = q.text + tools.TAB + str(score)
        
        print(text, file=f)
    
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--qfile', dest="qfile", required=True, nargs=1, help="Path to the sg_format_questions.txt file")
    parser.add_argument('-m', '--model', dest="model", required=True, nargs=1, help="Path to the Word2Vec Model")
    parser.add_argument('-a', '--ansfile', dest="ansfile", required=True, nargs=1, help="Path to the file to write answers")
    
    args    = parser.parse_args()
    qfile   = args.qfile[0]
    model   = args.model[0]
    ansfile = args.ansfile[0]

    questions   = Questions(qfile)
    model       = Word2Vec.load(model)
    
    write_score(questions, model, ansfile)


