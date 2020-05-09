FROM python:3.8-slim

RUN pip install pipenv

RUN mkdir /app

WORKDIR /app

ADD . .

RUN  pipenv install --system --clear

WORKDIR /app/src

CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload