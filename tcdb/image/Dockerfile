FROM python:3.11.3-alpine3.18

WORKDIR /srv
COPY ./tcdb/image/requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install -r /tmp/requirements.txt
