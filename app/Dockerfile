FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .
CMD cd app
CMD python ./manage.py runserver 0.0.0.0:8000
