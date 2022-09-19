#FROM python:3.10

FROM python:3.10-slim-bullseye
COPY . /app
# set a directory for the app
WORKDIR /app
# install dependencies
RUN pip install -r requirements.txt
# download spacy 
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader stopwords
# define the port number the container should expose
EXPOSE 8080
# run the application
CMD python app.py