FROM python:3.7-slim

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./definitions.py ./definitions.py
COPY ./namespace1/webservice ./namespace1/webservice
COPY ./lib_logs ./lib_logs

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 namespace1.webservice.app:app