FROM eqqe/python-docker-utils-webservices:3.7-slim

COPY ./monitoring/getlogs ./monitoring/getlogs

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 monitoring.getlogs.get_logs_ws:app