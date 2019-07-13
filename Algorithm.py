from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas
import csv
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np


def run(documents, classifier, model):
    print("\n\nRunning Algorithm: '{}' with model: '{}'".format(classifier.__class__.__name__, model))

    docs = list(map(lambda x: ' '.join(x[0]), documents))
    y = list(map(lambda x: x[1], documents))

    if model == "Bag of Words":
        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(docs)
        X = X.toarray()
    else:
        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(docs).toarray()

    out_of_sample_threshold = len(X) - 200

    out_of_sample_X = X[out_of_sample_threshold:]
    X = X[:out_of_sample_threshold]

    out_of_sample_y = y[out_of_sample_threshold:]
    y = y[:out_of_sample_threshold]

    k_folds = 10
    X_folds = np.array_split(X, k_folds)
    y_folds = np.array_split(y, k_folds)
    scores = []

    for k in range(k_folds):
        X_train = list(X_folds)
        X_test = X_train.pop(k)
        X_train = np.concatenate(X_train)

        y_train = list(y_folds)
        y_test = y_train.pop(k)
        y_train = np.concatenate(y_train)

        scores.append(classifier.fit(X_train, y_train).score(X_test, y_test))

    print("Average score after {} fold crossvalidation: {}".format(k_folds, np.mean(scores)))

    classifier.fit(X, y)

    X_train = out_of_sample_X
    y_test = out_of_sample_y

    y_pred = classifier.predict(X_train)

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\n\nClassification report:")
    print(classification_report(y_test, y_pred))

    print("\n\nAccuracy score:")
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    # learn_test_threshold = int(round(len(documents) * learn_test_threshold_percentage))
    # testing_set = documents[learn_test_threshold:]  # set that we'll test against.

    # prediction = list(zip(testing_set, y_pred))

    # Write to CSV
    # with open("data/output" + classifier.__class__.__name__ + ".csv", 'w') as out:
    #     csv_out = csv.writer(out, delimiter="|")
    #     csv_out.writerow(['test_set', 'prediction'])
    #     for row in prediction:
    #         csv_out.writerow(row)

    return documents
