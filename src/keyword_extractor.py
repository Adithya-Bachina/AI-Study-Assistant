import pke
from nltk.corpus import stopwords
import os
import sys

# Initialize NLTK stopwords for efficiency
_stop_words = list(stopwords.words('english'))

def extract_keywords(text, num_keywords=5):
    """
    Extracts keyphrases from the input text using the RAKE algorithm.

    Args:
        text (str): The input text to extract keywords from.
        num_keywords (int): The desired number of keywords to extract.

    Returns:
        list: A list of extracted keywords (strings).
    """
    # Ensure text is a string
    text = str(text)

    # Initialize the RAKE extractor
    extractor = pke.unsupervised.Rake()

    # Load the document. pke handles internal tokenization, POS tagging using spaCy (if configured).
    extractor.load_document(input=text, language='en')

    # Candidate selection: identify sequences of nouns and adjectives as potential keyphrases.
    # n=2 allows for bigrams (two-word phrases). You can adjust this (e.g., n=3 for trigrams).
    extractor.candidate_selection(n=2)

    # Candidate weighting: apply the RAKE algorithm to score candidates.
    # Use NLTK's stopwords directly with pke's weighting.
    extractor.candidate_weighting(stoplist=_stop_words)

    # Get the top N best keyphrases based on their RAKE score.
    keyphrases = extractor.get_n_best(n=num_keywords)

    # Return just the keyphrase text, not the score (keyphrases are (text, score) tuples)
    return [kp[0] for kp in keyphrases]
