import os
import nltk
from flask import Flask, request, jsonify

# import the prediction function
from predict_sentiment import predict, dummy_tokenizer

# load nltk data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# initiate Flask app
app = Flask(__name__)

# define the routes
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    
    # get input data
    data = request.get_json()
    
    # predict the sentiment of the review
    prediction = predict(data['review'])
    
    return jsonify({"prediction": prediction})


# run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
