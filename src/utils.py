import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Initialize NLTK components for efficiency
# These are initialized once when the module is imported
_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Performs basic text cleaning: lowercasing, removing punctuation, and extra spaces.
    """
    text = str(text) # Ensure input is a string, robust against non-string inputs
    text = text.lower() # Convert to lowercase
    # Remove anything that's not an alphabet character or a space
    text = re.sub(r'[^a-z\s]', '', text)
    # Replace multiple spaces with a single space and strip leading/trailing/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    """
    Tokenizes text into words.
    """
    # Uses NLTK's word tokenizer, which is generally good
    return word_tokenize(text)

def remove_stopwords(words):
    """
    Removes common stopwords from a list of words.
    Assumes words are already lowercased.
    """
    return [word for word in words if word not in _stop_words]

def lemmatize_words(words):
    """
    Lemmatizes words to their base form.
    """
    return [_lemmatizer.lemmatize(word) for word in words]
