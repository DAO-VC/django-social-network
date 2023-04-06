FROM python:3.10

WORKDIR /usr/src/app
RUN apt update -y && apt install -y gcc python3-dev libjpeg-dev zlib1g-dev libffi-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT python manage.py migrate && python manage.py runserver