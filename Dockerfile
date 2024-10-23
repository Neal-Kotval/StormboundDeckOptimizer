# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base


FROM python:3.10.7

WORKDIR /usr/src/app

COPY . .

CMD [ "python3", "./app.py" ]
