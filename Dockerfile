# Menggunakan base image Python versi 3.10 slim
FROM python:3.9

ENV PYTHONBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

# Install pkg-config
RUN apt-get update && \
    apt-get install -y pkg-config && \
    apt-get install -y default-libmysqlclient-dev && \
    pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app