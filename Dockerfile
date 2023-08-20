# syntax=docker/dockerfile:1

FROM python:3.11-slim

LABEL maintainer="stanar278@gmail.com"

WORKDIR /app

COPY . .

CMD [ "python3", "main.py" ]

