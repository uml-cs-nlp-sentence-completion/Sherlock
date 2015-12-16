# Sherlock
MSR sentence completion challenge implementation.

This has been developed using python on MAC OS X

Requirements:
    python nltk - Installation instruction can be found at http://www.nltk.org/install.html
    python sklearn - Installation instruction can be found at http://scikit-learn.org/stable/install.html
    Python implementaion of Word2Vec - Installation instruction can be found at http://radimrehurek.com/gensim/install.html
    CMU Language Modeling toolkit : http://www.speech.cs.cmu.edu/SLM/toolkit.html

Installation:
    Run Install script
    
Data Set: Training and Test data set can be downloaded from the following link,
        https://www.dropbox.com/sh/j6a93xsj0efp6p7/AABJSXiU9nWz8t_QDX3C0kwla?dl=0.
        Please extract the the files and copy them into data folder under root directory.


Running Instruction:
    Run sherlock script from root directory. It will run all the algorithms. Each algorithm can be run separately. Please see below for usage examples.

Example Usage:
    
    $./sherlock - this will run all the algorithms

    $./sherlock --simple_4gram : This will run only simple 4-gram model including training, testing, and evaluation 
    $./sherlock --simple_4gram --train-only : This only train the simple 4-gram model 
    $./sherlock --simple_4gram --test-only model : This will only test the model and will save the results into results folder
    $./sherlock --simple_4gram --eval-only : This will run evaluation.

    $./sherlock --smoothed_3gram : This will run only smoothed 3-gram model including training, testing, and evaluation 
    $./sherlock --smoothed_3gram --train-only : This only train the smoothed 3-gram model 
    $./sherlock --smoothed_3gram --test-only model : This will only test the model and will save the results into results folder
    $./sherlock --smoothed_3gram --eval-only : This will run evaluation.

    $./sherlock --smoothed_4gram : This will run only smoothed 4-gram model including training, testing, and evaluation 
    $./sherlock --smoothed_4gram --train-only : This only train the smoothed 4-gram model 
    $./sherlock --smoothed_4gram --test-only model : This will only test the model and will save the results into results folder
    $./sherlock --smoothed_4gram --eval-only : This will run evaluation.

    $./sherlock --skipgram : This will run only skip gram model including training, testing, and evaluation 
    $./sherlock --skipgram --train-only : This only train the skip gram model 
    $./sherlock --skipgram --test-only sg_model : This will only test the model and will save the results into results folder
    $./sherlock --skipgram --eval-only : This will run evaluation.








