FROM python:3.10-slim-buster

# set a directory for the app
WORKDIR /usr/src/app

# copy all the necessary files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install MySQL driver
RUN pip install PyMySQL

# install gunicorn for the flask api
RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
