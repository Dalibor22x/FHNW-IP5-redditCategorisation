import CSVHandler
import os
import Algorithms
import Algorithm
from operator import itemgetter

# text_modes = ["normal", "title_only", "text_only"]
text_modes = ["normal"]
# feature_models = ["Bag of Words", "TF IDF"]
feature_models = ["TF IDF"]
possible_n_grams = [1, 2, 3]
# reduced_categories_possibilities = [True, False]
reduced_categories_possibilities = [True]
algorithms = Algorithms.Algorithms
all_algorithms = [
    algorithms.multinomial_naive_bayes(),
    algorithms.complement_naive_bayes(),
    # algorithms.gaussian_naive_bayes(),
    algorithms.random_forest(),
    algorithms.svc(),
    # algorithms.k_neighbors(),
    # algorithms.ada_boost()
]

def main():
    # If import is needed
    if os.path.exists("data/import_me.tsv"):
        print("Importing new categorised data sets")
        CSVHandler.prepare_subreddits()

    # evaluate_best_parameters()
    evaluate_best_model()
    # evaluate_best_TFIDF_parameters()

def evaluate_best_model():
    scores = []

    for reduced_categories in reduced_categories_possibilities:
        for text_mode in text_modes:
            for n in possible_n_grams:
                documents = CSVHandler.get_document(text_mode, n, reduced_categories)
                identifier_addition = "text-mode: '{}', {}-grams, reduced-categories: {}".format(text_mode, n,
                                                                                                 reduced_categories)

                for model in feature_models:
                    for algorithm in all_algorithms:
                        a = algorithm["algorithm"]
                        tfidf_max_features = algorithm["tfidf_max_features"]
                        tfidf_min_df = algorithm["tfidf_min_df"]
                        tfidf_max_df = algorithm["tfidf_max_df"]
                        scores.append(Algorithm.run(documents, a, model, identifier_addition, True, False, tfidf_max_features, tfidf_min_df, tfidf_max_df))

    print("\n\n\n\nOverview:")
    scores = sorted(scores, key=lambda s: (-s[1], s[0]))
    for s in scores:
        print(s)

    print("\nBest model:")
    print(max(scores, key=itemgetter(1)))


def evaluate_best_parameters():
    documents = CSVHandler.get_document("normal", 2, True)

    algorithms.hyperparameter_tuning__random_forest(documents=documents, text_model="TF IDF")
    # algorithms.hyperparameter_tuning__k_neighbors(documents=documents, text_model="TF IDF")
    # algorithms.hyperparameter_tuning__multinomial_naive_bayes(documents=documents, text_model="TF IDF")
    # algorithms.hyperparameter_tuning__svc(documents=documents, text_model="TF IDF")


def evaluate_best_TFIDF_parameters():
    documents = CSVHandler.get_document("normal", 2, True)
    scores = []
    model = "TF IDF"

    tfidf_max_features = [1500, 1000, 700, 2000]
    tfidf_min_df = [5, 2, 6, 9]
    tfidf_max_df = [0.5, 0.6, 0.7, 0.8, 0.9]

    for mf in tfidf_max_features:
        for min_df in tfidf_min_df:
            for max_df in tfidf_max_df:
                identifier_addition = "text-mode: 'normal', 2-grams, reduced-categories: True, max_features: {}, min_df: {}, max_df: {}".format(mf, min_df, max_df)
                algorithm = algorithms.random_forest()["algorithm"]
                scores.append(Algorithm.run(documents, algorithm, model, identifier_addition, True, False, mf, min_df, max_df))

    print("\n\n\n\nOverview:")
    scores = sorted(scores, key=lambda s: (-s[1], s[0]))
    for s in scores:
        print(s)

    print("\nBest model:")
    print(max(scores, key=itemgetter(1)))


if __name__ == '__main__':
    main()
