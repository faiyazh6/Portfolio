# Faiyaz Hasan 

import nltk
nltk.download('stopwords')
nltk.download('punkt')
import sys
import string
import os
import numpy as np
from nltk.tokenize import word_tokenize 

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dict_of_files = {} 
    for root, _, files in os.walk(directory): 
        for f in files: 
            if not f.startswith('.'): 
                # open the text file 
                text_file = open(os.path.join(root, f), "r")  
                # returns content as a string 
                dict_of_files[f] = text_file.read()
                text_file.close() 
    # return the dictionary of files with txt 
    return dict_of_files 

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # defining punctuation and stop words 
    punctuation = string.punctuation
    stop_words = nltk.corpus.stopwords.words("english")

    # using word_tokenize to filter the document 
    tokenized_doc = word_tokenize(document.lower()) 
    filtered_words = []
    for elem in tokenized_doc: 
        if elem not in punctuation and elem not in stop_words: 
            filtered_words.append(elem) 
    return filtered_words 

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    dict_with_idf = {} 
    length_of_documents = len(documents) 
    
    # create a set of all the words in all the documents
    all_words = []
    for list_of_words in documents.values(): 
        for word in list_of_words: 
            all_words.append(word) 

    # set only gives us unique words 
    all_words = set(all_words) 

    for word in all_words: 
        count = 0 
        for list_of_words in documents.values():
            if word in list_of_words:
                count += 1
        # calculating the idf and then inserting it into the dictionary 
        idf = np.log(length_of_documents/count) 
        dict_with_idf[word] = idf 
    
    # return the dictionary with idf 
    return dict_with_idf 

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    sum_of_tfidfs = [] 

    # calculate tf idf score of each file and add to dictionary 
    for file, list_of_words in files.items(): 
        tf_idfs = 0 
        for word in query: 
            tf_idf = list_of_words.count(word) * idfs[word] 
            tf_idfs += tf_idf 
        sum_of_tfidfs.append((file, tf_idfs)) 

    # sorting the list in descending order 
    sorted_lst = sorted(sum_of_tfidfs, key=lambda x: x[1], reverse = True) 

    list_of_files = [] 
    for elem in sorted_lst: 
        list_of_files.append(elem[0]) 
    
    # return a list of the filenames of the the n top files that match the query
    return list_of_files[:n] 

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sum_of_idfs = {} 
    # finding the common words 
    for sentence, list_of_words in sentences.items(): 
        common_words = query.intersection(list_of_words) 

        # getting the idfs 
        all_idfs = 0 
        for word in common_words: 
            all_idfs += idfs[word] 

        # calculating the query density 
        query_density = 0
        for word in list_of_words:
            if word in query:
                query_density += 1
        query_density /= len(list_of_words)

        sum_of_idfs[sentence] = (all_idfs, query_density)
    
    # sorting the list in descending order 
    sorted_lst = sorted(sum_of_idfs.items(), key = lambda x: (x[1][0], x[1][1]), reverse =True)
    
    list_of_sentences = [] 
    for elem in sorted_lst: 
        list_of_sentences.append(elem[0]) 
    
    # return a list of the n top sentences that match the query
    return list_of_sentences[:n]

if __name__ == "__main__":
    main()