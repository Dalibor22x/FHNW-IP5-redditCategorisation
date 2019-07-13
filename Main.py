import CSVHandler
import os
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
# multinomial_naive_bayes.run(documents)

algorithms = Algorithms.Algorithms

for model in models:
    Algorithm.run(documents, algorithms.multinomial_naive_bayes(), model)
    Algorithm.run(documents, algorithms.complement_naive_bayes(), model)
    Algorithm.run(documents, algorithms.gaussian_naive_bayes(), model)
    Algorithm.run(documents, algorithms.random_forest(), model)
    Algorithm.run(documents, algorithms.k_neighbors(), model)
