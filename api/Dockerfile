FROM eqqe/python-docker-utils-webservices:3.8.5-slim-2020-08-19-17-02

COPY ./api ./api

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 api.entrypoints:app
