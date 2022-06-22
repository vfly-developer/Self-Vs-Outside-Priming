import sys
from os import listdir, makedirs
from os.path import isfile, join, dirname
from pre_process import prune_files, get_cognates

def self_outside_priming(summarized, speakers, avg_utterance_length, file):
    #TODO: ask for advice regarding cognates at meeting tomorrow

    # Commentation still needed to be done next time I return to this project, will most likely also try to preprocess the
    # current cognates in the csv into a usable form for the project, will try to do something regarding analysis on the 
    # congates once the commentation of the code is done. 

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
    return sum_and_counts_self_prime, sum_and_counts_outside_prime, speakers, avg_utterance_length, file

def cognate_priming(eng_cognates, esp_cognates, summarized, speakers):
    # Goes through the summarized utterances to see whether or not there is an effect when cognates are in the nearby vicinity
    # of a cpdeswitch 
    
    for line in summarized:
        lang = line[2]
        word = line[5]
        if lang == 'spa':
            if word in esp_cognates:
                print(word)
        elif lang == 'eng':
            if word in eng_cognates:
                print(word)
    
    #print(summarized)
    pass

def printout(sum_and_counts_self_prime, sum_and_counts_outside_prime, speakers, avg_utterance_length, file):
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

path = sys.argv[1]
cognate_file = sys.argv[2]
# finds all the relevant files within a directory to run the script on
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
eng_cognates, esp_cognates = get_cognates(cognate_file)

for file in onlyfiles:
   res = prune_files(path, file)
 #  printout(self_outside_priming(res))
   cognate_priming(eng_cognates, esp_cognates, res[0], res[1])
   