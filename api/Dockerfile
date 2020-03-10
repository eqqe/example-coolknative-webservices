# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Install production dependencies.
RUN pip install Flask==1.1.1 gunicorn==20.0.4 requests==2.16.0 redis==3.4.1 fluent-logger==0.9.5

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./api_utils ./api_utils
COPY ./api ./api
COPY ./definitions.py ./definitions.py
COPY ./lib_logs ./lib_logs

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 api.entrypoints:app