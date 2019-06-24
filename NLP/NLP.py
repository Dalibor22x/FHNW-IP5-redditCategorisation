import nltk
import random

import CSVHandler

documents = CSVHandler.getDocument()

random.shuffle(documents)  # Random shuffle in order to not always test with the last subreddit

all_words = []
for w in CSVHandler.getAllWords(documents):
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]

learn_test_threshold = 550
training_set = featuresets[:learn_test_threshold]  # set that we'll train our classifier with
testing_set = featuresets[learn_test_threshold:]  # set that we'll test against.

# TODO Try Bag of words and TFID
classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)

classifier.show_most_informative_features(15)