import sys
from os import listdir, makedirs
from os.path import isfile, join, dirname
import csv

# folder path for the files we want to run the script on
def prune_files(path, file):
    init = 1
    utterances = []
    utterances.append([])

    with open(join(path, file), "r") as f:
        # breaks up file into utterances using the utterance_id found in the tsv
        for idx, line in enumerate(f.readlines()[1:]):
            stripped = line.replace('\n', '').split('\t')
            try:
                if int(stripped[1]) != init: 
                    utterances.append([])
                    init = int(stripped[1])
                utterances[init-1].append((stripped[3], stripped[8], stripped[9]))
            except IndexError:
                # this is only here to skip the last row which denotes the number of rows
                pass

    # transforms the current un-altered list of utterances to a summarized version
    # summarized keeps track of whether a codeswitch happened, the language the
    # utterance switched to, the speaker, and the index of where you can find it
    # inside the tsv.  
    utterances_length = len(utterances)
    summarized = []
    cs_total = 0
    mult_cs = 0
    accounted = False
    sum = 0
    speakers = []
    for idx1, utterance in enumerate(utterances):
        code_switch = False
        lang = "" 
        speaker = utterance[0][1]
        # keeps track of number of speakers
        if not speaker in speakers:
            speakers.append(speaker)
        for idx2, tup in enumerate(utterance):
            if idx2 == 0:
                lang = tup[2]
            else:
                if lang == "eng&spa" and tup[2] != "eng&spa" and tup[2] != "999":
                    lang = tup[2]
                if lang != tup[2] and tup[2] != "eng&spa" and lang != "eng&spa" and tup[2] != "999":
                    if code_switch and not accounted:
                        mult_cs += 1
                        accounted = True
                    else:
                        code_switch = True
                    cs_total += 1
        word = utterance[0][0]
        summarized.append((code_switch, lang, speaker, idx1, 0, word))
        sum += len(utterance) - 1 # accounting for ending punctuation
    avg_utterance_length = sum / utterances_length

    # keeps track of utterances made by the same person in a row into one utterance cluster
    i = 0
    prev = summarized[0][2]
    for idx, line in enumerate(summarized[1:]):
        if line[2] != prev:
            prev = line[2]
            i += 1
        list_line = list(line)
        list_line[4] = i
        summarized[idx+1] = tuple(list_line)
    return summarized, speakers, avg_utterance_length, file

# returns cognates found in csv file "cognates_en_es.csv"
def get_cognates(file):
    eng_cognates = []
    esp_cognates = []

    with open(file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for idx, line in enumerate(csvreader):
            if idx != 0:
                eng_cognates.append(line[0])
                esp_cognates.append(line[1])
    return eng_cognates, esp_cognates
# Bank of printout statements for quick testing if needdd
'''
print(last_codeswitches)
print(sum_and_counts_self_prime)
print(sum_and_counts_outside_prime)

print(sum_and_counts_outside_prime[0][0]/sum_and_counts_outside_prime[0][1])
print(sum_and_counts_outside_prime[1][0]/sum_and_counts_outside_prime[1][1])

print(speakers)
print(summarized)
print(cs_in_collapsed)
print(outside_priming)
print(self_priming)
print(cs_total)
print(mult_cs)
print(utterance[0])
print(len(utterances))
print(avg_utterance_length)
'''
