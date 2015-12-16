#! /bin/bash

#
# install.sh
#

cd data/

wget http://research.microsoft.com/en-us/um/people/gzweig/Pubs/MSR_Sentence_Completion_Challenge_V1.tgz

tar -zxf MSR_Sentence_Completion_Challenge_V1.tgz

wget http://research.microsoft.com/en-us/um/people/gzweig/Pubs/Holmes_Training_Data.tgz

tar -zxf Holmes_Training_Data.tgz

rm *.tgz

cd ../bin

wget http://www.speech.cs.cmu.edu/SLM/CMU-Cam_Toolkit_v2.tar.gz

tar -zxf CMU-Cam_Toolkit_v2.tar.gz

rm *.gz

cd CMU-Cam_Toolkit_v2/src
sed -i 's/#BYTESWAP_FLAG  = -DSLM_SWAP_BYTES/BYTESWAP_FLAG  = -DSLM_SWAP_BYTES/' Makefile

make install

cd ../../../


