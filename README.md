# genalex2ima2
python2.7 code that makes a genalex file into an sqlite database, and then produces infiles for ima2 from the database

This repository contains two sets of python code:
- micsatgenalex2db.py for taking data from a GenAlEx csv file and make it into an SQlite database.
- micsatdb2ima2.py for taking data from the SQlite database and making it into an X number of input files for IMa2 or IMa2p
  (pairwise population comparisons, all possible pairs)

Test files 
- test.csv a tiny data set for making the database
- testout.sqlite the resulting database after running micsatgenalex2db.py on test.csv

What you will need to run the software:
- python (tested only on v2.7) (python comes already installed on linux and mac, on windows you will need to install it manually)
- sqlite (tested only on version 3.8.0)

To run on the testfiles, type the following:
>python micsatgenalex2db.py

>python micsatdb2ima2.py
