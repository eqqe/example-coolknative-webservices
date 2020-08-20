FROM eqqe/python-docker-utils-webservices:3.8.5-slim-2020-08-19-17-02

COPY ./namespace1/readwebservice ./namespace1/readwebservice

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.readwebservice.app:app
