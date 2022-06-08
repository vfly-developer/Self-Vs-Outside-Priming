import sys
import numpy as np
from os import listdir
from os.path import isfile, join
import math
import re

path = sys.argv[1]

def exec(file):
    init = 1
    utterances = []
    utterances.append([])

    with open(file, "r") as f:
        for idx, line in enumerate(f.readlines()[1:]):
            stripped = line.replace('\n', '').split('\t')
            #print(stripped)
            try:
                if int(stripped[1]) != init: 
                    utterances.append([])
                    init = int(stripped[1])
                utterances[init-1].append((stripped[3], stripped[8], stripped[9]))
            except IndexError:
                # this is only here to check the last row which denotes the number of rows
                pass

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
        for idx2, word in enumerate(utterance):
            if idx2 == 0:
                lang = word[2]
            else:
                if lang == "eng&spa" and word[2] != "eng&spa" and word[2] != "999":
                    lang = word[2]
                if lang != word[2] and word[2] != "eng&spa" and lang != "eng&spa" and word[2] != "999":
                    if code_switch and not accounted:
                        mult_cs += 1
                        accounted = True
                    else:
                        code_switch = True
                    cs_total += 1
        summarized.append((code_switch, lang, speaker, idx1, 0))
        sum += len(utterance) - 1 # accounting for ever-prevalent ending punctuation
    avg_utterance_length = sum / utterances_length

    #TODO: sentence parsing

    # allows you to check whether if the preceding utterance of a speaker was a code-switch or it
    # or if you had a code-switch from the same speaker in the second to last utterance 
    # find distance to most recent code-switch to yourself vs not yourself 
    # apply cognatal priming to the set of features later as well 

    # later on -> maybe also try to find a way to split by sentence using a sentence tokenizer
    # ie first collapsing into utterance cluster and then using the sentence tokenizer on it

    #collapses summarizes by same person in a row into one list
    i = 0
    prev = summarized[0][2]
    for idx, line in enumerate(summarized[1:]):
        if line[2] != prev:
            prev = line[2]
            i += 1
        list_line = list(line)
        list_line[4] = i
        summarized[idx+1] = tuple(list_line)

    # check to see self-priming from close-by utterances 

    self_priming = 0
    outside_priming = 0

    codeswitched = []
    cs_in_collapsed = 0

    # fix this to work with new melting

    last_codeswitches = []
    sum_and_counts_self_prime = []
    sum_and_counts_outside_prime = []
    last_switch_speaker = -1
    # tuple of line number, utterance number, distance between code switch, number of cs
    for i in range(len(speakers)):
        last_codeswitches.append((-1, -1))
        sum_and_counts_self_prime.append((0,0))
        sum_and_counts_outside_prime.append((0,0))
    for line in summarized:
        if line[0] == True:
            speaker = line[2]
            speaker_idx = speakers.index(speaker)
            
            if last_codeswitches[speaker_idx][0] != -1:
                if speaker_idx == last_switch_speaker:
                    new_sum = sum_and_counts_self_prime[speaker_idx][0] + (line[3] - last_codeswitches[speaker_idx][0])
                    new_count = sum_and_counts_self_prime[speaker_idx][1] + 1
                    sum_and_counts_self_prime[speaker_idx] = (new_sum, new_count)
                elif speaker_idx != last_switch_speaker:
                    new_sum = sum_and_counts_outside_prime[speaker_idx][0] + (line[3] - last_codeswitches[last_switch_speaker][0])
                    new_count = sum_and_counts_outside_prime[speaker_idx][1] + 1
                    sum_and_counts_outside_prime[speaker_idx] = (new_sum, new_count)

            last_codeswitches[speaker_idx] = (line[3], line[4])
            last_switch_speaker = speaker_idx

    #print out avg length between self and outside priming code switches

    save_path = "/Printout"
    file_name = file.split(".")[0]
    with open(file_name, "w") as f:
        f.write("Self:\n")
        for idx, tup in enumerate(sum_and_counts_self_prime):
            sum = tup[0]
            count = tup[1]
            if sum != 0:
                f.write("Speaker: " + str(speakers[idx]) + " - Avg: " + str(sum / count / avg_utterance_length) + "\n")
            else:
                f.write("Speaker: " + str(speakers[idx]) + " - Avg: N/A\n")
        f.write("\n")
        f.write("Outside:\n")
        for idx, tup in enumerate(sum_and_counts_outside_prime):
            sum = tup[0]
            count = tup[1]
            if sum != 0:
                f.write("Speaker: " + str(speakers[idx]) + " - Avg: " + str(sum / count / avg_utterance_length) + "\n")
            else:
                f.write("Speaker: " + str(speakers[idx]) + " - Avg: N/A\n")

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for file in onlyfiles:
    exec(join(path, file))
'''
for collapse in collapsed:
    occurences = 0
    for line in collapse:
        if line[0] == True:
            occurences += 1
    if occurences > 1:
        self_priming += 1
    codeswitched.append((occurences > 0))
    if occurences > 0:
        cs_in_collapsed += 1 

for idx, codeswitch in enumerate(codeswitched[1:]):
    if codeswitched[idx] == True and codeswitch:
        outside_priming += 1
'''




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
