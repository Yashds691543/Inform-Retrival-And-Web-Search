from flask import Flask, render_template, request
import glob
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import wordpunct_tokenize as tokenize
from nltk.stem.porter import PorterStemmer
import string

# Initialize Flask app
searchengine = Flask(__name__)

# Path to the stopwords file
local_stopwords_path = '/Users/yashds/Downloads/Inform Retrival Project/final/english.stopwords.txt'

# Read stopwords from the local file
with open(local_stopwords_path, 'r') as file:
    stop_words = set(file.read().splitlines())

# Function to read and preprocess files
def get_preprocessed_files():
    preprocessed_files = []
    for preprocessedFile in sorted(glob.glob('/Users/yashds/Downloads/Inform Retrival Project/final/files/*.txt')):
        with open(preprocessedFile, 'r', newline='', encoding="utf-8") as file:
            preprocessed_data = file.read()
            preprocessed_files.append(preprocessed_data)
    return preprocessed_files

# Function to remove special characters from a query string
def remove_special_char(query_str):
    return re.sub('[^a-zA-Z]+', ' ', query_str).strip().lower()

# Function to evaluate a query using cosine similarity
def get_evaluation(query_str):
    preprocessed_files = get_preprocessed_files()
    query_str = remove_special_char(query_str)
    preprocessed_files_data = preprocessed_files + [query_str]

    porter = PorterStemmer()
    # Tokenize and stem the words, remove punctuation and stop words
    vector_array = [[porter.stem(token.lower()) for token in tokenize(file.translate(str.maketrans("", "", string.punctuation))) if token.lower() not in stop_words] for file in preprocessed_files_data]
    transform_vector = [' '.join(vector) for vector in vector_array]

    # Compute TF-IDF and cosine similarity
    tf_idf = TfidfVectorizer().fit_transform(transform_vector)
    cosine_sim = cosine_similarity(tf_idf[-1:], tf_idf)
    cosine_data_array = cosine_sim[0]

    # Sort the cosine similarity values
    cosine_dict_data = dict(enumerate(cosine_data_array[0:-1]))
    cosine_sorted_array = sorted(cosine_dict_data.items(), key=lambda cosine_value: cosine_value[1], reverse=True)

    cosine_sorted_dict = dict(cosine_sorted_array)

    # Evaluate related documents and calculate precision, recall, F-score
    related = [dict_value for dict_value in cosine_sorted_dict.values() if dict_value < cosine_sorted_array[0][1] / 4]
    margin = cosine_sorted_array[0][1] / 2
    marginal = 0.5 * margin

    similar_count = 1
    actual_count = 1
    for key, value in cosine_sorted_dict.items():
        if value >= marginal:
            actual_count += 1
            similar_count += 1
        if value >= margin:
            similar_count += 1

    relevant_displayed = int(0.6 * actual_count)
    precision = relevant_displayed / similar_count if similar_count else 0
    recall = relevant_displayed / len(related) if related else relevant_displayed / similar_count
    f_score = 2 * (precision * recall / (precision + recall)) if (precision + recall) != 0 else 0

    return query_str, precision, recall, f_score

# Route to display the initial search page
@searchengine.route('/')
def initial_load():
    return render_template('index.html')

# Route to handle query submission and display evaluation results
@searchengine.route('/', methods=['POST'])
def output():
    query_strs = request.form.getlist('queries')
    print("Received queries:", query_strs)  # Debugging: Print received queries
    results = []

    for query in query_strs:
        query_str, precision, recall, f_score = get_evaluation(query)
        print(f"Evaluated: {query_str}, Precision: {precision}, Recall: {recall}, F-Score: {f_score}")  # Debugging
        results.append((query_str, precision, recall, f_score))

    return render_template('output.html', results=results)


# Run the Flask app
if __name__ == '__main__':
    searchengine.run(port=5066, debug=True)
