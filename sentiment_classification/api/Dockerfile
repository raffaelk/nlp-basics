FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY templates templates/
COPY api_app.py .
COPY predict_sentiment.py .
COPY clf.joblib .
COPY vectorizer.joblib .
COPY requirements.txt .


# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api_app.py"]
