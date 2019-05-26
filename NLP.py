import nltk
import random

import CSVHandler

documents = CSVHandler.getDocument()

random.shuffle(documents)

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

# set that we'll train our classifier with
training_set = featuresets[:400]

# set that we'll test against.
testing_set = featuresets[400:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)

classifier.show_most_informative_features(15)