from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


class Algorithms:

    @staticmethod
    def gaussian_naive_bayes():
        algorithm = {
            "algorithm": GaussianNB(),
            "tfidf_max_features": 700,
            "tfidf_min_df": 6,
            "tfidf_max_df": 0.5,
            "bow_max_features": 1500,
            "bow_min_df": 5,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def complement_naive_bayes():
        algorithm = {
            "algorithm": ComplementNB(),
            "tfidf_max_features": 2000,
            "tfidf_min_df": 2,
            "tfidf_max_df": 0.5,
            "bow_max_features": 700,
            "bow_min_df": 5,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def multinomial_naive_bayes():
        algorithm = {
            "algorithm": MultinomialNB(alpha=6, fit_prior=False),
            "tfidf_max_features": 1000,
            "tfidf_min_df": 6,
            "tfidf_max_df": 0.5,
            "bow_max_features": 2000,
            "bow_min_df": 2,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def random_forest():
        algorithm = {
            "algorithm": RandomForestClassifier(bootstrap=False, max_depth=120, max_features="sqrt", min_samples_leaf=2, min_samples_split=2, n_estimators=800),
            "tfidf_max_features": 2000,
            "tfidf_min_df": 2,
            "tfidf_max_df": 0.8,
            "bow_max_features": 2000,
            "bow_min_df": 6,
            "bow_max_df": 0.6
        }
        return algorithm

    @staticmethod
    def k_neighbors():
        algorithm = {
            "algorithm": KNeighborsClassifier(),
            "tfidf_max_features": 1500,
            "tfidf_min_df": 2,
            "tfidf_max_df": 0.5,
            "bow_max_features": 700,
            "bow_min_df": 9,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def svc():
        algorithm = {
            "algorithm": SVC(gamma=0.08838834764831845, C=7),
            "tfidf_max_features": 1000,
            "tfidf_min_df": 6,
            "tfidf_max_df": 0.5,
            "bow_max_features": 700,
            "bow_min_df": 2,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def ada_boost():
        algorithm = {
            "algorithm": AdaBoostClassifier(),
            "tfidf_max_features": 700,
            "tfidf_min_df": 9,
            "tfidf_max_df": 0.5,
            "bow_max_features": 1500,
            "bow_min_df": 2,
            "bow_max_df": 0.5
        }
        return algorithm

    @staticmethod
    def hyperparameter_tuning__multinomial_naive_bayes(documents, feature_model):
        param_grid = {
            'alpha': [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 1.1, 1.2, 1.3, 1.7, 2, 6, 3],
            'fit_prior': [True, False]
        }

        model = MultinomialNB()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, feature_model)

    @staticmethod
    def hyperparameter_tuning__svc(documents, feature_model):
        param_grid = {
            'gamma': [pow(2, -3), pow(2, -3.25), pow(2, -3.5), pow(2, -3.75), pow(2, -4), pow(2, -2.75), pow(2, -2.5), pow(2, -2.25), pow(2, -2), pow(2, -1.75)],
            'C': range(1, 15)
        }

        model = SVC()
        Algorithms.random_hyperparameter_tuning(model, param_grid, documents, feature_model)

    @staticmethod
    def hyperparameter_tuning__k_neighbors(documents, feature_model):
        param_grid = {
            'n_neighbors': range(1, 31)
        }

        model = KNeighborsClassifier()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, feature_model)

    @staticmethod
    def hyperparameter_tuning__random_forest(documents, feature_model):
        param_grid = {
            'bootstrap': [False],
            'max_depth': [80, 90, 100, 110, 120],
            'max_features': ['sqrt'],
            'min_samples_leaf': [1, 2, 4],
            'min_samples_split': [2, 5, 10],
            'n_estimators': [600, 800, 1000, 1200, 1400]
        }

        model = RandomForestClassifier()
        Algorithms.hyperparameter_tuning(model, param_grid, documents, feature_model)

    @staticmethod
    def hyperparameter_tuning(model, param_grid, documents, feature_model):
        grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, verbose=2)

        docs = list(map(lambda x: ' '.join(x[0]), documents))
        y = list(map(lambda x: x[1], documents))

        if feature_model == "Bag of Words":
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
    def random_hyperparameter_tuning(model, param_grid, documents, feature_model):
        grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, cv=10, n_jobs=-1, verbose=2)

        docs = list(map(lambda x: ' '.join(x[0]), documents))
        y = list(map(lambda x: x[1], documents))

        if feature_model == "Bag of Words":
            vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
            X = vectorizer.fit_transform(docs)
            X = X.toarray()
        else:
            tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
            X = tfidfconverter.fit_transform(docs).toarray()

        grid.fit(X, y)

        print(grid.best_score_)
        print(grid.best_params_)
