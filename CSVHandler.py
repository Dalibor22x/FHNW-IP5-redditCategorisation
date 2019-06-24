import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


ps = PorterStemmer() # for stemming the words
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def getDocument():
    document = []
    with open('categorized/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        next(reader) # Skip the first row (header)

        for row in reader:
            if row[0] != '':
                # TODO:
                # Try with title only first
                # document.append(((getCleanTokens(row[2])), row[0]))

                # Try with text only next
                # document.append(((getCleanTokens(row[3])), row[0]))

                # Try with text and title
                document.append(((getCleanTokens(row[2]) + getCleanTokens(row[3])), row[0]))

        return document

def getAllWords(document):
    allWords = []
    for row in document:
        for tokens in row[0]:
            allWords.append(tokens)
    return allWords


def getCleanTokens(words):
    word_tokens = word_tokenize(words)

    # TODO: Remove links

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w.lower()))

    return filtered_sentence
