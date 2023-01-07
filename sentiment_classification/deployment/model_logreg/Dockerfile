FROM python:3.7-slim-buster

# set a directory for the app
WORKDIR /usr/src/app

# copy all the necessary files to the container
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
