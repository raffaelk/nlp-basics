# Sentiment Classification of Movie Reviews & Deployment with Docker
The goal of this project is to classify a collection of movie reviews, written in natural language, in either positive or negative sentiment.

This project started as part of a semster assignment of the NLP course of Ryan Cotterell at ETH Zürich. The code for my original hand-in is in a separate [repo](https://github.com/raffaelk/NLP20_Assignment). Here I present an extended version of the original tasks, with some added features and documentation.

## Main Technologies Used
- Language: Python 
- Visualization: Matplotlib, wordcloud
- Analysis and Modelling: pandas, scikit-learn, NLTK
- Deployment: Flask, SQL, HTML, Docker
- Set-Up: Bash

## Model
In the notebook [sentiment_classification.ipynb](sentiment_classification.ipynb) (or [open with nbviewer](https://nbviewer.jupyter.org/github/raffaelk/nlp-basics/blob/main/sentiment_classification/sentiment_classification.ipynb)) I compare a lexicon based approached to a discriminative classifier. The lexicon based approach simply counts negative and positive words, according to a sentiment dictionary. This leads to an accuracy of 68% on a test set. The discriminative model consists of a logistic regression model which has been trained on a training set an then evaluated on the same test set as the lexicon based approach. An accuracy of 85% is achieved.

To get all the data sets either follow the instructions in the notebook or run the bash script [set_up.sh](set_up.sh).

## APIs and Containerized App

### Running the App
To deploy the models, I built a simple application running in multiple docker containers communicating over REST-APIs and orchestrated with docker-compose. To start it, run the following steps:
- install [docker](https://www.docker.com/)
- copy the content of the [deployment](deployment) folder
- run `$ docker-compose up -d --build` in a terminal
- go to http://localhost:5000/ in a webbrowser

There is a text box for an own movie review. After clicking on 'submit', the sentiment of the text will be predicted. As a test case real one and five star reviews from amazon can be evaluated. The underlying prediction models are fairly simple, so it is also easy to trick it into giving a false prediction. As only unigrams have been used, the model is not capable of analyzing the context of important words. E.g. the sentences *"The movie was not good."* and *"The movie was good."* will both be labelled as positive.

### Description

The full code for the app is in the [deployment](deployment) folder. The docker compose file orchestrates four services:
- **prediction_app**: This service runs a web application built with HTML and flask. It acts as a GUI where movie review texts can be submitted and the resulting predictions will be displayed. The communication with the prediction models is handeled with REST-APIs and review text and predictions are stored in a database.
- **mysql_db**: A MySQL database will be set up in a container from the official MySQL image.
- **model_logreg_api**: The discriminative classifier model runs as an independent service. The prediction app can send POST requests to the model's predict endpoint.
- **model_lex_api**: Independent service for the lexicon based model.

### Endpoints

The prediction model services have the following endpoint:

**POST** `/predict`

Body:
```json
{
  "review": "Some movie review text."
}
```

Response:
```json
{
  "prediction": "positive / negative"
}
```

