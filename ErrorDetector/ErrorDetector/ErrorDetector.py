from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
#import enchant
import nltk
import re
from builtins import any as b_any

class Typo(object):
    lineNum = 0
    wordNum = 0
    errorIndexFront = 0
    errorIndexRear = 0
    suggestion = {}
    unstemmed = ""

    def __init__(self, lineNum, wordNum, unstemmed):
        self.lineNum = lineNum
        self.wordNum = wordNum
        self.errorIndexFront = 0
        self.errorIndexRear = 0
        self.suggestion = {}
        self.unstemmed = unstemmed

    def setErrorIndexFront(self, errorIndexFront):
        self.errorIndexFront = errorIndexFront

    def setErrorIndexRear(self, errorIndexRear):
        self.errorIndexRear = errorIndexRear

    def addSuggestion(self, word):
        self.suggestion[word] = len(self.suggestion)

    def getErrorIndexFront(self):
        return self.errorIndexFront

    def getErrorIndexRear(self):
        return self.errorIndexRear

    def getSuggestion(self):
        return self.suggestion

lib = {}
with open("kebi.txt") as f:
    i = 0
    for line in f:
        lib[line.replace('\n','').lower()] = i
        i+=1
        
data = []
with open("sentence3.txt",encoding='ansi') as g:
    for line in g:
        data.append(re.sub(r"[^A-Za-z0-9 ]","",re.sub(r"[^A-Za-z0-9\.\,\n ]"," ",line)).lower())

factory = StemmerFactory()
stemmer = factory.create_stemmer()
#d = enchant.Dict("en_US")
en = set(w.lower() for w in nltk.corpus.words.words())

typo = {}
for lineNum, line in enumerate(data,1):
    currLine = []
    currLine = line.split()
    for wordNum, word in enumerate(currLine,1):
        if not word.isdigit():
            if word not in en:
                if word not in lib.keys():    
                    stemmed = stemmer.stem(word)
                    if stemmed not in lib.keys():
                        #print(stemmed)
                        typo[stemmed] = Typo(lineNum,wordNum,word)

for word in typo.keys():
    print(word)
    for x in range(0, len(word)):
        if not b_any(i.startswith(word[0:x]) for i in lib.keys()):
            typo[word].setErrorIndexFront(x)
            #print(word[0:x])
            #print(word[0:typo[word].getErrorIndexFront() - 1])
            break

    for x in range(len(word) - 2, 0, -1):
        if not b_any(i.endswith(word[x:len(word)]) for i in lib.keys()):
            typo[word].setErrorIndexRear(x)
            print(word[x:len(word)])
            #print(word[typo[word].getErrorIndexRear()+1:len(word)])
            break

    for sug in lib.keys():
        if abs(len(sug) - len(word))<2:
            if sug.startswith(word[0:typo[word].getErrorIndexFront() - 2]):
                if sug.endswith(word[typo[word].getErrorIndexRear() + 2:len(word)]):
                    typo[word].addSuggestion(sug)
                    #print(sug)
                elif sug.endswith(word[typo[word].getErrorIndexRear() + 1:len(word)]):
                    typo[word].addSuggestion(sug)
            elif sug.startswith(word[0:typo[word].getErrorIndexFront() - 1]):
                if sug.endswith(word[typo[word].getErrorIndexRear() + 1:len(word)]):
                    typo[word].addSuggestion(sug)
                elif sug.endswith(word[typo[word].getErrorIndexRear() + 2:len(word)]):
                    typo[word].addSuggestion(sug)

    

for word in typo.keys():
    for sug in typo[word].getSuggestion().keys():
        #todo
        s = (typo[word].getErrorIndexFront() - 1) + (len(word) - typo[word].getErrorIndexRear() + 1)
        n1 = len(word)
        n2 = len(sug)
        u1 = 0
        u2 = 0
        if n1 == n2:
            u1 = len(word[(typo[word].getErrorIndexFront() - 1):(len(word) - typo[word].getErrorIndexRear() + 1)])
            u2 = u1
        else:
            u2 = abs(n2 - n1)
        typo[word].getSuggestion()[sug] = ((s ^ 2) - ((n2 - n1) ^ 2) - ((u1 + u2) ^ 2)) / (s ^ 2)

    for k,v in list(typo[word].getSuggestion().items()):
        if v <= 0:
            del typo[word].getSuggestion()[k]
    
    print(typo[word].getSuggestion())