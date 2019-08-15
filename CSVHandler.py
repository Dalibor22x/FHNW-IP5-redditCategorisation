import csv
import nltk
import os
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('stopwords')  # Used for removing stopwords
nltk.download('punkt')  # Used for removing punctuation
nltk.download('wordnet')  # Used for lemmatization
stop_words = set(stopwords.words('english'))


def import_new_dataset():
    """
    Import new dataset with named 'data/import_me.tsv' and transform into file 'data/all_subreddits.csv'.
    File 'data/import_me.tsv' is deleted after import.
    """
    with open('data/import_me.tsv', 'U') as f:
        separator = "|"
        new_text = f.read()

        # Replace separator character with different character
        while separator in new_text:
            new_text = new_text.replace(separator, '~~')

        # Replace TSV separator (tab) with separator
        while '	' in new_text:
            new_text = new_text.replace('	', separator)

    with open('data/all_subreddits.csv', "w") as f:
        f.write(new_text)

    if os.path.exists("data/import_me.tsv"):
        os.remove("data/import_me.tsv")


def get_document(text_mode, n, reduced_categories, categorized=True):
    """
    Get list of documents ready for model training, testing and predictions.

    :param text_mode: A String being either 'normal', 'title_only' or 'text_only' where 'title_only means to only use
                      the title from the Reddit submission, 'text_only' means to only use the selftext from the submission
                      and 'normal' means to use both in combination with each other.

    :param n: An integer value used to generate n-grams where n is the amount of grams to be created.

    :param reduced_categories: A boolean value used for excluding certain submissions with a specific category
                               if set to True. Otherwise, no submissions are excluded. Has no effect if the parameter
                               'categorzied' is set to False.

    :param categorized: A boolean value with default value True. It is used for returning only manually categorized
                        submissions if set to True in order to train and test models. If set to False however, this method
                        also returns unclassified submissions in order for models to predict categories.

    :return: A preprocessed list of documents
    """

    print("Running in mode: " + text_mode)

    old_categories = False

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

    # If categorized == True: Array containing tuples of tokenized text and the category --> (tokens, category)
    # If categorized == False: Array containing only the tokenized text --> (tokens)
    documents = []

    with open('data/all_subreddits.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        next(reader)  # Skip the first row (header)

        for row in reader:
            # Group excluded categories into one category 'other'
            # if row[0] in excluded_categories:
            #     row[0] = "Other"
            if categorized:
                # Check whether old 'Question' category should be used or the new split up 'Question' category
                if old_categories:
                    row[0] = row[0].split(';')[0]
                else:
                    if ';' in row[0]:
                        row[0] = row[0].split(';')[1]

                    # Group categories 'Feature request' and 'Usability' together
                    if row[0] == "Feature request" or row[0] == "Usability":
                        row[0] = "Feature request / Usability"

                if row[0] != '' and row[0] not in excluded_categories:
                    if text_mode == "title_only":
                        documents.append(((get_preprocessed_tokens(row[2], n)), row[0]))
                    elif text_mode == "text_only":
                        documents.append(((get_preprocessed_tokens(row[3], n)), row[0]))
                    else:
                        documents.append(((get_preprocessed_tokens(row[2] + " " + row[3], n)), row[0]))

            elif not categorized:
                if text_mode == "title_only":
                    documents.append((get_preprocessed_tokens(row[2], n)))
                elif text_mode == "text_only":
                    documents.append((get_preprocessed_tokens(row[3], n)))
                else:
                    documents.append((get_preprocessed_tokens(row[2] + " " + row[3], n)))

        # Write to CSV
        with open('data/preprocessed.csv', 'w') as out:
            csv_out = csv.writer(out, delimiter="|")
            csv_out.writerow(['tokens', 'classification'])  # Write header
            for row in documents:
                csv_out.writerow(row)

        return documents


def get_preprocessed_tokens(words, n):
    """
    Get a preprocessed array of tokens from the given String. Preprocessing includes transforming the text to lowercase,
    removing punctuation, stopwords and links, performing stemming and lemmatiztion and finally zipping the array to
    create n-grams using the given Integer n.

    :param words: The String to be preprocessed.

    :param n: An integer value used to generate n-grams where n is the amount of grams to be created.

    :return: A preprocessed array of tokens.
    """

    words = re.sub(r"http\S+", "", words)  # Remove links

    tokenizer = RegexpTokenizer(r'\w+')  # This step also removes punctuation
    word_tokens = tokenizer.tokenize(words)  # Create tokens
    ps = PorterStemmer()  # For stemming the tokens
    lemmatizer = WordNetLemmatizer()  # For lemmatizing the tokens

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            w = w.lower()
            w = ps.stem(w)
            w = lemmatizer.lemmatize(w, pos='v')
            filtered_sentence.append(w)

    # Create n-grams
    ngrams = zip(*[filtered_sentence[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]
