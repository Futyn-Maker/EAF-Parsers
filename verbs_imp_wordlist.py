import csv

with open('verbs_imp.csv', 'r', encoding='utf8') as csvFile:
    wordTable = list(csv.reader(csvFile, delimiter=';'))
wordTable.pop(0)

wordList = {}

for word in wordTable:
    word[2] = word[2].lower()
    if word[2] in wordList:
        value = wordList[word[2]]
        wordList[word[2]] = value + 1
    else:
        wordList[word[2]] = 1
wordArraySorted = sorted(wordList, key=lambda x: int(wordList[x]), reverse=True)

wordTable = [['Lemma', 'Quantity']]
for word in wordArraySorted:
    wordTable.append([word, wordList[word]])

with open('verbs_imp_wordlist.csv', 'w', encoding='utf8', newline='') as outFile:
    writer = csv.writer(outFile, delimiter=';')
    writer.writerows(wordTable)
print('Done!')