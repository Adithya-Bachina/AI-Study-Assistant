# src/question_generator.py - UPGRADED WITH ANSWERS

from nltk.tokenize import sent_tokenize
import re

def generate_questions_from_text(text, keywords, num_questions=5):
    """
    Generates a list of question-answer dictionaries.
    Includes 'Fill-in-the-Blank' questions with answers and 'What is...' questions.

    Args:
        text (str): The original text.
        keywords (list): A list of keywords.
        num_questions (int): The number of questions to generate.

    Returns:
        list: A list of dictionaries, e.g., [{'question': '...', 'answer': '...'}].
    """
    qa_pairs = []
    processed_sentences = set()  # Avoid using the same sentence twice
    sentences = sent_tokenize(text)

    # Prioritize creating fill-in-the-blank questions
    for keyword in keywords:
        if len(qa_pairs) >= num_questions:
            break

        for sentence in sentences:
            if sentence in processed_sentences:
                continue

            if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
                blank_sentence = re.sub(
                    r'\b' + re.escape(keyword) + r'\b', '_______', sentence, flags=re.IGNORECASE, count=1
                )
                
                # Check if the question is meaningful (not just a blank)
                if blank_sentence != sentence:
                    qa_pairs.append({
                        'question': f"Fill in the blank: \"{blank_sentence}\"",
                        'answer': keyword.capitalize()
                    })
                    processed_sentences.add(sentence)
                    break # Move to the next keyword

    # If not enough questions, add "What is..." questions as fallback
    current_keywords_index = 0
    while len(qa_pairs) < num_questions and current_keywords_index < len(keywords):
        keyword = keywords[current_keywords_index]
        question = f"What is {keyword.lower()}?"
        
        # Avoid adding a duplicate question
        is_duplicate = any(d['question'] == question for d in qa_pairs)
        if not is_duplicate:
            qa_pairs.append({
                'question': question,
                'answer': "Refer to the text for the definition." # Generic answer for this type
            })
        current_keywords_index += 1

    return qa_pairs[:num_questions]