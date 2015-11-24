#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : smoothed_3gram.py
                                                                              
 Creation Date : 23-11-2015
                                                                              
 Last Modified : Tue 24 Nov 2015 04:54:30 PM EST
                                                                              
 Created By : Renan Campos                                                    
                                                                              
 Purpose : Smoothed 3 gram solution.

"""

from solution import Solution
import subprocess


TRAINING = "data/Holmes_Training_Data/"

TEST = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/"

class smoothed_3gram(Solution):

  def __init__(self, verbose=False):
    if verbose:
      print "Smooth 3gram solution started"
    self.verbose = verbose
  
  def train(self, data):
    if self.verbose:
      print "Running smoothed_3gram script on ", data
      
    o=subprocess.call(["src/cmu_scripts/smoothed_3gram.sh", "--train", TRAINING])

    if self.verbose:
      print "Train script ",
      if o == 0:
        print "suceeded! Model built!"
      else:
        print "failed!"
  
  def test(self, data):
    if self.verbose:
      print "Running smoothed_3gram script on ", data
      
    o = subprocess.call(["src/cmu_scripts/smoothed_3gram.sh", "--test", TEST])

    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"


  def evaluate(self, results):
    if self.verbose:
      print "Running evaluate script"

    o = subprocess.call(["src/evaluate.sh", "results/Smoothed_3gram.res"])
    
    if self.verbose:
      print "Test script ",
      if o == 0:
        print "suceeded! Results file created"
      else:
        print "failed!"

