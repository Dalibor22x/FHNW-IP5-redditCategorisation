from enum import Enum
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB


class Algorithms(Enum):
    GaussianNaiveBayes = GaussianNB()
    ComplementNaiveBayes = ComplementNB()
    MultinomialNaiveBayes = MultinomialNB()
    RandomForest = RandomForestClassifier(n_estimators=1000, random_state=0)