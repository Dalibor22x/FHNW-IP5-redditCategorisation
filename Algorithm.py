from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import csv
import CSVHandler


def run(documents, model, feature_model, identifier_addition, write_output, predict_uncategorized, tfidf_max_features, tfidf_min_df, tfidf_max_df, bow_max_features, bow_min_df, bow_max_df):
    """
    Run training and 10-fold cross validation on the given model as well as out-of-sample predictions and print the
    results. Depending on parametrization also writes the prediction to a CSV file named after the identifier.

    :param documents: A list of preprocessed documents used for training and testing the model.

    :param model: The sklearn model to be trained and tested (e.g. RandomForestClassifier)

    :param feature_model: A String being either 'Bag of Words' or 'TF IDF' used for vectorizing the document.

    :param identifier_addition: A String of additional information to add to the identifier in order to make it
                                distinguishable and used for file name.

    :param write_output: A boolean value whether or not to write the predictions into a CSV file. If predict_uncategorized
                         is set to True, the data used for prediction is the remaining data entries which are not categorized.
                         If it is set to False, it will use out-of-sample data (which is categorized) for the prediction.

    :param predict_uncategorized: A boolean value used in combination with write_output whether or not to predict
                                  on uncategorized data. Is only showing results when write_output is true.

    :param tfidf_max_features: An Integer value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param tfidf_min_df: A Float value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param tfidf_max_df: A Float value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param bow_max_features: An Integer value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :param bow_min_df: A Float value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :param bow_max_df: A Float value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :return: A tuple consisting of the identifier and the mean score of the 10-fold cross validation.
    """

    identifier = "Algorithm: '{}', feature-model: '{}', {}".format(model.__class__.__name__, feature_model, identifier_addition)
    print("\n\nRunning: '{}'".format(identifier))

    X, y, docs = get_X_and_y(documents, feature_model, True, tfidf_max_features, tfidf_min_df, tfidf_max_df, bow_max_features, bow_min_df, bow_max_df)
    out_of_sample_threshold = len(X) - 200

    out_of_sample_X = X[out_of_sample_threshold:]
    X = X[:out_of_sample_threshold]

    out_of_sample_y = y[out_of_sample_threshold:]
    y = y[:out_of_sample_threshold]

    k_folds = 10
    X_folds = np.array_split(X, k_folds)
    y_folds = np.array_split(y, k_folds)
    scores = []

    # Perform 10-fold cross validation
    for k in range(k_folds):
        X_pred = list(X_folds)
        X_test = X_pred.pop(k)
        X_pred = np.concatenate(X_pred)

        y_train = list(y_folds)
        y_test = y_train.pop(k)
        y_train = np.concatenate(y_train)

        scores.append(model.fit(X_pred, y_train).score(X_test, y_test))

    print("Average score after {} fold crossvalidation: {}".format(k_folds, np.mean(scores)))

    # Perform predictions on out-of-sample data
    print("\nOut of sample:")

    # Model must be fitted again with the whole dataset (without out-of-sample data), because 10-fold cross validation
    # overwrites the model on each iteration and 1 fold is always used for training and thus the model is missing
    # potentially important data for the fitting process
    model.fit(X, y)

    X_pred = out_of_sample_X
    y_test = out_of_sample_y

    y_pred = model.predict(X_pred)

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\n\nClassification report:")
    print(classification_report(y_test, y_pred))

    print("\n\nAccuracy score:")
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)

    # Write out-of-sample predictions to CSV file
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

    # Write new data predictions to CSV file
    elif write_output and predict_uncategorized:
        uncategorized_documents = CSVHandler.get_document(text_mode="normal", n=3, reduced_categories=True, categorized=False)

        X_pred, _, u_docs = get_X_and_y(uncategorized_documents, feature_model, False, tfidf_max_features, tfidf_min_df, tfidf_max_df, bow_max_features, bow_min_df, bow_max_df)
        y_pred = model.predict(X_pred)
        uncategorized_identifier = "uncategorized_" + identifier
        prediction = list(zip(u_docs, y_pred))

        # Write to CSV
        file_name = uncategorized_identifier.replace(" ", "_").replace("'", "").replace(":", "").replace(",", "_")
        with open("data/output/uncategorized/" + file_name + ".csv", 'w') as out:
            csv_out = csv.writer(out, delimiter="|")
            csv_out.writerow(['test_set', 'prediction'])
            for row in prediction:
                csv_out.writerow(row)

    return (identifier, np.mean(scores))  # Return tuple


def get_X_and_y(documents, feature_model, categorized, tfidf_max_features, tfidf_min_df, tfidf_max_df, bow_max_features, bow_min_df, bow_max_df):
    """
    Get the vectorized X and y value for training and testing.

    :param documents: A list of preprocessed documents used for training and testing the model.

    :param feature_model: A String being either 'Bag of Words' or 'TF IDF' used for vectorizing the document.

    :param categorized: A Boolean value whether the given documents is a list of categorized submissions or a list of
                        uncategorized submissions.

    :param tfidf_max_features: An Integer value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param tfidf_min_df: A Float value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param tfidf_max_df: A Float value passed to TfidfVectorizer. See TfidfVectorizer documentation for more information.

    :param bow_max_features: An Integer value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :param bow_min_df: A Float value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :param bow_max_df: A Float value passed to CountVectorizer. See CountVectorizer documentation for more information.

    :return: X, y and the document without the categories.
    """

    if categorized:
        docs = list(map(lambda x: ' '.join(x[0]), documents))
        y = list(map(lambda x: x[1], documents))
    else:
        docs = list(map(lambda x: ' '.join(x), documents))
        y = []

    if feature_model == "Bag of Words":
        vectorizer = CountVectorizer(max_features=bow_max_features, min_df=bow_min_df, max_df=bow_max_df, stop_words=stopwords.words('english'))
        X = vectorizer.fit_transform(docs).toarray()

    elif feature_model == "TF IDF":
        tfidfconverter = TfidfVectorizer(max_features=tfidf_max_features, min_df=tfidf_min_df, max_df=tfidf_max_df, stop_words=stopwords.words('english'))
        X = tfidfconverter.fit_transform(docs).toarray()

    return X, y, docs
