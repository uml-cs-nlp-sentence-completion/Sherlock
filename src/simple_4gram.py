#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : simple_4gram.py
                                                                              
 Creation Date : 23-11-2015
                                                                              
 Last Modified : Mon 23 Nov 2015 06:15:21 PM EST
                                                                              
 Created By : Renan Campos                                                    
                                                                              
 Purpose : Simple 4 gram solution.

"""

from solution import Solution
import subprocess


TRAINING = "data/Holmes_Training_Data/"

TEST = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/"

class simple_4gram(Solution):

  def __init__(self, verbose=False):
    if verbose:
      print "Simple 4gram solution started"
    self.verbose = verbose
  
  def train(self, data):
    if self.verbose:
      print "Running simple_4gram script on ", data
      
    o=subprocess.call(["src/cmu_scripts/simple_4gram.sh", "--train", TRAINING])

    if self.verbose:
      print "Train script ",
      if o == 0:
        print "suceeded! Model built!"
      else:
        print "failed!"
  
  def test(self, data):
    if self.verbose:
      print "Running simple_4gram script on ", data
      
    o = subprocess.call(["src/cmu_scripts/simple_4gram.sh", "--test", TEST])

    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"


  def evaluate(self, results):
    if self.verbose:
      print "Running evaluate script"

    o = subprocess.call(["src/evaluate.sh", "results/Simple_ngram.res"])
    
    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"

