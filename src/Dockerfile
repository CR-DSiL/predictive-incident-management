#FROM python:3.10

FROM python:3.10-slim-bullseye
COPY . /app
# set a directory for the app
WORKDIR /app

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y \
 && apt-get install gettext-base -y 
# populate "ocbcinst.ini" as this is where ODBC driver config sits
RUN echo "[FreeTDS]\n\
Description = FreeTDS Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


# install dependencies
RUN pip install -r requirements.txt
# download spacy 
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader stopwords
# define the port number the container should expose
EXPOSE 8080 
EXPOSE 1433

# Entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# run the application
CMD ["python", "app.py"]