import sys
from os import listdir, makedirs
from os.path import isfile, join, dirname

# folder path for the files we want to run the script on
path = sys.argv[1]

def exec(path, file):
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
        sum += len(utterance) - 1 # accounting for ending punctuation
    avg_utterance_length = sum / utterances_length

    #TODO: Comment the CODE!!!! and implement cognates

    # Commentation still needed to be done next time I return to this project, will most likely also try to preprocess the
    # current cognates in the csv into a usable form for the project, will try to do something regarding analysis on the 
    # congates once the commentation of the code is done. 

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

    last_codeswitches = []
    sum_and_counts_self_prime = []
    sum_and_counts_outside_prime = []
    last_switch_speaker = -1
    # last_codeswitches: tuple of line number, utterance number 
    # sum_and_counts_alpha: distance between code switch, number of cs
    for i in range(len(speakers)):
        last_codeswitches.append((-1, -1))
        sum_and_counts_self_prime.append((0,0))
        sum_and_counts_outside_prime.append((0,0))

    # Goes through each line inside of summarized to find instances of priming 
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

    # Prints out resultant averages to the Printout folder, keeping the same path as the data outside of the new directory
    save_path = "Printout"
    file_name = file.split(".")[0] + ".txt"
    final = join(save_path, path, file_name)
    makedirs(dirname(final), exist_ok=True)
    with open(final, "w") as f:
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

# finds all the relevant files within a directory to run the script on
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for file in onlyfiles:
    exec(path, file)


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
