import nltk
import CSVHandler


def run(documents):
    print("\n\nRunning Algorithm: 'Naive Bayes'")

    all_words = []
    for w in CSVHandler.get_all_words(documents):
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:3000]
    featuresets = [(find_features(rev, word_features), category) for (rev, category) in documents]

    learn_test_threshold = int(round(len(documents) * 0.8))
    training_set = featuresets[:learn_test_threshold]  # set that we'll train our classifier with
    testing_set = featuresets[learn_test_threshold:]  # set that we'll test against.

    classifier = nltk.NaiveBayesClassifier.train(training_set)

    print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    classifier.show_most_informative_features(15)


def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features