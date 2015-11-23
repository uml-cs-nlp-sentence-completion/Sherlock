#!/bin/bash

indir=$1
outdir=$2

if [[ $# -ne 2 ]]
then
    echo "usage: sentencifiy.sh input_dir output_dir"
else
    for file in $indir/*
        do
            if [[ -f $file ]]; then
                base_file=${file##*/}
                opennlp SentenceDetector en-sent.bin < $file | opennlp TokenizerME en-token.bin > $outdir/$base_file
            fi
        done
fi
