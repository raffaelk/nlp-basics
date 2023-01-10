from flask import Flask, render_template, url_for, request, redirect
import requests
from sqlalchemy import create_engine, text
import os

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
    with engine.connect() as con:
        con.execute("CREATE DATABASE IF NOT EXISTS sentiment_app;")

        con.execute(f"""
        CREATE TABLE IF NOT EXISTS sentiment_app.predictions (
            id INT AUTO_INCREMENT,
            review TEXT,
            prediction VARCHAR(20),
            PRIMARY KEY(ID)
        );
        """)
        
    return engine

# set up database and get engine
ENGINE = set_up_database(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        review = {"review": request.form['content']}
        
        response = requests.post('http://localhost:5001/predict', json=review).json()
        
        with ENGINE.connect() as con:
            con.execute(text(f"""
            INSERT INTO sentiment_app.predictions (review, prediction)
            VALUES (:rev, :pred);
            """), rev=review['review'], pred=response['prediction'])
        
        return redirect('/')
        
    else:
        with ENGINE.connect() as con:
            response = con.execute("""
            SELECT * 
            FROM sentiment_app.predictions
            ORDER BY id DESC;
            """)
        
        review_list = list(response)
        
        return render_template('index.html', review_list=review_list)

if __name__ == "__main__":
    app.run(debug=True)