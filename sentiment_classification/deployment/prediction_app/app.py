from flask import Flask, render_template, url_for, request, redirect
import requests
from sqlalchemy import create_engine, text
import os
import logging
import time

# define logger
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', 
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
                   )
logger = logging.getLogger()

# env var for db connection
MYSQL_USER = os.environ.get('MYSQL_USER') #'root'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') #'secret'
MYSQL_HOST = os.environ.get('MYSQL_HOST') #'localhost'

##################################################
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'secret'
MYSQL_HOST = 'localhost'
###################################################

def set_up_database(mysql_user, mysql_password, mysql_host):
    """
    Sets up the necessary database and table.
    """
    
    # create connection to the mysql db
    engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:3306/')
    
    # initialize db and table
    connect_retries = 5
    while connect_retries > 0:
        try:
            with engine.connect() as con:
                con.execute("CREATE DATABASE IF NOT EXISTS sentiment_app;")

                con.execute(f"""
                CREATE TABLE IF NOT EXISTS sentiment_app.predictions (
                    id INT AUTO_INCREMENT,
                    review TEXT,
                    prediction_lex VARCHAR(10),
                    prediction_logreg VARCHAR(10),
                    PRIMARY KEY(ID)
                );
                """)
                connect_retries = 0
                logging.info("Database successfully set up.")
        except:
            logger.error(f'Database connection during set up failed. Retry in 5 seconds. {connect_retries} retries left.')
            connect_retries -= 1
            time.sleep(5)

        
    return engine

# set up database and get engine
ENGINE = set_up_database(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST)

# initialize flask app
app = Flask(__name__)

# define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        # get review text from input form
        review = {"review": request.form['content']}
        
        # predict with lexicon model
        try:
            response_lex = requests.post('http://localhost:5002/predict', json=review).json()
        except:
            response_lex = {"prediction": "error"}
            logging.error("No response from lexicon model.")
        
        # predict with logreg model
        try:
            response_logreg = requests.post('http://localhost:5001/predict', json=review).json()
        except:
            response_logreg = {"prediction": "error"}
            logging.error("No response from logreg model.")
        
        # write precictions to the database
        try:
            with ENGINE.connect() as con:
                con.execute(text(f"""
                INSERT INTO sentiment_app.predictions (review, prediction_lex, prediction_logreg)
                VALUES (:rev, :pred_lex, :pred_logreg);
                """), rev=review['review'], pred_lex=response_lex['prediction'], pred_logreg=response_logreg['prediction'])
        except:
            logger.error("Could not write predictions to the database.")
        
        return redirect(f'/?lex={response_lex["prediction"]}&logreg={response_logreg["prediction"]}')
        
    else:
        try:
            with ENGINE.connect() as con:
                response = con.execute("""
                SELECT id, review, prediction_lex, prediction_logreg 
                FROM sentiment_app.predictions
                ORDER BY id DESC;
                """)
            review_list = [dict(row) for row in response]
            histo_db = True
        except:
            logger.error("Could not get history from database.")
            review_list = []
            histo_db = False
        
        return render_template('index.html', review_list=review_list, histo_db=histo_db)
    
@app.route('/history/clear', methods=['GET'])
def clear_history():
    try:
        with ENGINE.connect() as con:
            con.execute("TRUNCATE TABLE sentiment_app.predictions")
    except:
        logger.error("Could not clear history.")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)