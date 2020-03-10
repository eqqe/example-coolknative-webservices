FROM eqqe/python-docker-utils-webservices:3.7-slim

COPY ./namespace1/asyncwebservice ./namespace1/asyncwebservice

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.asyncwebservice.app:app