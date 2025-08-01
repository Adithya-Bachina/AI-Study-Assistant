# app/app.py - UPGRADED WITH ANALYSIS

from flask import Flask, render_template, request
import os
import sys
from io import BytesIO
import base64
from wordcloud import WordCloud

# --- Project Path Setup ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Import Core Functions ---
try:
    from src.summarizer import summarize_text
    from src.keyword_extractor import extract_keywords
    from src.question_generator import generate_questions_from_text
    from src.file_parser import (
        extract_text_from_pdf,
        extract_text_from_docx,
        extract_text_from_pptx
    )
    # NEW: Import analyzer functions
    from src.analyzer import analyze_text_statistics, extract_concepts
    print("Successfully imported NLP, file parsing, and analysis functions from src.")
except ImportError as e:
    print(f"Error importing functions: {e}")

# --- Flask App Initialization ---
UPLOAD_FOLDER = os.path.join(project_root, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_word_cloud(text):
    if not text:
        return None
    try:
        wordcloud = WordCloud(
            width=800, height=400, background_color='rgba(255, 255, 255, 0)', 
            mode='RGBA', collocations=False
        ).generate(text)
        
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format="PNG")
        img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return img_str
    except ValueError:
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        input_text = ""
        action = request.form.get('action')
        
        # File Handling
        if 'file_upload' in request.files and request.files['file_upload'].filename != '':
            file = request.files['file_upload']
            if file and allowed_file(file.filename):
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file_stream = BytesIO(file.read())
                
                if file_extension == 'pdf': input_text = extract_text_from_pdf(file_stream)
                elif file_extension == 'docx': input_text = extract_text_from_docx(file_stream)
                elif file_extension == 'pptx': input_text = extract_text_from_pptx(file_stream)
                elif file_extension == 'txt': input_text = file_stream.getvalue().decode('utf-8', errors='ignore')
            else:
                return render_template('index.html', error="Invalid file type.")
        
        if not input_text:
            input_text = request.form.get('text_input', '')

        if not input_text.strip():
            return render_template('index.html', error="Please provide text or a file.")

        try:
            num_sentences = int(request.form.get('num_sentences', 3))
            num_keywords = int(request.form.get('num_keywords', 10))
            num_questions = int(request.form.get('num_questions', 5))
        except (ValueError, TypeError):
            num_sentences, num_keywords, num_questions = 3, 10, 5

        summary_result, keywords_result, questions_result, error_message = None, None, None, None
        word_cloud_image, stats_result, concepts_result = None, None, None # NEW: analysis results

        try:
            if action == 'summarize':
                summary_result = summarize_text(input_text, num_sentences=num_sentences)
            
            elif action == 'keywords':
                keywords = extract_keywords(input_text, num_keywords=num_keywords)
                keywords_result = ", ".join(keywords)
                if keywords_result: word_cloud_image = create_word_cloud(keywords_result)
            
            elif action == 'questions':
                keywords_for_questions = extract_keywords(input_text, num_keywords=num_questions * 2)
                questions_result = generate_questions_from_text(input_text, keywords_for_questions, num_questions=num_questions)
            
            # NEW: Handle analysis action
            elif action == 'analyze':
                stats_result = analyze_text_statistics(input_text)
                concepts_result = extract_concepts(input_text)

            elif action == 'all':
                summary_result = summarize_text(input_text, num_sentences=num_sentences)
                
                num_to_extract = max(num_keywords, num_questions * 2)
                all_keywords = extract_keywords(input_text, num_keywords=num_to_extract)
                
                keywords_result = ", ".join(all_keywords[:num_keywords])
                if keywords_result: word_cloud_image = create_word_cloud(keywords_result)
                
                questions_result = generate_questions_from_text(input_text, all_keywords, num_questions=num_questions)
                
                # NEW: Add analysis to 'all'
                stats_result = analyze_text_statistics(input_text)
                concepts_result = extract_concepts(input_text)

        except Exception as e:
            error_message = f"An error occurred: {e}"

        return render_template(
            'index.html',
            original_text=input_text,
            summary_result=summary_result,
            keywords_result=keywords_result,
            questions_result=questions_result,
            word_cloud_image=word_cloud_image,
            stats_result=stats_result,           # NEW
            concepts_result=concepts_result,     # NEW
            num_sentences=num_sentences,
            num_keywords=num_keywords,
            num_questions=num_questions,
            error=error_message
        )

if __name__ == '__main__':
    app.run(debug=True)