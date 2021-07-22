FROM python:3.8.8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip --no-cache-dir install poetry

COPY pyproject.toml .
RUN poetry install --no-dev

COPY . .

