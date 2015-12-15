#! /usr/bin/env python

"""                                                                              
 Copyright Gayas Chowdhury 2015
                                                                              
 File Name : skipgram_solution.py
                                                                              
 Creation Date : 15-12-2015
                                                                              
 Last Modified : Tue 15 Dec 2015 05:53:00 PM EST
                                                                              
 Created By : Gayas Chowdhury
                                                                              
 Purpose : Skip Gram Solution

"""

from solution import Solution

import subprocess
import os


TRAINING        = "data/Holmes_Training_Data/"
PROCESSED       = "data/preprocessed/"
MODEL           = "models/skipgram_model"
TEST            = "data/MSR_Sentence_Completion_Challenge_V1/Data/"
MF_QUESTIONS    = "data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.questions.txt"
LM_QUESTIONS    = "data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.lm_format.questions.txt"
SG_QUESTIONS    = "data/MSR_Sentence_Completion_Challenge_V1/Data/sg_format.questions.txt"
ANSWERS         = "results/skipgram.res"

class skipgram_solution(Solution):

  def __init__(self, verbose=False):
    if verbose:
      print "Skip Gram solution started"
    self.verbose = verbose

    if (len(os.listdir(PROCESSED)) == 1 ):
        # Call preprocess.
        if (self.verbose):
            print "Preprocessing files"
        # Make call
        call = ["python"]
        call.append("src/preprocessing.py")
        call.append("-f")

        for each in os.listdir(TRAINING):
            call.append(TRAINING + each)
        call.append("-o")
        call.append(PROCESSED)
                            
        o=subprocess.call(call)
        if o == 0:
            print "Preprocessed files built."
        else:
            print "failed on preprocess"
            exit(1)
  
  def train(self, data):
    if self.verbose:
      print "Running sg_train script on ", data
    
    procs = ["python", "src/sg_train.py", "-f"]
    
    for fname in os.listdir(PROCESSED):
        procs.append(PROCESSED + fname)

    procs = procs + ["-m", MODEL]
    
    o=subprocess.call(procs)

    if self.verbose:
      print "Train script ",
      if o == 0:
        print "suceeded! Model built!"
      else:
        print "failed!"
  
  def test(self, data):
    if self.verbose:
      print "Running sg_test script on ", data
   
    if(not os.path.isfile(SG_QUESTIONS)):
        # Call preprocess.
        if (self.verbose):
            print "Preparing Questions"
        # Make call
        call = ["python"]
        call.append("src/prepare_questions.py")
        call.append("-l")
        call.append(LM_QUESTIONS)
        call.append("-mf")
        call.append(MF_QUESTIONS)
        call.append("-o")
        call.append(SG_QUESTIONS)

        o=subprocess.call(call)
        if o == 0:
            print "Prepared Questions."
        else:
            print "failed on preparing questions"
            exit(1)
    
    o = subprocess.call(["python","src/sg_test.py", "-q", SG_QUESTIONS, "-m", MODEL, "-a", ANSWERS])

    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"


  def evaluate(self, results):
    if self.verbose:
      print "Running evaluate script"

    o = subprocess.call(["src/evaluate.sh", ANSWERS])
    
    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"

