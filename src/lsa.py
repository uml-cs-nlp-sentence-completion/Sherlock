#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : lsa.py
                                                                              
 Creation Date : 15-12-2015
                                                                              
 Last Modified : Tue 15 Dec 2015 08:34:08 PM EST
                                                                              
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
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from tools import cosine_similarity

import cPickle as pickle

TRAINING = "data/Holmes_Training_Data/"

PRE_DATA = "data/preprocessed/"

TEST = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/"

MODEL="models/lsa.model"

class _lsa_model:
  def __init__(self, vocab, corpus):
    """
      Create CountVectorizer object,
      Create a tfidf array
      Use SVD (Singular Value Decomposition) to approximate tfidf array
      Pickle-able
    """

    self.v = CountVectorizer(vocabulary=vocab)

    X = self.v.fit_transform(corpus).toarray()

    transformer = TfidfTransformer()

    tfidf = transformer.fit_transform(X)

    # SVD
    M,N = X.shape

    U,s,Vt = linalg.svd(X)

    # Reduce Matrix to only 300 dimensions
    for i in range(len(s)):
      if (i < 300):
        continue
      s[i] = 0

    Sig = linalg.diagsvd(s, M, N)
  
    # Store approximated document-term Matrix
    self.dt = (U.dot(Sig.dot(Vt))).transpose()

    print self.dt

  def cos_similarity(self, test_sentence, test_word):
    """
      Treat the test sentence as a document,
      Computes the total cosine similarity of each word in the sentence with
      respect to the test word.
      Returns total
    """
    tot_sim = 0
    
    if not self.v.vocabulary.get(test_word):
      return tot_sim

    t_vec = self.dt[self.v.vocabulary.get(test_word)]
    print test_word
    print t_vec

    print test_sentence
    for each in test_sentence.split():
      print each
      if not self.v.vocabulary.get(each):
        continue

      print self.dt[self.v.vocabulary.get(each)] 
      tot_sim += cosine_similarity(t_vec, self.dt[self.v.vocabulary.get(each)])

    return tot_sim
    

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

    # Create vocabulary with 100000 words
    # Add to set
    call = ["src/cmu_scripts/make_vocab.sh"]
    for each in os.listdir(PRE_DATA):
      if (each == ".gitignore"):
        continue
      call.append(PRE_DATA + each)
    o=subprocess.call(call)
    if o == 0:
      print "Preprocessed files built."
    else:
      print "failed on vocab creation"
      exit(1)

    f = open("tmp/terms.vocab", "r")
    temp = f.readlines()
    f.close()
    
    vocab = []
  
    for each in temp:
      vocab.append(each.strip())

    # Create a term-document matrix
    corpus = []
    for each in os.listdir(PRE_DATA):
      if (each == '.gitignore'):
        continue
      corpus.append(''.join(open(PRE_DATA + each, "r").read().split('\n')))

    # Create model
    lsa_mod = _lsa_model(vocab, corpus)

    # Pickle model
    output = open(MODEL, 'wb')
    pickle.dump(lsa_mod, output)
    output.close()


  def test(self, data):
    """
      Unpickle model (term-document matrix)
      Treat each test sentence as a document, and calculate similarity
      Write test sentence and resulting score to results file.
    """  
    if self.verbose:
      print "Running lsa script on ", data

    # Load lsa model
    pkl_file = open(MODEL, 'rb')
    lsa_mod = pickle.load(pkl_file)
    pkl_file.close()

    # Prepare test sentences
    o = subprocess.call(["python", "src/prepare_questions.py", "-l", TEST+"Holmes.lm_format.questions.txt", "-mf", TEST+"Holmes.machine_format.questions.txt", "-o", "tmp/questions.txt"])
    if o == 0:
      print "suceeded! Results file created"
    else:
      print "failed on prepare questions"
      exit(1)

    fi = open("tmp/questions.txt", "r")
    fo = open("results/lsa.res",   "w")

    for line in fi:
      print line
      t_word     = line.split('\t')[2].strip()
      t_sentence = line.split('\t')[0].split('>')[1].split('<')[0].strip()

      score = lsa_mod.cos_similarity(t_sentence, t_word)

      fo.write(line.split('\t')[0].strip() + '\t' + str(score) + "\n")

    fi.close()
    fo.close()



  def evaluate(self, results):
    if self.verbose:
      print "Running evaluate script"

    o = subprocess.call(["src/evaluate.sh", "results/lsa.res"])
    
    if o == 0:
      print "suceeded! Evaluation complete"
    else:
      print "failed!"

    


