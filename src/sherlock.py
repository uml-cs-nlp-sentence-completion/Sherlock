#! /usr/bin/env python

"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : sherlock.py
                                                                              
 Creation Date : 01-11-2015
                                                                              
 Last Modified : Mon 23 Nov 2015 12:28:33 AM EST
                                                                              
 Created By : Renan Campos                                                    
                                                                              
 Purpose : Runs various solutions for the MSR sentence completion challenge. For
           each different solution, add a new flag. This program will train, 
           test and evaluate the results of that implementation.

           This program assumes that the training data is located in the
           Sherlock/data directory, and that necassary binaries are located in
           Sherlock/bin. 
"""


import sys
import argparse

from solution import Solution

def main():

  sol = Solution()
 
  # Sherlock Specific arguments
  parser = argparse.ArgumentParser(description="Trains, tests and evaluates \
                                                several different solutions \
                                                to the MSR sentence \
                                                completion challenge.")
  parser.add_argument( "--train-only", action="store_true", dest="model",
                       default=False, help="Only train model." )                      
  parser.add_argument( "--test-only", action="store", dest="model",
                       default="None", help="Test on given model." )
#  parser.add_argument( "--training-data", dest="train_set", nargs="*",
#                       default="None", help="List of training data" )
#  parser.add_argument( "--test-data", dest="test_set", nargs="*",
#                       default="None", help="List of test data" )


  # Solution flags
  parser.add_argument( "--simple-ngram", action="store_true", default=False,
                       help="Simple-ngram model description here.")
  args = parser.parse_args()

  if (args.simple_ngram):
    # Do simple ngram program
    pass

  else:
   sys.stderr.write("ERROR: No flag specified\n\n")
   parser.print_help()
   sys.exit()

   sol.train()

   sol.test()

   sol.evaluate()

if __name__ == "__main__":
  main()
