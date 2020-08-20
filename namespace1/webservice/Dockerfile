FROM eqqe/python-docker-utils-webservices:3.8.5-slim-2020-08-19-17-02

COPY ./namespace1/webservice ./namespace1/webservice

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.webservice.app:app
