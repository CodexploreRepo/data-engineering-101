FROM python:3.12-slim

WORKDIR /app/

COPY requirements.txt requirements.txt
# libpq-dev gcc: for psycopg2 module
# curl         : to use curl command
RUN apt-get update \
    && apt-get -y install libpq-dev gcc curl \ 
    && pip install --upgrade pip \   
    && pip install --no-cache-dir -r requirements.txt

COPY ingestion.py ingestion.py
ENTRYPOINT [ "python", "ingestion.py"]