#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

# Function to get text from a webpage, ignoring SSL verification
def get_text(url):
    html_code_1 = requests.get(url, verify=False).text
    data = BeautifulSoup(html_code_1, 'html.parser')
    links = []
    '''Acquired all the links that are on the web page'''
    for link in data.find_all('a'):
        links.append(link.get('href'))
    '''Removed this link as we are not able to access this link'''
    links.remove('http://www.people.memphis.edu/%7Ejaffairs/')
    text = []
    for link in links:
        if link is not None:
            if ('http' or 'https') in link:
                print(link)
                html_code = requests.get(link, verify=False).text
                code_to_text = BeautifulSoup(html_code, 'html.parser').get_text()
                text.append(code_to_text)
    return text

# Function to get text from Yahoo News articles, ignoring SSL verification
def get_yahoo_news_test(urls):
    text = []
    for url in urls:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = ''
        for news_item in soup.find_all('div', class_='caas-body'):
            body = body + news_item.find('p').text + ' '
        text.append(body)
    return text

# Fetch stopwords, ignoring SSL verification
response = requests.get('https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt', verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
stop_words = soup.text.split('\n')

# Source: https://stackoverflow.com/a/47091490/4084039
def decontracted(phrase):
    # Specific contractions
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    
    # General contractions
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def preprocess(text):
    ps = PorterStemmer()
    for i in range(len(text)):
        # Decontraction
        text[i] = decontracted(text[i])
        # Remove digits
        text[i] = re.sub(r'[0-9]+', '', text[i])
        # Remove punctuation
        text[i] = re.sub(r'[^\w\s]', '', text[i])
        # Remove URLs
        text[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text[i])
        # Remove HTML-like strings
        text[i] = re.sub('<[^<]+?>', '', text[i])
        # Remove stopwords and convert to lower case, and stem words
        text[i] = ' '.join(ps.stem(e) for e in text[i].lower().split() if e not in stop_words)
    return text

if __name__ == '__main__':
    text1 = get_text('http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/')
    urls = [
        'https://news.yahoo.com/nevada-secretary-state-contender-pledges-002032329.html', 
        'https://news.yahoo.com/students-protest-ben-sasse-views-222719353.html', 
        'https://news.yahoo.com/astrazenecas-covid-vaccine-suffers-setback-230741535.html', 
        'https://www.yahoo.com/news/california-parking-space-law-aims-for-affordable-housing-and-climate-change-win-win-222640846.html', 
        'https://www.yahoo.com/news/is-it-a-mistake-to-rebuild-in-climate-danger-zones-201845727.html', 
        'https://news.yahoo.com/alzheimers-memory-loss-know-your-body-184013508.html', 
        'https://news.yahoo.com/uk-prosecutor-nurse-poisoned-2-152252482.html', 
        'https://news.yahoo.com/conservation-explosion-frog-numbers-mass-014005619.html', 
        'https://news.yahoo.com/celebration-women-science-tech-ending-013326319.html', 
        'https://news.yahoo.com/spacex-falcon-9-puts-spectacular-004613023.html'
    ]
    text2 = get_yahoo_news_test(urls)
    preprocessed_text = preprocess(text1 + text2)
    print('preprocessed_text: ', preprocessed_text)
    
    # Save the preprocessed text using pickle
    # Source: https://stackoverflow.com/a/11218504
    with open('preprocessed_text.pkl', 'wb') as handle:
        pickle.dump(preprocessed_text, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[4]:


import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

def get_inverted_indices(preprocessed_text):
    preprocessed_text_dict = {'d'+str(i) : preprocessed_text[i] for i in range(len(preprocessed_text))}

    
    inverted_indices_dict = {}

    for document in preprocessed_text_dict:
      text = preprocessed_text_dict[document]
      tokens = text.strip().split()
      for token in tokens:
        try:
          inverted_indices_dict[(token, document)] += 1
        except:
          inverted_indices_dict[token, document] = 1
    return inverted_indices_dict
    

if __name__ == '__main__':
    with open('preprocessed_text', 'rb') as handle:
        preprocessed_text = pickle.load(handle)

    inverted_indices_dict = get_inverted_indices(preprocessed_text)
    print('inverted_indices_dict: ', inverted_indices_dict)
    
    # saving the inverted indices for future use
    with open('inverted_indices', 'wb') as handle:
        pickle.dump(inverted_indices_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[7]:


import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import pickle

def get_inverted_indices(preprocessed_text):
    # Creating a dictionary with document identifiers (d1, d2, etc.) as keys
    preprocessed_text_dict = {'d' + str(i): preprocessed_text[i] for i in range(len(preprocessed_text))}
    inverted_indices_dict = {}

    # Iterating over each document and its associated text
    for document in preprocessed_text_dict:
        text = preprocessed_text_dict[document]
        tokens = text.strip().split()

        # Building the inverted index
        for token in tokens:
            try:
                inverted_indices_dict[(token, document)] += 1
            except KeyError:
                inverted_indices_dict[(token, document)] = 1

    return inverted_indices_dict

if __name__ == '__main__':
    # Load preprocessed text from file
    with open('preprocessed_text', 'rb') as handle:
        preprocessed_text = pickle.load(handle)

    # Generate inverted indices
    inverted_indices_dict = get_inverted_indices(preprocessed_text)
    print('Inverted Indices Dictionary: ', inverted_indices_dict)

    # Save the inverted indices dictionary for future use
    with open('inverted_indices', 'wb') as handle:
        pickle.dump(inverted_indices_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:





# In[11]:




import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader  
from io import BytesIO


# Create an SSL context that does not verify certificates
ssl_context = ssl._create_unverified_context()

# Load stopwords with SSL verification disabled
stopWords = urlopen("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt", context=ssl_context).read()
stopWordsContent = BeautifulSoup(stopWords, features="html.parser")
stopwordsdata = stopWordsContent.get_text().split("\n")
# Set the main URL and retrieve its content
url = "https://www.memphis.edu/"
page = requests.get(url, stream=True)
soup = BeautifulSoup(page.content, "html.parser")

count = 0
linksData = set()

# Process each link found on the main page
for link in soup.findAll('a'):
    url = link.get('href')
    if url:
        linksData.add(url)
        text = []
        tokens = []
        
        if ".pdf" in url:
            print(f"Processing PDF: {url}")
            response = requests.get(url)
            raw_text = response.content
            with BytesIO(raw_text) as data:
                reader = PdfReader(data)  # Updated to PdfReader
                for page in reader.pages:
                    text.append(page.extract_text())
            if text:
                text_content = text[0].replace("\n", " ")
                tokens = text_content.split()

        elif ".txt" in url:
            print(f"Processing TXT: {url}")
            response = requests.get(url)
            text_content = response.text.replace("\n", " ")
            tokens = text_content.split()

        elif ".php" in url or ".html" in url:
            print(f"Processing PHP/HTML: {url}")
            response = requests.get(url)
            page_soup = BeautifulSoup(response.content, 'html5lib')
            body_text = ''.join(page_soup.findAll(text=True))
            text_content = body_text.replace("\n", " ")
            tokens = text_content.split()

        # Save the processed tokens to text files in chunks of 50 words
        for i in range(0, len(tokens) - 50, 50):
            chunk = tokens[i:i + 50]
            filename = f'file{count}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(chunk))
            count += 1

# Save all processed links to a text file
with open('links.txt', 'w') as file:
    file.write("\n".join(linksData))

# List of specific website links to process
websiteLinks = [
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://cs.memphis.edu/~vrus/teaching/ir-websearch/",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html",
    "https://sites.google.com/view/dr-vasile-rus/home",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule"
]

# Process and save the content of each specific link
for webLink in websiteLinks:
    print(f"Processing Website Link: {webLink}")
    response = requests.get(webLink, verify=False)
    page_soup = BeautifulSoup(response.content, 'html5lib')
    body_text = ''.join(page_soup.findAll(text=True))
    text_content = body_text.replace("\n", " ")
    tokens = text_content.split()

    # Save the processed tokens in chunks of 50 words
    for i in range(0, len(tokens) - 50, 50):
        chunk = tokens[i:i + 50]
        filename = f'file{count}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(chunk))
        count += 1


# In[ ]:


import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import PyPDF2
from io import BytesIO
import re

import ssl
from PyPDF2 import PdfReader  





# Create an SSL context that does not verify certificates
ssl_context = ssl._create_unverified_context()

# Load stopwords with SSL verification disabled
stopWords = urlopen("https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt", context=ssl_context).read()
stopWordsContent = BeautifulSoup(stopWords, features="html.parser")
stopwordsdata = stopWordsContent.get_text().split("\n")
# Set the main URL and retrieve its content
url = "https://www.memphis.edu/"
page = requests.get(url, stream=True)
soup = BeautifulSoup(page.content, "html.parser")

count = 0
linksData = set()

# Decontract function to expand contractions in text
def decontracted(phrase):
    # Handle specific contractions
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # General contractions
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

# Preprocess text: remove numbers, punctuation, URLs, and apply stemming
def preprocess(text):
    ps = PorterStemmer()
    for i in range(len(text)):
        text[i] = decontracted(text[i])
        text[i] = re.sub(r'[0-9]+', '', text[i])  # Remove digits
        text[i] = re.sub(r'[^\w\s]', '', text[i])  # Remove punctuation
        text[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text[i])  # Remove URLs
        text[i] = re.sub('<[^<]+?>', '', text[i])  # Remove HTML tags
        # Remove stopwords and apply stemming
        text[i] = ' '.join(ps.stem(word) for word in text[i].lower().split() if word not in stopwordsdata)
    return text

# Process links from the page
for link in soup.findAll('a'):
    text = []
    url = link.get('href')
    
    if url:  # Check if the link is valid
        linksData.add(url)  # Add link to processed links set
        
        if ".pdf" in url:
            print(f"Processing PDF: {url}")
            response = requests.get(url)
            raw_text = response.content
            with BytesIO(raw_text) as data:
                pdf_reader = PyPDF2.PdfReader(data)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            cleanText = preprocess(text)
            text1 = cleanText[0].replace("\n", " ")
            tokens = text1.split()

        elif ".txt" in url:
            print(f"Processing TXT: {url}")
            text = requests.get(url).text
            cleanText = preprocess([text])
            text1 = cleanText[0].replace("\n", " ")
            tokens = text1.split()

        elif ".php" in url or ".html" in url:
            print(f"Processing PHP/HTML: {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]
            cleanText = preprocess(obj)
            text = cleanText[0].replace("\n", " ")
            tokens = text.split()

        # Save tokens in chunks of 50 to text files
        for i in range(0, len(tokens) - 50, 50):
            response_data = tokens[i:i + 50]
            filename = f'file{count}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(response_data))
            count += 1

# Save the processed links into a file
with open('links.txt', 'w') as file:
    file.write("\n".join(linksData))

# Additional list of specific website links to process
websiteLinks = [
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://cs.memphis.edu/~vrus/teaching/ir-websearch/",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/codingStyle.html",
    "https://emunix.emich.edu/~mevett/DataStructures/style-reqs.html",
    "https://sites.google.com/view/dr-vasile-rus/home",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#announcements",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#courseinfo",
    "https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/#schedule"
]

# Process the additional website links
for webLink in websiteLinks:
    print(f"Processing Website Link: {webLink}")
    response = requests.get(webLink, verify=False)
    soup = BeautifulSoup(response.content, 'html5lib')
    obj = [''.join(s.findAll(text=True)) for s in soup.findAll('body')]
    cleanText = preprocess(obj)
    text = cleanText[0].replace("\n", " ")
    tokens = text.split()

    # Save the processed tokens to text files
    for i in range(0, len(tokens) - 50, 50):
        response_data = tokens[i:i + 50]
        filename = f'file{count}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(response_data))
        count += 1


# In[ ]:


import requests
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
import nltk
nltk.download('punkt_tab')

from numpy.linalg import norm
import os
from flask import Flask, render_template, request
import ssl
import logging
import traceback

import requests as requests
from flask import Flask, request, render_template
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('punkt')
from numpy.linalg import norm
import os
ssl._create_default_https_context = ssl._create_unverified_context


searchengine = Flask(__name__)

response = requests.get('https://www.cs.memphis.edu/~vrus/teaching/ir-websearch/papers/english.stopwords.txt', verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
stop_words = soup.text.split('\n')

directory = '/Users/yashds/Downloads/Inform Retrival Project/files'


def query_term_freq_inverted_index(text):
    qurey_text = [text]

    index_vector = TfidfVectorizer(input='content', encoding='utf-8', analyzer='word', tokenizer=nltk.word_tokenize,
                                   stop_words=stop_words, ngram_range=(1, 2), use_idf=True,
                                   norm='l2')

    tfidf = index_vector.fit_transform(qurey_text)

    return tfidf.toarray()

def doc_term_freq_inverted_index():
    documentsList = []
    preprocessed_files_list = []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        preprocessed_files_list.append(file)
        with open(filepath, 'r', newline='', encoding="utf-8", errors='replace') as processingfile:
            data = processingfile.read()
            documentsList.append(data)

    index_vector = TfidfVectorizer(input='content', encoding='utf-8', analyzer='word', tokenizer=nltk.word_tokenize,
                                       stop_words=stop_words, ngram_range=(1, 2), use_idf=True,
                                       norm='l2')

    tfidf = index_vector.fit_transform(documentsList)
    return tfidf.toarray(), preprocessed_files_list


@searchengine.route('/')
def initial_load():
    return render_template('index.html')


@searchengine.route('/', methods=['POST'])


    
def output():
    text = request.form.get('input-data')
    words_list = [text]
    words_list = [i for i in words_list if i]
    if len(words_list) == 0:
        return render_template('index.html')
    
    with open('/Users/yashds/Downloads/Inform Retrival Project/links.txt', 'r', newline='', encoding='utf-8') as file:
        links = file.read().split()
    
    query_vector = query_term_freq_inverted_index(text)
    document_vector, filenames = doc_term_freq_inverted_index()

    cosinesimilarity = {}
    for i in range(len(document_vector)):
        query = np.concatenate([query_vector[0], np.ones(len(document_vector[i]) - len(query_vector[0]))])
        x = np.dot(query, document_vector[i]) / (norm(query) * norm(document_vector[i]))
        cosinesimilarity[str(i)] = x

    sorted_cosine_list = sorted(cosinesimilarity.items(), key=lambda x: x[1], reverse=True)
    cosine_sorted_dict = dict(sorted_cosine_list)

    filename_sorted = []
    filelink_sorted = []

    for key, value in cosine_sorted_dict.items():
        index = int(key)
        if index < len(filenames) and index < len(links):
            filename_sorted.append(filenames[index])
            filelink_sorted.append(links[index])
        

    return render_template('output.html', length=len(filelink_sorted), file=filename_sorted, link=filelink_sorted)


if __name__ == '__main__':
    searchengine.run(port=5002) 

