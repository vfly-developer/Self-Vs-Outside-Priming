import pandas as pd
from os import listdir, makedirs, walk
from os.path import isfile, join, dirname
import matplotlib.pyplot as plt
import sys
import re

root = sys.argv[1]

d = {}
d["Self"] = []
d["Outside"] = []
all_files = []

for path, subdirs, files in walk(root):
    for name in files:
        all_files.append(join(path, name))

for file in all_files:
    contents = []
    self = True
    with open(file, "r") as f:
        contents = [line.replace('\n', '') for line in f.readlines()]
    pruned = []
    for line in contents:
        alpha = re.sub('[^a-zA-Z]+', '', line)
        if alpha == "Self" or alpha == "Outside":
            pruned.append(alpha)
        else:
            test = re.findall('\d*\.?\d+', line)
            if test:
                pruned.append(test[0])

    #print(pruned) 
    curr = "Self"
    for prune in pruned[1:]:
        if prune == "Outside":
            curr = prune
        else:
            d[curr].append(float(prune))

#print(data["Self"])
#print(data["Outside"])

def find_avg(list):
    sum = 0
    count = 0
    for entry in list:
        sum += entry
        count += 1
    return (sum/count)

df = pd.DataFrame(data=d)

'''
df.plot.hist(alpha=0.5)
df.plot.box()
'''

d["Average"] = []
d["Average"].append(find_avg(d["Self"]))
d["Average"].append(find_avg(d["Outside"]))

print(d["Average"])


plt.show()


#print(df.dtypes)