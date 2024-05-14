FROM python:3.9.1


RUN python -m pip install --upgrade pip
RUN apt-get install wget
RUN pip install pandas sqlalchemy pgcli psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 
ADD DATA /app/DATA
ENTRYPOINT [ "python", "ingest_data.py" ]