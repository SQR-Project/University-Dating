FROM ubuntu:jammy as build

ENV VENV_PATH=/venv-dating-app

COPY . /dating-app

RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3-pip build-essential libpq-dev

RUN python3.11 -m venv $VENV_PATH

RUN $VENV_PATH/bin/pip install -U pip setuptools

RUN $VENV_PATH/bin/pip install poetry

WORKDIR /dating-app

RUN $VENV_PATH/bin/poetry install

WORKDIR /dating-app/app

EXPOSE $PORT

CMD $VENV_PATH/bin/poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload

