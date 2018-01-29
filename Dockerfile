# Use an official Python runtime as a parent image
FROM python:3.5-slim
#FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

#ENTRYPOINT [ "python" ]

#CMD [ "app.py" ]