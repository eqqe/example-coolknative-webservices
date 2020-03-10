FROM eqqe/python-docker-utils-webservices:3.7-slim

COPY ./namespace1/webservice ./namespace1/webservice

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.webservice.app:app