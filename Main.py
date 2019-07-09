import CSVHandler
import os
import NaiveBayes
import TFIDF
import MultinomialNaiveBayes
import Algorithms
import Algorithm

# If import is needed
if os.path.exists("data/import_me.tsv"):
    CSVHandler.prepare_subreddits()

modes = ["normal", "title_only", "text_only"]
models = ["Bag of Words", "TF IDF"]

current_mode = modes[0]

documents = CSVHandler.get_document(current_mode)

print("\n")
# NaiveBayes.run(documents)
# TFIDF.run(documents)
# MultinomialNaiveBayes.run(documents)

print("Model: " + models[0])
Algorithm.run(documents, Algorithms.MultinomialNB, models[0])
Algorithm.run(documents, Algorithms.ComplementNB, models[0])
Algorithm.run(documents, Algorithms.GaussianNB, models[0])
Algorithm.run(documents, Algorithms.RandomForestClassifier, models[0])

print("Model: " + models[1])
Algorithm.run(documents, Algorithms.MultinomialNB, models[1])
Algorithm.run(documents, Algorithms.ComplementNB, models[1])
Algorithm.run(documents, Algorithms.GaussianNB, models[1])
Algorithm.run(documents, Algorithms.RandomForestClassifier, models[1])
