import csv
import nltk
import os
import re
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


def get_document(text_mode, n, reduced_categories, categorized=True):
    print("Running in mode: " + text_mode)

    if reduced_categories:
        excluded_categories = [
                                "Advertisement",
                                "Feature information",
                                # "Feature request",
                                "Feature shortcoming",
                                "Feature strength",
                                "General complaint",
                                "General praise",
                                "How to",
                                "Social interaction",
                                "Software Constraint",
                                "Software extension",
                                "Content related",
                                # "Unclear / Unrelated"
                                ]
    else:
        excluded_categories = []

    documents = []
    with open('data/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        next(reader)  # Skip the first row (header)

        for row in reader:
            # if row[0] in excluded_categories:
            #     row[0] = "Other"
            if categorized:
                if row[0] != '' and row[0] not in excluded_categories:
                    if text_mode == "title_only":
                        documents.append(((get_clean_tokens(row[2], n)), row[0]))
                    elif text_mode == "text_only":
                        documents.append(((get_clean_tokens(row[3], n)), row[0]))
                    else:
                        documents.append(((get_clean_tokens(row[2] + " " + row[3], n)), row[0]))
            elif not categorized:
                if text_mode == "title_only":
                    documents.append((get_clean_tokens(row[2], n)))
                elif text_mode == "text_only":
                    documents.append((get_clean_tokens(row[3], n)))
                else:
                    documents.append((get_clean_tokens(row[2] + " " + row[3], n)))


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


def get_clean_tokens(words, n):
    words = re.sub(r"http\S+", "", words)  # Remove links

    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(words)
    lemmatizer = WordNetLemmatizer()

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            w = ps.stem(w.lower())
            w = lemmatizer.lemmatize(w, pos='v')
            filtered_sentence.append(w)

    ngrams = zip(*[filtered_sentence[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]
