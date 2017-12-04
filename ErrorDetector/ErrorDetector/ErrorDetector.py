from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import enchant
import nltk
import re


lib = []
with open("kebi.txt") as f:
    for line in f:
        lib.append(line.replace('\n','').lower())

data = []
with open("sentence.txt",encoding='utf-8') as g:
    for line in g:
        data.append(line)

factory = StemmerFactory()
stemmer = factory.create_stemmer()
d = enchant.Dict("en_US")
en = set(w.lower() for w in nltk.corpus.words.words())

typo = []
for lineNum, line in enumerate(data,1):
    currLine = []
    currLine = re.sub(r"[^A-Za-z0-9 ]","",re.sub(r"[^A-Za-z0-9\.\,\n ]"," ",line)).lower().split()
    for wordNum, word in enumerate(currLine,1):
        if not word.isdigit():
            if word not in en:
                if word not in lib:    
                    stemmed = stemmer.stem(word)
                    if stemmed not in lib:
                        print(stemmed)
                        typo.append((lineNum,wordNum))

