from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import ElasticNet

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
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
        return MultinomialNB(alpha=6, fit_prior=False)

    @staticmethod
    def random_forest():
        return RandomForestClassifier(n_estimators=100)

    @staticmethod
    def k_neighbors():
        return KNeighborsClassifier()

    @staticmethod
    def svc():
        return SVC(gamma=0.08838834764831845, C=7)

    @staticmethod
    def elastic_net():
        return ElasticNet()

    @staticmethod
    def hyperparameter_tuning__multinomial_naive_bayes(documents, text_model):
        param_grid = {
            'alpha': [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 1.1, 1.2, 1.3, 1.7, 2, 6, 3],
            'fit_prior': [True, False]
        }

        model = MultinomialNB()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, text_model)

    @staticmethod
    def hyperparameter_tuning__svc(documents, text_model):
        param_grid = {
            'gamma': [pow(2, -3), pow(2, -3.25), pow(2, -3.5), pow(2, -3.75), pow(2, -4), pow(2, -2.75), pow(2, -2.5), pow(2, -2.25), pow(2, -2), pow(2, -1.75)],
            'C': range(1, 15)
        }

        model = SVC()
        Algorithms.random_hyperparameter_tuning(model, param_grid, documents, text_model)

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

    @staticmethod
    def random_hyperparameter_tuning(model, param_grid, documents, text_model):
        grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, cv=10, n_jobs=-1, verbose=2)

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
