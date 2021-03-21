#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:41:22 2021

@author: raffael
"""

from predict_sentiment import predict, dummy_tokenizer

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def request_review():
    # review = "Bad! The actors weren't motivated to do a good job."
    return render_template('enter_review.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      
      review = result['review']
      
      sent = predict(review)
      
      return render_template("result.html",sentiment = sent)
    

if __name__ == '__main__':
   app.run(debug = True)


