FROM python:3.11-alpine3.18
COPY . /app
WORKDIR /app
RUN apk --update add --virtual build-dependencies gcc musl-dev libxml2-dev libxslt-dev --no-cache \
  && pip install -r requirements.txt \
  && apk del build-dependencies

CMD ["python", "Bot.py"]
