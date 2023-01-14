import pandas as pd
from typing import List
from flask import Flask, request, jsonify

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# load nltk data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_review(string: str) -> List[str]:
    """Preprocess one movie review by performing tokenization, removal of
    non-alphabetical tokens and stopwords, lemmatization.
    
    Args:
        string: One movie review as a single string
    
    Returns:
        A list of preprocessed tokens.
    
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

def get_lex(path_lex: str) -> List[str]:
    """Loads a sentiment-lexicon into a list of strings.
    
    Args:
        path_lex: Relative path to the lexicon-file.
    
    Returns:
        A list, containing all the words of the specified lexicon.
    
    """
    # read lexicon and transform to list
    lex = pd.read_csv(
        path_lex,
        comment=';',
        header=None,
        encoding='latin-1'
        ).to_numpy().ravel().tolist()

    # lemmatize lexicon to assure comparability to preprocessed reviews
    lemmatizer = WordNetLemmatizer()
    lex_lemma = [lemmatizer.lemmatize(w) for w in lex]

    return lex_lemma

def classifiy_lemma(lemma: List[str], lex_pos: List[str], lex_neg: List[str]) -> str:
    """Classification of the sentiment of one movie review in the form of a list 
    of preprocessed tokens by counting positive and negative words.
    
    Args:
        lemma: One movie review as a list of preprocessed tokens.
        lex_pos: A List of positive words.
        lex_neg: A list of negative words.
    
    Returns:
        A label. 'pos' if more positive words have been counted, 'neg' otherwise.       
    
    """
    pos_count = sum([1 for w in lemma if w in lex_pos])
    neg_count = sum([1 for w in lemma if w in lex_neg])

    return 'positive' if pos_count >= neg_count else 'negative'


# initiate Flask app
app = Flask(__name__)

# get positive and negative sentiment lexicons
LEX_POS = get_lex('opinion_lexicon/positive-words.txt')
LEX_NEG = get_lex('opinion_lexicon/negative-words.txt')

# define the routes
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    
    # get input data
    data = request.get_json()
    
    # predict the sentiment of the review  
    rev_pre = preprocess_review(data['review'])
    prediction = classifiy_lemma(rev_pre, LEX_POS, LEX_NEG)
    
    return jsonify({"prediction": prediction})


# run the application
if __name__ == '__main__':
    app.run()