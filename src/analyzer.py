# src/analyzer.py

import spacy
import textstat
from collections import defaultdict

# Load the spaCy model once when the module is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Spacy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

def analyze_text_statistics(text):
    """
    Calculates readability and other text statistics.
    Returns a dictionary of metrics.
    """
    if not text:
        return {}
        
    return {
        "flesch_grade": textstat.flesch_kincaid_grade(text),
        "reading_time_minutes": round(textstat.reading_time(text, ms_per_char=14.69) / 60, 2),
        "sentence_count": textstat.sentence_count(text),
        "word_count": textstat.lexicon_count(text, removepunct=True)
    }

def extract_concepts(text):
    """
    Extracts named entities (concepts) from the text using spaCy.
    Groups them by a more readable type (e.g., "People", "Organizations").
    """
    if not nlp or not text:
        return {}

    # Map spaCy labels to more user-friendly names
    LABEL_MAP = {
        "PERSON": "People",
        "ORG": "Organizations",
        "GPE": "Geopolitical Entities",
        "LOC": "Locations",
        "PRODUCT": "Products",
        "EVENT": "Events",
        "WORK_OF_ART": "Works of Art",
        "LAW": "Laws & Legal"
    }
    allowed_labels = set(LABEL_MAP.keys())

    doc = nlp(text)
    concepts = defaultdict(set)
    
    for ent in doc.ents:
        # Check if the entity is in our allowed list and not just whitespace
        if ent.label_ in allowed_labels and len(ent.text.strip()) > 2:
            human_readable_label = LABEL_MAP.get(ent.label_)
            concepts[human_readable_label].add(ent.text.strip())
            
    # Convert sets to sorted lists for consistent ordering
    sorted_concepts = {label: sorted(list(entities)) for label, entities in concepts.items()}
    return sorted_concepts