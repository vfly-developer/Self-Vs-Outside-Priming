import pandas as pd
from os import listdir, makedirs, walk
from os.path import isfile, join, dirname
import matplotlib.pyplot as plt
import sys
import re

# root directory we want to extract all the files from (in this case Printoht)
root = sys.argv[1]

# initializes dictionary to later turn into Dataframe for pandas
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
    # Prune all contents in the printouts to be purely statistical data we need
    for line in contents:
        alpha = re.sub('[^a-zA-Z]+', '', line)
        if alpha == "Self" or alpha == "Outside":
            pruned.append(alpha)
        else:
            test = re.findall('\d*\.?\d+', line)
            if test:
                pruned.append(test[0])
    # Separates the stats into that of Self vs Outside 
    curr = "Self"
    for prune in pruned[1:]:
        if prune == "Outside":
            curr = prune
        else:
            d[curr].append(float(prune))

# Finds the average of each list to allow for comparison
def find_avg(list):
    sum = 0
    count = 0
    for entry in list:
        sum += entry
        count += 1
    return (sum/count)

df = pd.DataFrame(data=d)

# Mass comment for different plots I found were useful to look at with regards to the data
'''
df.plot.hist(alpha=0.5)
'''
df.plot.box()

d["Average"] = []
d["Average"].append(find_avg(d["Self"]))
d["Average"].append(find_avg(d["Outside"]))

print(d["Average"])
plt.show()
