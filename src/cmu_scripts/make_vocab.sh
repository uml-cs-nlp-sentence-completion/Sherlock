#! /bin/bash
#
# Create a vocabulary file with the top 100000 words

CMU_DIR="bin/CMU-Cam_Toolkit_v2/bin"
TMP_DIR="tmp"

cat $@ | $CMU_DIR/text2wfreq | $CMU_DIR/wfreq2vocab -top 100000 > $TMP_DIR/a.vocab
tail -n+5 $TMP_DIR/a.vocab > $TMP_DIR/terms.vocab
rm $TMP_DIR/a.vocab

