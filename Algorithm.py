from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import csv
import CSVHandler


def run(documents, model, feature_model, identifier_addition, write_output, predict_uncategorized, tfidf_max_features, tfidf_min_df, tfidf_max_df):
    """

    TODO: Describe types etc.
    :param documents: The preprocessed documents to train and test on
    :param model: The sklearn model to be trained and tested (e.g. RandomForestClassifier)
    :param feature_model: TODO: The model for transforming the features (e.g. Bag of Words or TF IDF)
    :param identifier_addition: Additional information to add to the identifier in order to make it better distinguishable
                                … used for file name and evaluation …
    :param write_output: A boolean value whether or not to write the predictions into a CSV file. If predict_uncategorized
                         is set to True, the data used for prediction is the remaining data entries which are not categorized.
                         If it is set to False, it will use out-of-sample data (which is categorized) for the prediction.
    :param predict_uncategorized: A boolean value used in combination with write_output whether or not to predict
                                  on uncategorized data. Is only showing results when write_output is true.
    :param tfidf_max_features:
    :param tfidf_min_df:
    :param tfidf_max_df:
    :return:
    """
    identifier = "Algorithm: '{}', feature-model: '{}', {}".format(model.__class__.__name__, feature_model, identifier_addition)
    print("\n\nRunning: '{}'".format(identifier))

    X, y, docs = get_X_and_y(documents, feature_model, True, tfidf_max_features, tfidf_min_df, tfidf_max_df)
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

        scores.append(model.fit(X_train, y_train).score(X_test, y_test))

    print("Average score after {} fold crossvalidation: {}".format(k_folds, np.mean(scores)))

    print("\nOut of sample:")

    model.fit(X, y)

    X_train = out_of_sample_X
    y_test = out_of_sample_y

    y_pred = model.predict(X_train)

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\n\nClassification report:")
    print(classification_report(y_test, y_pred))

    print("\n\nAccuracy score:")
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    if write_output and not predict_uncategorized:
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
                
    elif write_output and predict_uncategorized:
        uncategorized_documents = CSVHandler.get_document(text_mode="normal", n=2, reduced_categories=True, categorized=False)

        X_train, _, u_docs = get_X_and_y(uncategorized_documents, feature_model, False, tfidf_max_features, tfidf_min_df, tfidf_max_df)
        y_pred = model.predict(X_train)
        uncategorized_identifier = "uncategorized_" + identifier
        prediction = list(zip(docs, y_pred))

        # Write to CSV
        file_name = uncategorized_identifier.replace(" ", "_").replace("'", "").replace(":", "").replace(",", "_")
        with open("data/output/uncategorized/" + file_name + ".csv", 'w') as out:
            csv_out = csv.writer(out, delimiter="|")
            csv_out.writerow(['test_set', 'prediction'])
            for row in prediction:
                csv_out.writerow(row)

    return (identifier, np.mean(scores))


def get_X_and_y(documents, feature_model, categorized, tfidf_max_features, tfidf_min_df, tfidf_max_df):
    """

    :param documents:
    :param feature_model:
    :param categorized:
    :param tfidf_max_features:
    :param tfidf_min_df:
    :param tfidf_max_df:
    :return:
    """
    if categorized:
        docs = list(map(lambda x: ' '.join(x[0]), documents))
        y = list(map(lambda x: x[1], documents))
    else:
        docs = list(map(lambda x: ' '.join(x), documents))
        y = []

    if feature_model == "Bag of Words":
        vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(docs)
        X = X.toarray()
    elif feature_model == "TF IDF":
        tfidfconverter = TfidfVectorizer(max_features=tfidf_max_features, min_df=tfidf_min_df, max_df=tfidf_max_df, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(docs).toarray()

    return X, y, docs