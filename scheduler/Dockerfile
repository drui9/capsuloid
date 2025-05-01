FROM python:3.12-alpine

RUN mkdir -p /var/www/scheduler
WORKDIR /var/www/scheduler

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ARG UID=1000
RUN adduser -D scheduler
RUN chown -R scheduler:scheduler /var/www

USER scheduler

CMD ["python3", "main.py"]

