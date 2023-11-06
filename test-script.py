import nltk
import math
import sys

model = sys.argv[1]
test = sys.argv[2]

tokenized = {}
uni_phi = {}
bi_phi = {}
bi_lambda = {}
tri_phi = {}
tri_lambda = {}
trigrams = {}
seen_words = []

with open(model, "r") as f:
    s = f.readlines()
    for line in s:
        spl = line.split()
        if len(spl) == 2:
            uni_phi.update({(spl[1]): float(spl[0])})
            seen_words.append(spl[1])
        elif len(spl) == 4:
            bi_phi.update({(spl[1], spl[2]): float(spl[0])})
            bi_lambda.update({spl[1]: float(spl[3])})
        elif len(spl) == 5:
            tri_phi.update({(spl[1], spl[2], spl[3]): float(spl[0])})
            tri_lambda.update({(spl[1], spl[2]): float(spl[4])})

with open(test, "r")  as f:
    s = f.read()
    s = s.lower()
    new_s = ""
    for char in s:
        if char == "\n":
            new_s += " "
        else:
            new_s += char
    sentences = nltk.tokenize.sent_tokenize(new_s)
    tokenized = [(nltk.tokenize.word_tokenize(t)) for t in sentences]

words = 0
first_three = []
for idx1, sentence in enumerate(tokenized):
    for idx, word in enumerate(sentence):
        if not word in seen_words:
            sentence[idx] = "<unk>"
        words += 1
    sentence.insert(0, "<s>")
    sentence.append("</s>")
    if(idx1 < 3):
        first_three.append(sentence)


for sentence in tokenized:
    for idx, word in enumerate(sentence):
        if(idx == 0):
            tup = ("<s>", sentence[idx], sentence[idx+1])
            if not tup in trigrams:
                trigrams.update({tup: 1})
            elif tup in trigrams:
                trigrams[tup] += 1
        elif(idx < len(sentence)-1):
            tup = (sentence[idx-1], sentence[idx], sentence[idx+1])
            if not tup in trigrams:
                trigrams.update({tup: 1})
            elif tup in trigrams:
                trigrams[tup] += 1

perplexity = 0
n = 0
for (x, y, z) in trigrams:
    n += trigrams[(x, y, z)]

def calcSurprisal(x,y,z,a):
    if a == 1:
        factor = -1
    else:
        factor = -trigrams[(x, y, z)]
    if (x,y,z) in tri_phi:
        surprise = factor * math.log2(tri_phi[(x,y,z)] + (tri_lambda[(x,y)] * (bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z]))))
    elif (x,y) in tri_lambda:
        if not (y,z) in bi_phi:
            surprise = factor * math.log2(tri_lambda[(x,y)] * (bi_lambda[y] * uni_phi[z]))
        else:
            surprise = factor * math.log2(tri_lambda[(x,y)] * (bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z])))
    elif (y,z) in bi_phi:
        surprise = factor * math.log2(bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z]))
    elif (y) in bi_lambda:
        surprise = factor * math.log2(bi_lambda[y] * uni_phi[z])
    elif (z) in uni_phi:
        surprise = factor * math.log2(uni_phi[z])
    return surprise

def calcProb(x, y, z, a):
    if(a != 1):
        factor = trigrams[(x, y, z)]
    else:
        factor = 1
    if (x,y,z) in tri_phi:
        prob = factor * (tri_phi[(x,y,z)] + (tri_lambda[(x,y)] * (bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z]))))
    elif (x,y) in tri_lambda:
        if not (y,z) in bi_phi:
            prob = factor * (tri_lambda[(x,y)] * (bi_lambda[y] * uni_phi[z]))
        else:
            prob = factor * (tri_lambda[(x,y)] * (bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z])))
    elif (y,z) in bi_phi:
        prob = factor * (bi_phi[(y,z)] + (bi_lambda[y] * uni_phi[z]))
    elif (y) in bi_lambda:
        prob = factor * (bi_lambda[y] * uni_phi[z])
    elif (z) in uni_phi:
        prob = factor * (uni_phi[z])
    return prob

for (x,y,z) in trigrams:
    surprise = calcSurprisal(x, y, z, 0)
    perplexity += surprise

surprisal = []
entropy = []
entropy_reduction = []

for sentence in first_three:
    for idx, word in enumerate(sentence):
        if(idx == 0):
            surprisal.append((sentence[idx+1], calcSurprisal("<s>", sentence[idx], sentence[idx+1], 1)))
        elif(idx < len(sentence)-1):
            surprisal.append((sentence[idx+1], calcSurprisal(sentence[idx-1], sentence[idx], sentence[idx+1], 1)))
        
for sentence in first_three:
    for idx, word in enumerate(sentence):
        if(idx != 0 and idx < len(sentence)):
            entrop = 0
            for word in seen_words:
                entrop += (calcProb(sentence[idx-1], sentence[idx], word, 1) * calcSurprisal(sentence[idx-1], sentence[idx], word, 1))
            if(sentence[idx] == "</s>"):
                entrop = 0
            entropy.append((sentence[idx], entrop))

for idx, (x,y) in enumerate(entropy):
    if(idx == 0):
        entropy_reduction.append(max(0, -entropy[idx][1]))
    else:
        if(x == "</s>"):
            entropy_reduction.append(0)
        else:
            entropy_reduction.append(max(0, entropy[idx-1][1] - entropy[idx][1]))

print("a)" + '\n' + "Perplexity: " + str(2 ** (perplexity / n)))
print("b) \nword surprisal entropy entropy-reduction")
for idx, word in enumerate(surprisal):
    print(str(surprisal[idx][0]) + " " + str(surprisal[idx][1]) + " " + str(entropy[idx][1]) + " " + str(entropy_reduction[idx])) 