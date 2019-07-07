import csv
import nltk
import os
import random
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


ps = PorterStemmer()  # for stemming the words
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


def prepare_subreddits():
    with open('categorized/all_subreddits.tsv', 'U') as f:

        new_text = f.read()

        while '|' in new_text:
            new_text = new_text.replace('|', '~~')

        while '	' in new_text:
            new_text = new_text.replace('	', '|')

    with open('categorized/all_subreddits.csv', "w") as f:
        f.write(new_text)

    if os.path.exists("categorized/all_subreddits.tsv"):
        os.remove("categorized/all_subreddits.tsv")


def get_document(mode):
    print("Running in mode: " + mode)

    documents = []
    with open('categorized/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        next(reader)  # Skip the first row (header)

        for row in reader:
            if row[0] != '':
                if mode == "title_only":
                    documents.append(((get_clean_tokens(row[2])), row[0]))
                elif mode == "text_only":
                    documents.append(((get_clean_tokens(row[3])), row[0]))
                else:
                    documents.append(((get_clean_tokens(row[2]) + get_clean_tokens(row[3])), row[0]))

        random.shuffle(documents)

        return documents  # Random shuffle in order to not always test with the last subreddit


def get_all_words(document):
    allWords = []
    for row in document:
        for tokens in row[0]:
            allWords.append(tokens)
    return allWords


def get_clean_tokens(words):
    word_tokens = word_tokenize(words)

    # TODO: Remove links

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w.lower()))

    return filtered_sentence
