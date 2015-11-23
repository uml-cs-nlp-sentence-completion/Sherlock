#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : solution.py
                                                                              
 Creation Date : 01-11-2015
                                                                              
 Last Modified : Sat 21 Nov 2015 11:29:31 AM EST
                                                                              
 Created By : Renan Campos                                                    
                                                                              
 Purpose : Abstract class for solution implementations for the MSR sentence
           completion challenge.                                                            
"""

class Solution:
  """
    This abstract data class defines the basic structure that all the solution
    implementations should follow. Each should override at least the train and
    test methods, although test should generate a consistant list that evaluate
    can use.
  """

  def __init__(self):
    pass

  def train(self):
    """ 
      Train the classifier (if necassary). Default behavior should be to train
      using the 500+ 19th century novels.
      No output.
    """
    pass

  def test(self):
    """
      Test the classifier on the test set.
      Output should be a set of a list [ Sentence, word in question, score]
    """
    pass

  def evaluate(self):
    """
      Calculate the accuracy of the classifier. This will by default call the perl
      script provided by the test data.
    """
    pass

   

