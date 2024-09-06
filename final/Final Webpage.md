# Flask-based Search Engine

## Overview
This project implements a simple search engine using Flask, Python, and text processing techniques. The search engine allows users to input queries and retrieve relevant documents ranked by cosine similarity based on the TF-IDF representation of the text data.

## Key Features
- **Flask Web Interface**: A user-friendly interface to search and view results.
- **Text Preprocessing**: Tokenization, stemming (Porter Stemmer), and stopword removal for efficient document comparison.
- **Cosine Similarity**: Documents are ranked using cosine similarity with TF-IDF vectorization.
- **File Handling**: Processes multiple `.txt` files for information retrieval.

## Prerequisites
- Python 3.x
- Flask: `pip install flask`
- Scikit-learn: `pip install scikit-learn`
- NLTK: `pip install nltk`

## Usage

1. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2. **Place Text Files**:
   - Ensure your text files are placed in the `/path/to/final/files/` directory.
   - Update the stopwords file path and file directory if necessary.

3. **Run the Flask Application**:
    ```bash
    python final.py
    ```
   - The app will be accessible at `http://127.0.0.1:5000`.

## How It Works
- **TF-IDF Vectorization**: Text files are vectorized using the TF-IDF method.
- **Cosine Similarity**: User queries are compared with preprocessed documents, and results are ranked based on similarity.
- **Flask Interface**: Users can input search queries via a web interface and view ranked results with links to the original documents.

## File Structure
- `final.py`: The main script that runs the Flask app and handles text processing and search functionality.
- `templates/`: Contains HTML templates for the Flask web interface.
- `files/`: Directory where the text files to be searched are stored.
- `english.stopwords.txt`: A file containing stopwords that are excluded from text processing.

## Future Enhancements
- Expand the ranking system with additional algorithms like BM25.
- Improve the user interface for a better search experience.
- Implement caching for faster repeated queries.

