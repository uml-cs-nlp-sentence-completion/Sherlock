#!/usr/bin/python
import os
import sys
import argparse
import nltk
import commands

from os import path

OUTPUT_DIR = './preprocessed'
end_end_tags = ["End of Project Gutenberg's Etext", "End of Project Gutenberg Etext"]

def preprocess_text(input_path, output_path):
    end_tag = "*END*"
    has_seen_end_tag = False
    
    content = ""
    in_file = open(input_path)
    out_file = open(output_path, 'w')
    
    for line in in_file:
        if not has_seen_end_tag:
            if end_tag not in line:
                continue
            else:
                has_seen_end_tag = True
                continue
        if end_end_tags[0] in line or end_end_tags[1] in line:
            continue
        if not line.strip():  # remove empty lines
            continue
        content = content + line

    content = content.strip().replace('\r\n', ' ')
    out_file.write(content)
    out_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="input", required=True, nargs="*", default="all", help="Input file names")
    
    args            = parser.parse_args()
    all_files       = args.input
    for file in all_files:
        if path.isfile(file):
            file_name = path.basename(file)
            out_file = path.join(OUTPUT_DIR, file_name)
            print 'Processing %s' % file
            preprocess_text(file, out_file)

