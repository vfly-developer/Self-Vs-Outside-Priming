import csv

eng_cognates = []
esp_cognates = []

with open("cognates_en_es.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for idx, line in enumerate(csvreader):
        if idx != 0:
            eng_cognates.append(line[0])
            esp_cognates.append(line[1])

print(eng_cognates)
print(esp_cognates)