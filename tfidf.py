__author__ = 'wanyanxie'
import numpy as np
import glob
import xml.etree.cElementTree as ET
import string
from collections import Counter
import re
import os

def filelist(pathspec):
    #print pathspec
    files = glob.glob(pathspec + "/*.xml")
    return files

#print len(filelist("./reuters-vol1-disk1-subset/*.xml"))

def get_text(fileName):

    """
    Read an xml file and return the text from <title> and <text>.
    Concatenate those two elements, putting a space in between so it doesn't
    form an incorrect compound word.
    """
    combined = []
    if not (os.stat(fileName).st_size == 0):
        tree = ET.parse(fileName)
        title = tree.find("title").text
        text_ref = tree.find("text").findall("p")
        text = [ref.text for ref in text_ref]
        combined = [title] + text
    return " ".join(combined)



def words(d):
    """
    Replace numbers, punctuation, tab, carriage return, newline with space
    wordlist = Split d into words
    Strip out w in wordlist smaller than 3 letters
    Normalize w in wordlist to lowercase
    """
    d = d.lower()
    d = re.sub("[^a-z]", " ", d)
    wordlist = d.split(" ")
    wordlist = [w for w in wordlist if len(w) >= 3]
    return wordlist

def create_indexes(filelist):
    df = Counter() ### document frequency
    tf_map = {}  ### term frequency, each file has a term frequency map
   # i = 0
    for f in filelist:
       # i += 1
       # print i, f
        d = get_text(f)
        wordlist = words(d)
        n = len(wordlist)
        tf = Counter(wordlist)
        # walk unique word list
        for t in tf:
            tf[t] = float(tf[t])/n # convert to a term freq from count
            df[t] += 1
        tf_map[f] = tf
    return(tf_map, df)
#
# fileName = filelist("./reuters-vol1-disk1-subset/*.xml")[0]
# filelist = filelist("./reuters-vol1-disk1-subset/*.xml")[0:1]
# create_indexes(filelist)

def doc_tfidf(tf, df, N):
    """
    :param tf: Term to frequency map tf
    :param df: Term to document count map df
    :param N: Number of documents N
    :return: Map of each term in doc (tf ) to TFIDF score
    """
    tfidf = {}
    for t in tf:
        df_t = (float(df[t]) + 1)/(N + 1)
        tfidf[t] = tf[t] * np.log(1.0/df_t)
    return tfidf

def create_tfidf_map(files):
    """
    :param files: Input: List of xml filenames f iles
    :return: Map from file name to map of term to TFIDF scores
    """
    tfidf_map = {}
    (tf_map, df) = create_indexes(files)
    N = len(files)
    for f in files:
        tfidf = doc_tfidf(tf_map[f], df, N)
        tfidf_map[f] = tfidf
    return tfidf_map

def create_indexes_search_engine(filelist):
    df = Counter() ### document frequency
    tf_map = {}  ### term frequency, each file has a term frequency map
   # i = 0
    for f in filelist:
       # i += 1
       # print i, f
        d = get_text(f)
        wordlist = words(d)
        n = len(wordlist)
        tf = Counter(wordlist)
        # walk unique word list
        for t in tf:
            tf[t] = float(tf[t])/n # convert to a term freq from count
            df[t] += 1
        tf_map[f] = tf
    return(tf_map, df)

def search(query):
    # query is a string with a list of words
    # find list of documents for each term in query
    # docs = intersection of these files
    # compute sum of TFIDF scores for each term in query relative to each document in docs
    # sort documents by reverse score
    # Returns a list of document filenames in reverse TFIDF order
    docs = []

    return docs




