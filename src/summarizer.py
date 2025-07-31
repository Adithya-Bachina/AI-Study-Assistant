from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer # You can try LsaSummarizer, LexRankSummarizer later
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os
import sys

# It's good practice to ensure the parent directory of src is in sys.path
# if you were running this file directly. For a multi-file project in Colab,
# the main notebook handles sys.path for imports across src/ modules.

def summarize_text(text, num_sentences=3, language="english"):
    """
    Generates an extractive summary of the input text using the TextRank algorithm.

    Args:
        text (str): The input text to summarize.
        num_sentences (int): The desired number of sentences in the summary.
        language (str): The language of the text (e.g., "english").

    Returns:
        str: The summarized text.
    """
    # Parse the text into a document format that sumy can understand
    parser = PlaintextParser.from_string(text, Tokenizer(language))

    # Initialize the stemmer and summarizer
    stemmer = Stemmer(language)
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language) # Use sumy's internal stop words list

    # Generate the summary
    summary = summarizer(parser.document, num_sentences)

    # Join the summary sentences back into a single string
    return " ".join([str(sentence) for sentence in summary])
