FROM python:3.11

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml  ./

RUN poetry install

COPY . .