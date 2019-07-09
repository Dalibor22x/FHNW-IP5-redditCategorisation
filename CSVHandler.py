import csv
import nltk
import os
import re
import random
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


ps = PorterStemmer()  # for stemming the words
# TODO: Download only if necessary
# nltk.download('stopwords')
# nltk.download('punkt')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))



def prepare_subreddits():
    with open('data/import_me.tsv', 'U') as f:

        new_text = f.read()

        while '|' in new_text:
            new_text = new_text.replace('|', '~~')

        while '	' in new_text:
            new_text = new_text.replace('	', '|')

    with open('data/all_subreddits.csv', "w") as f:
        f.write(new_text)

    if os.path.exists("data/import_me.tsv"):
        os.remove("data/import_me.tsv")


def get_document(mode):
    print("Running in mode: " + mode)

    # excluded_categories = ["Feature information", "Feature strength", "General praise", "Social interaction", "Software constraint", "Software extension"]
    excluded_categories = ["Bug report", "Content related", "Question", "Unclear / Unrelated"]

    documents = []
    with open('data/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        next(reader)  # Skip the first row (header)

        for row in reader:
            if row[0] != '' and row[0] in excluded_categories:
                if mode == "title_only":
                    documents.append(((get_clean_tokens(row[2])), row[0]))
                elif mode == "text_only":
                    documents.append(((get_clean_tokens(row[3])), row[0]))
                else:
                    documents.append(((get_clean_tokens(row[2]) + get_clean_tokens(row[3])), row[0]))

        # random.shuffle(documents)  # Random shuffle in order to not always test with the last subreddit

        # Write to CSV
        with open('data/preprocessed.csv', 'w') as out:
            csv_out = csv.writer(out, delimiter="|")
            csv_out.writerow(['tokens', 'classification'])
            for row in documents:
                csv_out.writerow(row)

        return documents


def get_all_words(document):
    allWords = []
    for row in document:
        for tokens in row[0]:
            allWords.append(tokens)
    return allWords


def get_clean_tokens(words):
    words = re.sub(r"http\S+", "", words)  # Remove links

    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(words)
    lemmatizer = WordNetLemmatizer()

    filtered_sentence = []

    # TODO: Add lemmatization

    for w in word_tokens:
        if w not in stop_words:
            w = ps.stem(w.lower())
            w = lemmatizer.lemmatize(w, pos='v')
            filtered_sentence.append(w)

    n = 2
    ngrams = zip(*[filtered_sentence[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]
