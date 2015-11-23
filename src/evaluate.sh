#! /bin/bash
#
# Author: Renan Campos
# Description: This script takes a result file and format, then calculates the accuracy
# of the answers. In the results file, out of each five, the one with the
# highest score is considered the correct one. This script figures this out by
# using the bestoffive.pl file provided by the MSR test data. 
#

MSR_DIR=data/MSR_Sentence_Completion_Challenge_V1
TMP=tmp

if [ ! -f "$1" ]
then
  echo "$1 is not a valid file."
  exit 1
fi

cat $1 | $MSR_DIR/bestof5.pl > $TMP/best.temp

$MSR_DIR/score.pl $TMP/best.temp $MSR_DIR/Data/Holmes.lm_format.answers.txt

rm $TMP/best.temp
