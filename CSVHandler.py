import csv

def getDocument():
    documents = []
    with open('categorized/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            documents.append((cleanString(row[2])+' '+cleanString(row[3]),row[0]))
        return documents

def getAllWords(document):
    allWords = []
    for row in document:
        for word in row[0].split(' '):
            allWords.append(word)
    return allWords

def cleanString(words):
    excluded = [',', '[', ']', '(', ')', '-', ';', '"', '\'', ':', '.']
    for e in excluded:
        words = words.replace(e, '')
    return words.lower()
