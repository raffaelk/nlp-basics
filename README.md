# Basic NLP Projects
This repo is a collection of some small projects in Natural Language Processing (NLP). They started as part of a semster assignment of the NLP course of Ryan Cotterell at ETH Zürich. The code for my original hand-in is in a separate [repo](https://github.com/raffaelk/NLP20_Assignment). Here I present an extended version of the original tasks, with some added features and documentation.

## Sentiment Classification of Movie Reviews
The goal of this project is to classify a collection of movie reviews, written in natural language, in either positive or negative sentiment.

### Main Technologies Used
- Language: Python 
- Visualization: Matplotlib, wordcloud
- Analysis and Modelling: pandas, scikit-learn, NLTK
- Deployment: Flask, HTML, Docker

### Model
In the notebook [sentiment_classification.ipynb](https://github.com/raffaelk/nlp-basics/blob/main/sentiment_classification.ipynb) I compare a lexicon based approached to a discriminative classifier. The lexicon based approach simply counts negative and positive words, according to a sentiment dictionary. This leads to an accuracy of 68% on a test set. The discriminative model consists of a logistic regression model which has been trained on a training set an then evaluated on the same test set as the lexicon based approach. An accuracy of 85% is achieved.

### Flask API/GUI
To productionize the logistic regression model, I built a simple flask API/GUI which can be accessed with a web browser. To use it, run the following steps:
- copy the content of the [api](https://github.com/raffaelk/nlp-basics/tree/main/api) folder
- create a new virtual environment
- install the dependencies with `pip install -r requirements.txt`
- run the api script: `python api_app.py`
- go to http://localhost:5000/ in a webbrowser

There is a text box for an own movie review. After clicking on 'submit', the sentiment of the text will be predicted. As a test case real one and five star reviews from amazon can be evaluated. The underlying prediction model is fairly simple, so it is also easy to trick it into giving a false prediction. As only unigrams have been used, the model is not capable of analyzing the context of important words. E.g. the sentences *"The movie was not good."* and *"The movie was good."* will both be labelled as positive.

### Docker Container
A Dockerfile is stored in the [api](https://github.com/raffaelk/nlp-basics/tree/main/api) folder as well. It can be used to create a Docker image and run the application in a container.

## Topic Classification of Newspaper Headlines
In this multiclass classification problem, a set of newspaper headlines is classified into distinct topic categories. 

### Main Technologies Used
- Language: Python 
- Visualization: Matplotlib, Seaborn
- Analysis and Modelling: pandas, scikit-learn, NLTK

### Data Analysis
In the first part of the notebook [topic_classification.ipynb](https://github.com/raffaelk/nlp-basics/blob/main/topic_classification.ipynb) an extended data analysis was performed. With graphical and statistical tools it could be shown how the importance of certain topics and words evolved over time.

### Model
In the second part of the notebook [topic_classification.ipynb](https://github.com/raffaelk/nlp-basics/blob/main/topic_classification.ipynb) a predictive model to automatically classify headlines has been created. An accuracy of approximately 75% was achieved.
