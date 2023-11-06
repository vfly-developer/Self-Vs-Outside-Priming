from flair.data import Sentence
from flair.models import SequenceTagger
from pre_process import convert_to_sentences_sentimix, convert_to_sentences_sentiment140, convert_to_sentences_tass2020
import matplotlib.pyplot as plt
import numpy as np

# load tagger
tagger = SequenceTagger.load("flair/upos-multi")

def tag_sentences(sentences):
    tag_count = {}
    for sentence in sentences:
        prep_sentence = Sentence(sentence)
        tagger.predict(prep_sentence)
        
        # iterate over tokens and print the predicted POS label
        for token in prep_sentence:
            token_list = str(token).split(" ")
            word = token_list[1]
            tag = token_list[3]
            
            if tag not in tag_count:
                tag_count[tag] = 1
            else:
                tag_count[tag] += 1

    return tag_count

def key_sort(dict):
    keys = list(dict.keys())
    keys.sort()

    sorted_dict = {i: dict[i] for i in keys}
    return sorted_dict

#spanglish_sentences = convert_to_sentences_sentimix("sentimix2020.txt")
#tag_count = tag_sentences(spanglish_sentences)
spanglish_tag_count = {'ADV': 1963, 'PRON': 3596, 'VERB': 4194, 'NOUN': 4270, 'ADJ': 1186, 'PROPN': 1697, 'ADP': 2073, 'DET': 1833, 'X': 2638, 'AUX': 1175, 'CCONJ': 914, 'SCONJ': 591, 'INTJ': 527, 'PART': 449, 'NUM': 270, 'PUNCT': 3826, 'SYM': 330}
#print(spanglish_tag_count)

#english_sentences = convert_to_sentences_sentiment140("sentiment140.csv")
#english_tag_count = tag_sentences(english_sentences[:10000])
english_tag_count = {'NOUN': 25366, 'PUNCT': 19121, 'X': 759, 'PROPN': 5212, 'INTJ': 2596, 'PRON': 18271, 'AUX': 10559, 'DET': 8342, 'VERB': 21062, 'ADP': 10886, 'PART': 5541, 'ADJ': 9396, 'SCONJ': 1609, 'CCONJ': 4082, 'ADV': 12428, 'NUM': 1883, 'SYM': 552}
#print(english_tag_count)

#spanish_sentences = convert_to_sentences_tass2020("combined_tass2020.tsv")
#spanish_tag_count = tag_sentences(spanish_sentences)
spanish_tag_count = {'ADP': 12982, 'NOUN': 19136, 'PUNCT': 11884, 'PRON': 10155, 'VERB': 20132, 'PROPN': 4934, 'ADV': 8861, 'SCONJ': 5225, 'AUX': 2707, 'CCONJ': 5336, 'DET': 11707, 'NUM': 1251, 'ADJ': 7384, 'X': 1299, 'PART': 46, 'INTJ': 93, 'SYM': 201}
#print(spanish_tag_count)

spanglish_tag_count = key_sort(spanglish_tag_count)
del spanglish_tag_count['X']
del spanglish_tag_count['SYM']
english_tag_count = key_sort(english_tag_count)
del english_tag_count['X']
del english_tag_count['SYM']
spanish_tag_count = key_sort(spanish_tag_count)
del spanish_tag_count['X']
del spanish_tag_count['SYM']


print(spanglish_tag_count)
print(english_tag_count)
print(spanish_tag_count)

# convert to percentages:
def convert_to_percentages(dct, total):
    for key in dct:
        dct[key] /= total

    return dct

spanglish_tag_count = convert_to_percentages(spanglish_tag_count, sum(spanglish_tag_count.values()))
english_tag_count = convert_to_percentages(english_tag_count, sum(english_tag_count.values()))
spanish_tag_count = convert_to_percentages(spanish_tag_count, sum(spanish_tag_count.values()))


x_tag_names = []
english_tag_count_lst = []
spanglish_tag_count_lst = []
spanish_tag_count_lst = []

for key in english_tag_count:
    x_tag_names.append(key)
    english_tag_count_lst.append(english_tag_count[key])
    spanglish_tag_count_lst.append(spanglish_tag_count[key])
    spanish_tag_count_lst.append(spanish_tag_count[key])
  
x_axis = np.arange(len(x_tag_names)) 
  
plt.bar(x_axis - 0.25, english_tag_count_lst, 0.25, label = 'English') 
plt.bar(x_axis, spanglish_tag_count_lst, 0.25, label = 'Spanglish') 
plt.bar(x_axis + 0.25, spanish_tag_count_lst, 0.25, label = 'Spanish') 


plt.xticks(x_axis, x_tag_names) 
plt.xlabel("Language Type") 
plt.ylabel("Percent of Occurrence") 
plt.title("POS Tags Percentage in each Language") 
plt.legend() 
plt.show() 
