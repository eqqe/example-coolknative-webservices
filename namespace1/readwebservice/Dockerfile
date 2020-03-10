FROM eqqe/python-docker-utils-webservices:3.7-slim

COPY ./namespace1/readwebservice ./namespace1/readwebservice

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.readwebservice.app:app