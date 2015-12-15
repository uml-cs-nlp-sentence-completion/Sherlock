#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : lsa.py
                                                                              
 Creation Date : 15-12-2015
                                                                              
 Last Modified : Tue 15 Dec 2015 04:21:14 PM EST
                                                                              
 Created By : Renan Campos                                                    
                                                                              
 Purpose : Implementation of Latent Semantic Analysis.
           Uses singular value decomposition on a term-document matrix to
           identify latent similarities between words.
"""

from solution import Solution
import subprocess
import os

import numpy as np
from scipy import linalg

TRAINING = "data/Holmes_Training_Data/"

PRE_DATA = "data/preprocessed/"

TEST = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/"

class lsa(Solution):
  
  def __init__(self, verbose=False):
    """ Preprocesses files if not already"""
    self.verbose = verbose
    
    if ( len(os.listdir(PRE_DATA)) == 1 ):
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
      call.append(PRE_DATA)

      o=subprocess.call(call) 
      if o == 0:
        print "Preprocessed files built."
      else:
        print "failed on preprocess"
        exit(1)

    if (self.verbose):
      print "Latent Semantic Analysis started"

  def train(self, data):
    """
      Generate vocabulary of top 100000 words
      Create term-document matrix
      Apply TF-IDF (Term Frequency, Inverse Document Frequency)
      Apply SVD to attain matricies U, s, and Vt
      Reduce s to 300 dimensions (zero out remainder)
      Create diagnol matrix Sig with s
      Multiply U Sig Vt to get approximated term-document matrix
      Pickle model
    """
    if self.verbose:
      print "Running lsa script on ", data

  def test(self, data):
    """
      Unpickle model (term-document matrix)
      Treat each test sentence as a document, and calculate te 
    """  
    if self.verbose:
      print "Running simple_4gram script on ", data
      

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

    


