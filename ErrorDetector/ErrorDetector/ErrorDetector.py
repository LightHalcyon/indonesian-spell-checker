from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


lib = []
with open("kebi.txt") as f:
    for line in f:
        lib.append(line.replace('\n',''))

data = []

with open("sentence.txt",encoding='utf-8') as g:
    for line in g:
        data.append(line)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

typo = []
for lineNum, line in enumerate(data,1):
    currLine = []
    currLine = line.replace('.','').replace(',','').replace('\n','').lower().split()
    for wordNum, word in enumerate(currLine,1):
        if word not in lib:
            if stemmer.stem(word) not in lib:
                typo.append((lineNum,wordNum))

print(typo)