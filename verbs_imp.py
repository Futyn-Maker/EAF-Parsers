from bs4 import BeautifulSoup
import re
import csv
import os
import logging
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

table = [['File Name', 'Token', 'Lemma']]

if not os.path.exists('out_verbs_imp'):
    os.mkdir('out_verbs_imp')
if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(filename="logs/errors_verbs_imp.log", filemode="w", level=logging.ERROR)
log = logging.getLogger("ex")

for file in os.listdir('in'):
    singleFileList = ''
    try:
        with open('in/' + file, 'r', encoding='utf8') as eafFile:
            eaf = eafFile.read()
        eaf = eaf.replace('part_of_speech', 'part of speech')
        eaf = eaf.replace('parts_of_speech', 'part of speech')
        eaf = eaf.replace('parts of speech', 'part of speech')
        eaf = BeautifulSoup(eaf, 'xml')

        grammaticalFeatures = eaf.find_all(LINGUISTIC_TYPE_REF=re.compile("(grammatical features)|(gram)|(grammatical_features)"))

        for tier in grammaticalFeatures:
            annotations = tier.find_all('ANNOTATION_VALUE', string=re.compile('Mood=Imp'))
            for annotation in annotations:
                try:
                    id = annotation.parent['ANNOTATION_REF']
                except KeyError:
                    ts1 = annotation.parent['TIME_SLOT_REF1']
                    ts2 = annotation.parent['TIME_SLOT_REF2']
                    id = eaf.select_one('TIER[LINGUISTIC_TYPE_REF="words"] ALIGNABLE_ANNOTATION[TIME_SLOT_REF1="' + ts1 + '"][TIME_SLOT_REF2="' + ts2 + '"]')['ANNOTATION_ID']
                partSpeech = eaf.select_one('TIER[LINGUISTIC_TYPE_REF="part of speech"] REF_ANNOTATION[ANNOTATION_REF="' + id + '"] ANNOTATION_VALUE')
                if partSpeech == None:
                    partSpeech = eaf.select_one('TIER[LINGUISTIC_TYPE_REF="part of speech"] REF_ANNOTATION[ANNOTATION_ID="' + id + '"] ANNOTATION_VALUE')
                    id = partSpeech.parent['ANNOTATION_REF']
                if partSpeech.string == 'VERB':
                    token = eaf.find(ANNOTATION_ID=id).ANNOTATION_VALUE.string
                    table.append([file, token, morph.parse(token)[0].normal_form])
                    singleFileList = singleFileList + token + '\n'
        if singleFileList != '':
            with open('out_verbs_imp/' + file + '.txt', 'w', encoding='utf8') as wordList:
                wordList.write(singleFileList)
    except Exception:
        logging.exception(file)
        print('Error processing the ' + file + '.')
        continue

with open('verbs_imp.csv', 'w', encoding='utf8', newline='') as outFile:
    writer = csv.writer(outFile, delimiter=';')
    writer.writerows(table)
print('Done!')