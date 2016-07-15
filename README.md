# genalex2ima2
python2.7 code that makes a genalex file into an sqlite database, and then produces infiles for ima2 from the database

This repository contains two sets of python code:
- micsatgenalex2db.py for taking data from a GenAlEx csv file and making it into an SQlite database.
- micsatdb2ima2.py for taking data from the SQlite database and making it into an X number of input files for IMa2 or IMa2p
  (pairwise sample comparisons, all possible pairs)

Test files 
- test.csv a tiny data set for making the database
- testout.sqlite the resulting database after running micsatgenalex2db.py on test.csv

What you will need to run the software:
- python (tested only on v2.7) (python comes already installed on linux and mac, on windows you will need to install it manually)
- sqlite (tested only on version 3.8.0)

Some notes
- only one mutation rate of 0.002 is added to all loci
- loci are only included if they have 20 or more alleles scored for a sample
- all alleles scored as 0 are excluded
- smallest allele (often 0) is coded as nrepeats=5
- subsequent alleles are coded as nrepeats=6, 7, etc., disregarding their actual length (e.g., a locus with lengths 0, 200, 204, 205, 206 will be coded as nrepeats 5, 6, 7, 8, 9)
- feel free to adjust the code to your needs!
