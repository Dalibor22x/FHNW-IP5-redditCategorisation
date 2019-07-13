from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier


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
        return RandomForestClassifier(n_estimators=1000, random_state=0)

    @staticmethod
    def k_neighbors():
        return KNeighborsClassifier(n_neighbors=5)
