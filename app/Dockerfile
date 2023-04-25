FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/
RUN poetry install

COPY . ./

ENTRYPOINT python -u ./manage.py runserver 0.0.0.0:8000
