# AI-Powered Study Assistant: Text Summarizer & Keyword Extractor

## Project Overview
This project aims to create an intelligent web application designed to help users, especially students, efficiently process and understand long texts. It provides two core functionalities: extractive text summarization and keyword/keyphrase extraction.

## Features (Minimum Viable Product - MVP)
* **Extractive Summarization:** Generates a concise summary by extracting the most important sentences directly from a given text.
* **Keyword/Keyphrase Extraction:** Identifies key terms and phrases highly relevant to the text content.

## Technologies Used
* Python
* Natural Language Processing (NLP) libraries: `sumy` (for TextRank summarization) and `pke` (for RAKE keyword extraction)
* Flask (web framework - planned for later development in VS Code)
* Google Colab (for initial NLP development and prototyping)
* Git & GitHub (for version control)

## Setup and Usage (Colab Development Phase)
1.  **Open this Colab Notebook:** `01_nlp_exploration.ipynb`
2.  **Run all cells from top to bottom.** This will:
    * Install necessary Python libraries.
    * Download NLTK data and prepare PKE resources.
    * Mount your Google Drive (optional, for persistent storage).
    * Clone/navigate into your GitHub repository.
    * Create the necessary project structure and initial files (`.gitignore`, `requirements.txt`, `src/`).
    * (Future: Create and test the `src/utils.py`, `src/summarizer.py`, and `src/keyword_extractor.py` files.)

## Future Enhancements (Roadmap)
* Build a user-friendly web interface using Flask.
* Implement basic factual question generation.
* Explore abstractive summarization using advanced Transformer models.
* Allow file uploads for summarization.
* Deployment to a cloud platform (e.g., Render, Heroku).

## License
[Optional: Add a license here, e.g., MIT License - you can pick one from choosealicense.com]

---
*(This README will be updated as the project progresses.)*
