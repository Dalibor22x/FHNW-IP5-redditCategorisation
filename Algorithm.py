from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas
import csv


def run(documents, classifier, model):
    print("\n\nRunning Algorithm: '{}'".format(classifier))

    learn_test_threshold_percentage = 0.8

    docs = list(map(lambda x: ' '.join(x[0]), documents))
    y = list(map(lambda x: x[1], documents))

    if model == "Bag of Words":
        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(docs)
        X = X.toarray()
    else:
        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(docs).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1 - learn_test_threshold_percentage), random_state=0)

    classifier = classifier()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\n\nClassification report:")
    print(classification_report(y_test, y_pred))

    print("\n\nAccuracy score:")
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(accuracy)

    learn_test_threshold = int(round(len(documents) * learn_test_threshold_percentage))
    testing_set = documents[learn_test_threshold:]  # set that we'll test against.

    prediction = list(zip(testing_set, y_pred))

    # Write to CSV
    with open("data/output" + classifier.__class__.__name__ + ".csv", 'w') as out:
        csv_out = csv.writer(out, delimiter="|")
        csv_out.writerow(['test_set', 'prediction'])
        for row in prediction:
            csv_out.writerow(row)

    return documents