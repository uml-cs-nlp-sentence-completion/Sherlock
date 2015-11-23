#! /bin/bash
#
# Author: Renan Campos
# Description: This script represents the simple 4-gram model specified in the
# MSR Sentence Completion Challenge. This evaluates the sentences in following
# way: Given the binary language model, the score of the sentence (initialized
# to zero) is incremented once for each bigram match, twice for each trigram
# match, and three times for each four-gram match. Where a match means that the
# test sentence contains the target word at least once in the background data.
# NOTE: This script should only be called by 'sherlock' from the Sherlock dir.
#

CMU_DIR="bin/CMU-Cam_Toolkit_v2/bin"
TMP_DIR="tmp"
MOD_DIR="models"
RES_DIR="results"

function print_help() {
  echo "ERROR: invalid arguments"
  echo "Examples:"
  echo "script --train <path to training data>"
  echo "script --test <test data>"
  echo "arguments given: " $@
}

function train_data() {
  # Argument should be path to training data
  cat $1* \
  | $CMU_DIR/text2wfreq \
  | $CMU_DIR/wfreq2vocab -top 30000 > $TMP_DIR/$$.vocab \
  && \
  echo "After freq" && \
  cat $1* \
  | $CMU_DIR/text2idngram -n 4 -temp $TMP_DIR/ -vocab $TMP_DIR/$$.vocab \
  | $CMU_DIR/idngram2lm -n 4 -vocab $TMP_DIR/$$.vocab -idngram - \
  -binary $MOD_DIR/Simple4.binlm -spec_num 10000000 100000000 1000000000 \
  && \
  echo "Simple 4-gram model trained successfully"

  rm $TMP_DIR/$$.vocab 
}

function test_data() {
  # This expects argument to be the path to the test file
  # Using the trained language model, this will evaluate each line of the
  # machine format test file (after removing the question number and brackets
  # using sed), then calculate the score using awk.
  count=1
  t_string=""

  echo "Setup..."

  > $RES_DIR/Simple_4gram.res

  while read line
  do
    echo $line | sed 's/.*) \|\[\|\]//g' > $TMP_DIR/$$_$count.txt

    t_string+="perplexity -text $TMP_DIR/$$_$count.txt\n"
    count=$(($count + 1))
  done < $1/Holmes.lm_format.questions.txt

  echo "Computing scores..."

  echo -e $t_string  \
    | $CMU_DIR/evallm -binary $MOD_DIR/Simple4.binlm \
    | grep "Number of" \
    | awk '\
          BEGIN {score=0; weight=3} \
          { \
          score = (score + ($6 * weight)); weight--; \
          if (weight == -1) { print score; weight=3; score=0; } \
          } \
          END {}' \
    > $TMP_DIR/$$_score.txt

  while read line <&3 && read score <&4
  do
    echo -e "$line\t$score" >> $RES_DIR/Simple_4gram.res
  done 3< $1/Holmes.lm_format.questions.txt 4<$TMP_DIR/$$_score.txt

  rm $TMP_DIR/$$*.txt

  echo "Complete. Output in Simple_ngram.res"
}

function check_dir() {
  if [ ! -d "$1" ]
  then
    echo "$1 is not a directory"
    exit 1
  fi
}

if [[ $# -eq 2 ]]
then
  if [ "$1" == "--train" ]
  then
    check_dir $2
    train_data $2
    exit 0
  elif [ "$1" == "--test" ]
  then
    check_dir $2
    test_data $2
    exit 0
  else
    echo $1
    print_help $@
    exit 1
  fi
else
  print_help $@
  exit 1
fi

