# pull official base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR ./app

# install dependencies
COPY requirements.txt /app/

RUN pip install -r requirements.txt

# copy project
COPY . /app/