#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:41:22 2021

@author: raffael
"""

# import necessary packages
import os
import nltk
from flask import Flask, render_template, request, jsonify

# import the prediction function
from predict_sentiment import predict, dummy_tokenizer

# load nltk data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# initiate Flask
app = Flask(__name__)

# start input form
@app.route('/')
def request_review():
    return render_template('enter_review.html')


# show sentiment of review
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':

        # get review from input form
        result = request.form
        review = result['review']

        # predict sentiment
        prediction = predict(review)

        return render_template("result.html", sentiment=prediction)

@app.route('/predict', methods=['POST'])
def predict_senti():
    
    data = request.get_json()
    
    prediction = predict(data['review'])
    
    return jsonify({"prediction": prediction})


# run the application
if __name__ == '__main__':
    app.run(debug = True)
