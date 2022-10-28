FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PORT=$PORT
ENV DB_HOST=host.docker.internal
ENV DB_USER=root
ENV DB_PASS=root

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port $PORT

