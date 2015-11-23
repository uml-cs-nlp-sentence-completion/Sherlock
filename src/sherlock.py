"""                                                                              
 Copyright Renan Campos 2015                                                  
                                                                              
 File Name : sherlock.py
                                                                              
 Creation Date : 01-11-2015
                                                                              
 Last Modified : Mon 23 Nov 2015 05:37:53 PM EST
                                                                              
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
from simple_4gram import simple_4gram

TRAINING_DATA = "data/Holmes_Training_Data/*.TXT"

TEST_DATA = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.lm_format.questions.txt"

EVAL_DATA = \
"data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.lm_format.answers.txt"

def main():

  sol = Solution()
 
  # Sherlock Specific arguments
  parser = argparse.ArgumentParser(description="Trains, tests and evaluates \
                                                several different solutions \
                                                to the MSR sentence \
                                                completion challenge.")
  parser.add_argument( "--train-only", action="store_true", dest="train",
                       default=False, help="Only train model." ) 
  parser.add_argument( "--test-only", action="store", dest="model",
                       default=None, help="Test on given model." )
  parser.add_argument( "--eval-only", action="store_true", dest="eval_only",
                       default=False, help="Only evaluate data" )
  parser.add_argument( "-v", "--verbose", action="store_true", dest="v",
                       default=False, help="Display debugging info" )
#  parser.add_argument( "--training-data", dest="train_set", nargs="*",
#                       default="None", help="List of training data" )
#  parser.add_argument( "--test-data", dest="test_set", nargs="*",
#                       default="None", help="List of test data" )


  # Solution flags
  parser.add_argument( "--simple-ngram", action="store_true", default=False,
                       help="Simple-ngram model description here.")

  args = parser.parse_args()

  if (args.simple_ngram):
    sol = simple_4gram(args.v) 
  else:
    sys.stderr.write("ERROR: No flag specified\n\n")
    parser.print_help()
    sys.exit()

  if args.model == None and not args.eval_only:
    print "train"
    sol.train(TRAINING_DATA)

  if not args.train and not args.eval_only:
   print "test"
   sol.test(TEST_DATA)

  if not args.train and args.model == None:
   print "eval"
   sol.evaluate(EVAL_DATA)

if __name__ == "__main__":
  main()
