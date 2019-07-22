from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import csv


def run(documents, classifier, feature_model, identifier_addition, write_output, tfidf_max_features, tfidf_min_df, tfidf_max_df):
    identifier = "Algorithm: '{}', feature-model: '{}', {}".format(classifier.__class__.__name__, feature_model, identifier_addition)
    print("\n\nRunning: '{}'".format(identifier))

    docs = list(map(lambda x: ' '.join(x[0]), documents))
    y = list(map(lambda x: x[1], documents))

    if feature_model == "Bag of Words":
        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(docs)
        X = X.toarray()
    else:
        tfidfconverter = TfidfVectorizer(max_features=tfidf_max_features, min_df=tfidf_min_df, max_df=tfidf_max_df, stop_words=stopwords.words('english'))
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

    print("\nOut of sample:")

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

    if write_output:
        out_of_sample_x_data = docs[:out_of_sample_threshold]
        out_of_sample_y_data = y[:out_of_sample_threshold]
        prediction = list(zip(zip(out_of_sample_x_data, out_of_sample_y_data), y_pred))

        # Write to CSV
        file_name = identifier.replace(" ", "_").replace("'", "").replace(":", "").replace(",", "_")
        with open("data/output/" + file_name + ".csv", 'w') as out:
            csv_out = csv.writer(out, delimiter="|")
            csv_out.writerow(['test_set', 'prediction'])
            for row in prediction:
                csv_out.writerow(row)

    return (identifier, np.mean(scores))
