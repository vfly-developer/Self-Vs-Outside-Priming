# Self-Vs-Outside-Priming

## Purpose
This is a directed research project under the lead of Professor Martin van Schijndel and the C.Psyd Research Lab at Cornell University.
We hope to be able to better understand factors that go towards priming a code-switch as well as investigating the differences seen by an outside prime vs a self prime. Currently, the main factors focused on in the code are distance from a previous codeswitch, and the 
existance of nearby cognates in a nearby (or the same) clause. The project is currently drawing data from the Miami Bangor corpus for 
billingual English-Spanish speakers and may expand for use on other corpora as well. 

## Method
The project uses a mix of basic data manipulation done within Python to prepare for the statistical analysis done with the help of the
Pandas and Matplotlib libraries. The code currently takes in .tsv files, formatted in the guidelines stated on the Miami Bangor corpus website for their English-Spanish transcriptions, and converts them to easily readible "printout" files that show the average utterance
distance between priming codeswitches for the respective speakers in a file. These printout files are then fed into the plotting script which strips away all the information regarding speaker to purely plot out the data points in (currently) a box plot. 

## Current Plans
I hope to be able to implement the effect cognates have on the codeswitch as well by investigating the prevalence of a nearby cognate to a codeswitch. I'm currently using the cognates_en_es.csv file that is available publicly on https://github.com/vsoto/cognates_en_es and will be referencing them at the end using the requested citations. I also hope to do an even greater indepth analysis on the current files (and most likely find more) to have a more well-tested conclusion regarding these types of priming. 

## Thanks
Thank you to Professor Marten van Schijndel and the C.Pysd Research Lab for leading me and guiding me through the process of exploring and researching about a topic I'm interested in. I would honestly have had no clue where to start if not for their direction, specifically Professor Marten's. 

## Citations
The Role of Cognate Words, POS Tags and Entrainment in Code-Switching; Soto, Victor and Cestero, Nishmar and Hirschberg, Julia; Proc. Interspeech 2018; 1938--1942; 2018

Improving Code-Switched Language Modeling Performance Using Cognate Features; Soto, Victor and Hirschberg, Julia; Proc. Interspeech; 2019

Bangor Miami corpus - http://bangortalk.org.uk/speakers.php?c=miami

### Any advice or suggestions are greatly appreciated! Please feel free to fork this project to work on your own version of it and mess around with it!
