import CSVHandler
import os
import NaiveBayes
import TFIDF

# If import is needed
if os.path.exists("categorized/all_subreddits.tsv"):
    CSVHandler.prepare_subreddits()

modes = ["normal", "title_only", "text_only"]

current_mode = modes[0]

documents = CSVHandler.get_document(current_mode)

print("\n")
NaiveBayes.run(documents)
TFIDF.run(documents)
