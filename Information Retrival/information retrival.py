#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import glob
import math
import nltk
import re

# Importing all required libraries
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
import glob
import math
import nltk
import re

User_inp_String = input("Enter list of strings separated by comma ")

# Tkinter GUI
window = Tk()
window.title("Develop a Web Interface")
window.geometry('720x720')
window.configure(background="")

a = Label(window, text="Search Input")
a.place(x=10, y=10)

a1 = StringVar()
query = Entry(textvariable=a1, width=30)
query.place(x=30, y=30)

def clicked():
    res = "Welcome to " + txt.get()
    a.configure(text=res)

def helloCallBack():
    return a1.get()

btn = ttk.Button(window, text="Submit", command=lambda: [helloCallBack, window.destroy()])
btn.place(x=60, y=60)
window.mainloop()

# Splitting the user input string
flist = User_inp_String.split(",")
read_txt = []
File1 = '/Users/yashds/Downloads/Inform Retrival Project/PreProcessing/preprocessed_text'

Preproc_Docs = [File1]

# Iterating through each file file1, file2...
for User_inp_String in Preproc_Docs:
    with open(User_inp_String, encoding='ISO-8859-1') as text:  # Changed encoding to handle Unicode errors
        read_txt = text.readlines()  # reading lines in each file

# Inverted index to retrieve documents containing at least one of the keywords
Indexing = CountVectorizer(ngram_range=(3, 3))
Indexing1 = Indexing.fit_transform(read_txt)
features = (Indexing.get_feature_names_out())

Indexing = TfidfVectorizer(ngram_range=(3, 3))
Indexing2 = Indexing.fit_transform(read_txt)

Numbering = (Indexing2.toarray())
sum1 = Indexing2.sum(axis=0)
Numbering1 = []

# Collecting features and their weights
for key, value in enumerate(features):
    Numbering1.append((value, sum1[0, key]))

a = helloCallBack()

# Creating a ranked list of documents
ranking = pd.DataFrame(Numbering1, columns=['VALUES', a])
words = (ranking.sort_values(a, ascending=False))

# Display top 100 results
print("\n\nWORDS SEARCHED : \n", words.head(100))
print("\n")
