#! /usr/bin/env python

"""                                                                              
 Copyright Gayas Chowdhury 2015
                                                                              
 File Name : skipgram_solution.py
                                                                              
 Creation Date : 15-12-2015
                                                                              
 Last Modified : Tue 23 Nov 2015 08:31:31 PM EST
                                                                              
 Created By : Gayas Chowdhury
                                                                              
 Purpose : Skip Gram Solution

"""

from solution import Solution
import subprocess
import os


TRAINING    = "data/preprocessed/"
MODEL       = "models/skipgram_model"

TEST        = "data/MSR_Sentence_Completion_Challenge_V1/Data/"
QUESTIONS   = "data/MSR_Sentence_Completion_Challenge_V1/Data/SkipGram_format.questions.txt"
ANSWERS     = "results/Smoothed_4gram.res"

class skipgram_solution(Solution):

  def __init__(self, verbose=False):
    if verbose:
      print "Skip Gram solution started"
    self.verbose = verbose
  
  def train(self, data):
    if self.verbose:
      print "Running sg_train script on ", data
    
    procs = ["python", "src/sg_train.py", "-f"]
    
    for fname in os.listdir(TRAINING):
        procs.append(TRAINING + fname)

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
      
    o = subprocess.call(["src/sg_test.py", "-q", QUESTIONS, "-m", MODEL, "-a", ANSWERS])

    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"


  def evaluate(self, results):
    if self.verbose:
      print "Running evaluate script"

    o = subprocess.call(["src/evaluate.sh", "results/Smoothed_4gram.res"])
    
    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"

