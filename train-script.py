import nltk
import sys

def countEntry(dict):
    d = {}
    for entry in dict:   
        d.update({entry: len(dict[entry])})
    return d

train = sys.argv[1]
valid = sys.argv[2]

DELTA = 0.75
train_tokenized = []
valid_tokenized = []
trigram_counts = {}

seen_words = {}

def prep(file):
    with open(file, "r", encoding="utf-8")  as f:
        s = f.read()
        s = s.lower()
        new_s = ""
        for char in s:
            if char == "\n":
                new_s += " "
            elif char != "=":
                new_s += char
        sentences = nltk.tokenize.sent_tokenize(new_s)
        dest = [(nltk.tokenize.word_tokenize(t)) for t in sentences]
        return dest

train_tokenized = prep(train)
valid_tokenized = prep(valid)

for sentence in train_tokenized:
    for word in sentence:
        if not word in seen_words:
            seen_words.update({word: 1})
        else:
            seen_words[word] += 1
    sentence.insert(0, "<s>")
    sentence.append("</s>")

seen_words.update({"<unk>": 0})

for sentence in valid_tokenized:
    for idx, word in enumerate(sentence):
        if not word in seen_words:
            seen_words["<unk>"] += 1
            sentence[idx] = "<unk>"
        else:
            seen_words[word] += 1
    sentence.insert(0, "<s>")
    sentence.append("</s>")

final_tokenized = train_tokenized + valid_tokenized

trigrams = {}
end_tri = {}
beg_tri = {}
mid_tri = {} 
bigrams = {}
end_bi = {}
beg_bi = {}

for sentence in final_tokenized:
    for idx, word in enumerate(sentence):
        if(idx == 0):
            tup = ("<s>", sentence[idx], sentence[idx+1])
            tri_end = ("<s>", sentence[idx])
            tri_beg = (sentence[idx], sentence[idx+1])
            tri_mid = (sentence[idx])
            bi_tup = (sentence[idx], sentence[idx+1])
            bi_placeholder = ("<s>", "<s>")
            bi_beg = (sentence[idx+1])
            bi_end = (sentence[idx])
            
            if not tup in trigrams:
                trigrams.update({tup: 1})
            elif tup in trigrams:
                trigrams[tup] += 1
            if not tri_beg in beg_tri:
                beg_tri.update({tri_beg: [sentence[idx]]})
            elif tri_beg in beg_tri:
                if not sentence[idx] in beg_tri[tri_beg]:
                    beg_tri[tri_beg].append(sentence[idx])
            if not tri_mid in mid_tri:
                mid_tri.update({tri_mid: [(sentence[idx], sentence[idx+1])]})
            elif tri_mid in mid_tri:
                if not (sentence[idx], sentence[idx+1]) in mid_tri[tri_mid]:
                    mid_tri[tri_mid].append((sentence[idx], sentence[idx+1]))
            if not tri_end in end_tri:
                end_tri.update({tri_end: [sentence[idx+1]]})
            elif tri_end in end_tri:
                if not sentence[idx+1] in end_tri[tri_end]:
                    end_tri[tri_end].append(sentence[idx+1])
            if not bi_tup in bigrams:
                bigrams.update({bi_tup: 1})
            elif bi_tup in bigrams:
                bigrams[bi_tup] += 1
            if not bi_placeholder in bigrams:
                bigrams.update({bi_placeholder: 1})
            elif bi_placeholder in bigrams:
                bigrams[bi_placeholder] += 1
            if not bi_beg in beg_bi:
                beg_bi.update({bi_beg: [sentence[idx]]})
            elif bi_beg in beg_bi:
                if not sentence[idx] in beg_bi[bi_beg]:
                    beg_bi[bi_beg].append(sentence[idx])
            if not bi_end in end_bi:
                end_bi.update({bi_end: [sentence[idx+1]]})
            elif bi_end in end_bi:
                if not sentence[idx+1] in end_bi[bi_end]:
                    end_bi[bi_end].append(sentence[idx+1])
        elif(idx < len(sentence)-1):
            tup = (sentence[idx-1], sentence[idx], sentence[idx+1])
            tri_beg = (sentence[idx], sentence[idx+1])
            tri_end = (sentence[idx-1], sentence[idx])
            tri_mid = (sentence[idx])
            bi_tup = (sentence[idx], sentence[idx+1])
            bi_beg = (sentence[idx+1])
            bi_end = (sentence[idx])
            if not tup in trigrams:
                trigrams.update({tup: 1})
            elif tup in trigrams:
                trigrams[tup] += 1
            if not tri_beg in beg_tri:
                beg_tri.update({tri_beg: [sentence[idx-1]]})
            elif tri_beg in beg_tri:
                if not sentence[idx-1] in beg_tri[tri_beg]:
                    beg_tri[tri_beg].append(sentence[idx-1])
            if not tri_mid in mid_tri:
                mid_tri.update({tri_mid: [(sentence[idx-1], sentence[idx+1])]})
            elif tri_mid in mid_tri:
                if not (sentence[idx-1], sentence[idx+1]) in mid_tri[tri_mid]:
                    mid_tri[tri_mid].append((sentence[idx-1], sentence[idx+1]))
            if not tri_end in end_tri:
                end_tri.update({tri_end: [sentence[idx+1]]})
            elif tri_end in end_tri:
                if not sentence[idx+1] in end_tri[tri_end]:
                    end_tri[tri_end].append(sentence[idx+1])
            if not bi_tup in bigrams:
                bigrams.update({bi_tup: 1})
            elif bi_tup in bigrams:
                bigrams[bi_tup] += 1
            if not bi_end in end_bi:
                end_bi.update({bi_end: [sentence[idx+1]]})
            elif bi_end in end_bi:
                if not sentence[idx+1] in end_bi[bi_end]:
                    end_bi[bi_end].append(sentence[idx+1])
            if not bi_beg in beg_bi:
                beg_bi.update({bi_beg: [sentence[idx]]})
            elif bi_beg in beg_bi:
                if not sentence[idx] in beg_bi[bi_beg]:
                    beg_bi[bi_beg].append(sentence[idx])

count_beg_tri = countEntry(beg_tri)
count_mid_tri = countEntry(mid_tri)
count_end_tri = countEntry(end_tri)
count_beg_bi = countEntry(beg_bi)
count_end_bi = countEntry(end_bi)
len_bi = len(bigrams) - 1
len_tri = len(trigrams)

unigrams_phi = {}
bigrams_delta = {}
bigrams_phi = {}
trigrams_delta = {}
trigrams_phi = {}

for entry in count_beg_bi:
    unigrams_phi.update({entry: count_beg_bi[entry] / len_bi})

for (x, y) in bigrams:
    if (y != "<s>"):
        bigrams_delta.update({x: (DELTA / count_mid_tri[x]) * count_end_bi[x]})
        bigrams_phi.update({(x, y): max((count_beg_tri[(x, y)] - DELTA), 0) / count_mid_tri[x]})

for (x, y, z) in trigrams:
    trigrams_delta.update({(x, y): DELTA / bigrams[(x, y)] * count_end_tri[(x, y)]})
    trigrams_phi.update({(x, y, z): max(trigrams[(x, y, z)] - DELTA, 0) / bigrams[x, y]})

with open("ngram.model", "w") as f:
    for unigram in unigrams_phi:
        f.write(str(unigrams_phi[(unigram)]) + " " + unigram + "\n")
    for (x,y) in bigrams_phi:
        f.write(str(bigrams_phi[(x,y)]) + " " + x + " " + y + " " + str(bigrams_delta[(x)]) + "\n")
    for (x,y,z) in trigrams_phi:
        f.write(str(trigrams_phi[(x,y,z)]) + " " + x + " " + y + " " + z + " " + str(trigrams_delta[(x, y)]) + "\n")
