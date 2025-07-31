from rake_nltk import Rake # Import the Rake class from rake_nltk
from nltk.corpus import stopwords
import os
import sys

# Initialize NLTK stopwords for efficiency (rake_nltk can use these)
_stop_words = list(stopwords.words('english'))

def extract_keywords(text, num_keywords=5):
    """
    Extracts keyphrases from the input text using the RAKE algorithm (via rake_nltk).

    Args:
        text (str): The input text to extract keywords from.
        num_keywords (int): The desired number of keywords to extract.

    Returns:
        list: A list of extracted keywords (strings).
    """
    # Ensure text is a string
    text = str(text)

    # Initialize the Rake extractor
    # You can pass a custom list of stopwords and even punctuation here if needed
    rake_instance = Rake(stopwords=_stop_words)

    # Extract keywords from the text
    rake_instance.extract_keywords_from_text(text)

    # Get the top N ranked phrases.
    # get_ranked_phrases() returns a list of strings, ranked highest to lowest.
    ranked_phrases = rake_instance.get_ranked_phrases()

    # Return the top 'num_keywords'
    return ranked_phrases[:num_keywords]
