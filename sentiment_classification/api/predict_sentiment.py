#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 18:30:25 2021

@author: raffael
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from typing import List

from joblib import load


# redefine some of the functions needed (copied from the main notebook)
def preprocess_review(string: str) -> List[str]:
    """Preprocess one movie review by performing tokenization, removal of
    non-alphabetical tokens and stopwords, lemmatization.

    Args:
        string: One movie review as a single string.

    Returns:
        A List of preprocessed tokens.

    """
    # tokenize input
    tokens = word_tokenize(string.lower())

    # remove non-alphabetical tokens
    tokens_alpha = [w for w in tokens if w.isalpha()]

    # remove stopwords
    tokens_no_stops = [w for w in tokens_alpha
                       if w not in stopwords.words('english')]

    # lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens_lemma = [lemmatizer.lemmatize(w) for w in tokens_no_stops]

    return tokens_lemma


def dummy_tokenizer(text: str) -> str:
    """ Dummy function, just returns the input argument."""
    return text


def predict(my_review: str) -> str:
    """ Predict the sentiment of a single movie review.

    Args:
        my_review: One movie review as a single string.

    Returns:
        Predicted sentiment of the review.
    """
    # load pre saved model
    vectorizer = load('vectorizer.joblib')
    clf = load('clf.joblib')

    # preprocess and predict sentiment
    my_review_pre = preprocess_review(my_review)
    my_review_tfidf = vectorizer.transform([my_review_pre])
    my_pred = clf.predict(my_review_tfidf)

    sentiment = 'positive' if my_pred[0] else 'negative'

    return sentiment
