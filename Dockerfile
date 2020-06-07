FROM python:alpine3.8

ADD . /app
WORKDIR /app

CMD [ "python", "./main.py"]