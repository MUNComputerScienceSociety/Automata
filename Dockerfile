FROM python:3.8-alpine3.10
COPY . /app
WORKDIR /app

RUN apk --update add --virtual build-dependencies gcc=8.3.0-r0 musl-dev=1.1.22-r3 --no-cache \
  && pip install -r requirements.txt \
  && apk del build-dependencies

CMD ["python", "Bot.py"]
