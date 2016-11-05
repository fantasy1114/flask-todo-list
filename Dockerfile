FROM alpine:3.4

# from https://github.com/frol/docker-alpine-python3
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

ADD . /code
WORKDIR /code
RUN pip install gunicorn
RUN pip install -r requirements.txt
