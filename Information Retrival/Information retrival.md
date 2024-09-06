# Information Retrieval System

## Overview
This project implements an information retrieval system using a GUI created with Tkinter. It allows users to input a search query and retrieves relevant documents based on various text processing techniques, such as tokenization and TF-IDF vectorization.

## Key Features
- **Tkinter GUI**: Provides a graphical interface for user interaction.
- **Text Processing**: Uses tokenization and vectorization (CountVectorizer and TF-IDF) to process and compare documents.
- **Cosine Similarity**: Ranks documents based on the similarity to the user's input query.
- **File Handling**: Processes multiple `.txt` files for search and retrieval.

## Prerequisites
- Python 3.x
- Tkinter (comes pre-installed with Python)
- Scikit-learn: `pip install scikit-learn`
- NLTK: `pip install nltk`

## Usage

1. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2. **Place Text Files**:
   - Ensure your text files are placed in the `/path/to/files/` directory.

3. **Run the Application**:
    ```bash
    python information\ retrival.py
    ```
   - A GUI will appear where you can enter a search query.

4. **Search Process**:
   - The system will process your query and search the text files using vectorization techniques (TF-IDF or CountVectorizer).
   - The results will be ranked based on cosine similarity.

## File Structure
- `information\ retrival.py`: The main script that runs the GUI and handles text processing and search functionality.
- `files/`: Directory where the text files to be searched are stored.

## Future Enhancements
- Expand the search capabilities with additional text processing techniques like lemmatization or stemming.
- Improve the GUI to display results within the application.
- Implement more advanced ranking algorithms like BM25 for better result relevance.

