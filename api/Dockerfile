FROM eqqe/python-docker-utils-webservices:3.7-slim

COPY ./api ./api

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 api.entrypoints:app