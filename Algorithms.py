from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np


class Algorithms:

    @staticmethod
    def gaussian_naive_bayes():
        return GaussianNB()

    @staticmethod
    def complement_naive_bayes():
        return ComplementNB()

    @staticmethod
    def multinomial_naive_bayes():
        return MultinomialNB()

    @staticmethod
    def random_forest():
        return RandomForestClassifier()

    @staticmethod
    def k_neighbors():
        return KNeighborsClassifier()

    @staticmethod
    def hyperparameter_tuning__multinomial_naive_bayes(documents, text_model):
        param_grid = {
            'alpha': np.linspace(0.5, 1.5, 6),
            'fit_prior': [True, False]
        }

        model = MultinomialNB()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, text_model)

    @staticmethod
    def hyperparameter_tuning__k_neighbors(documents, text_model):
        param_grid = {
            'n_neighbors': range(1, 31)
        }

        model = KNeighborsClassifier()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, text_model)

    @staticmethod
    def hyperparameter_tuning__random_forest(documents, text_model):
        param_grid = {
            'bootstrap': [True],
            'max_depth': [80, 90, 100, 110],
            'max_features': [2, 3],
            'min_samples_leaf': [3, 4, 5],
            'min_samples_split': [8, 10, 12],
            'n_estimators': [100, 200, 300, 1000]
        }

        model = RandomForestClassifier()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, text_model)

    @staticmethod
    def hyperparameter_tuning(model, param_grid, documents, text_model):
        grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, verbose=2)

        docs = list(map(lambda x: ' '.join(x[0]), documents))
        y = list(map(lambda x: x[1], documents))

        if text_model == "Bag of Words":
            vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
            X = vectorizer.fit_transform(docs)
            X = X.toarray()
        else:
            tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
            X = tfidfconverter.fit_transform(docs).toarray()

        grid.fit(X, y)

        print(grid.best_score_)
        print(grid.best_params_)
