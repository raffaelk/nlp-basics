
# Basic NLP Projects (under construction)
This repo is a collection of a few small projects in Natural Language Processing (NLP). They started as part of a semster assignment of the NLP course of Ryan Cotterell at ETH Zürich. The code for my original hand-in is in a seperate [repo](https://github.com/raffaelk/NLP20_Assignment). Here I present an extended version of the original tasks, with some added features and documentation.

## Sentiment Classification of Movie Reviews
The first project is to classify a collection of movie reviews, written in natural language, in either positive or negative sentiment.

### Technologies used

### Model
In the notebook [sentiment_classification.ipynb](https://github.com/raffaelk/nlp-basics/blob/main/sentiment_classification.ipynb) I compare a lexicon based approached to a discriminative classifier. The lexicon based approach simply counts negative and positive words, according to a sentiment dictionary. This leads to an accuracy of 68% on a test set. The discriminative model consists of a logistic regression model which has been trained on a training set an then evaluated on the same test set as the lexicon based approach. An accuracy of 85% is acchieved.

### Flask API/GUI
To productionize the logistic regression model, I built a simple flask API/GUI which can be accessed with a web browser. To use it run the following steps:
- copy the content of the [api](https://github.com/raffaelk/nlp-basics/tree/main/api) folder
- create a new virtual environment
- install the dependencies with `pip install -r requirements.txt`
- run the api script: `python api_app.py`
- go to http://localhost:5000/ in a webbrowser
There is a textbox for an own movie review. After clicking on 'submit', the sentiment of the text will be predicted. As a test case real one and five star reviews from amazon can be evaluated. The underlying prdiction model is fairly simple, so it is also easy to trick it into giving a fals prediction. As only unigrams have been used, the model is not capable of analyzing the context of important words. E.g. the sentences *"The movie was not good."* and *"The movie was good."* will both be labelled as positive.
