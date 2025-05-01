FROM python:3.12-alpine

RUN mkdir -p /var/www/capsule
WORKDIR /var/www/capsule


COPY wsgi.py wsgi.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ARG UID=1000
RUN adduser -D capsule
RUN chown -R capsule:capsule /var/www

USER capsule
ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "wsgi:app"]

