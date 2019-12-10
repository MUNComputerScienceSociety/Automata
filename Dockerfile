FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk add gcc && pip install -r requirements.txt
CMD python Bot.py
