#!/usr/bin/python
import os
import sys
import argparse
import nltk

from os import path

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

    in_file.close()

    content = content.replace('\r\n', ' ')
    out_file.write(content)
    out_file.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="input", required=True, nargs="*", help="Input file names")
    parser.add_argument('-o', '--outputdir', dest="output_dir", required=True, nargs=1, help="Output dir")
    
    args            = parser.parse_args()
    files           = args.input
    
    output_dir      = args.output_dir[0]

    for file in files:
        if path.isfile(file):
            file_name = path.basename(file)
            out_file = path.join(output_dir, file_name)
            print 'Processing %s' % file
            preprocess_text(file, out_file)

