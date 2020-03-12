FROM python:3.7-slim

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./api_utils ./api_utils
COPY ./api ./api
COPY ./definitions.py ./definitions.py
COPY ./lib_logs ./lib_logs

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 api.entrypoints:app