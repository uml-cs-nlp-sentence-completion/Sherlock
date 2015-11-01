#! /bin/bash
#
#
# Description: This script represents the simple 4-gram model specified in the
# MSR Sentence Completion Challenge. This evaluates the sentences in following
# way: Given the binary language model, the score of the sentence (initialized
# to zero) is incremented once for each bigram match, twice for each trigram
# match, and three times for each four-gram match. Where a match means that the
# test sentence contains the target word at least once in the background data.
#

echo $@

#cat a.text | text2wfreq | wfreq2vocab -top 20000 > a.vocab
#cat a.text | text2idngram -vocab a.vocab | \
#   idngram2lm -vocab a.vocab -idngram - \
#      -binary a.binlm -spec_num 5000000 15000000
#      echo "perplexity -text b.text" | evallm -binary a.binlm
