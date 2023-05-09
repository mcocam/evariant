FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    PYTHONIOENCODING=utf-8

RUN apt-get update && apt-get install -y \
    build-essential \
    clustalw

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY ./app /app