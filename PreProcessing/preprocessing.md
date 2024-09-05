# Preprocessing and Search Engine Notebook

## Overview
This repository contains a Jupyter Notebook that implements web scraping and a basic search engine using Flask and Python. The search engine allows users to input queries and receive ranked documents based on cosine similarity calculations. The main components of the notebook include:

- **Web Scraping**: Automatically retrieving data from specified web pages.
- **Text Preprocessing**: Processing text documents and calculating term frequencies and inverted indices.
- **Cosine Similarity**: Ranking documents by comparing a query's term frequency vector with preprocessed document vectors.
- **Flask Web Application**: A simple web interface for users to interact with the search engine.

## Key Features
- **Flask Framework**: Provides a web interface for searching and displaying results.
- **Cosine Similarity**: Documents are ranked using a cosine similarity metric.
- **Web Scraping**: Pre-fetches data from multiple URLs for information retrieval.

## Prerequisites
- Python 3.9 or above
- Flask: `pip install flask`
- NumPy: `pip install numpy`
- NLTK (for text processing): `pip install nltk`

## Usage
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    ```
2. Install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask application:
    ```bash
    python app.py
    ```
4. Access the search engine via `http://127.0.0.1:5002` in your browser.

## How It Works
- The search engine reads a list of pre-processed documents.
- A query is entered into the interface, which is transformed into a vector.
- Cosine similarity is calculated between the query vector and document vectors.
- Results are ranked and displayed with links to the original documents.

## File Structure
- `preprocessing.ipynb`: The main notebook file that contains all the code for scraping, text preprocessing, and search engine logic.
- `app.py`: The Flask app that runs the search engine web interface.
- `templates/`: Contains the HTML templates for the web interface.

## Future Improvements
- Implement more advanced text processing techniques such as lemmatization.
- Expand the ranking algorithm with additional features like BM25.
- Add support for document relevance feedback.
