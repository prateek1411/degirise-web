# Dockerfile
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
FROM python:3.9-buster
# copy source and install dependencies

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/digiriseWeb
RUN mkdir -p /opt/app/pip_cache
COPY requirements.txt start-server.sh /opt/app/
COPY digiriseWeb /opt/app/digiriseWeb/
WORKDIR /opt/app

RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/bin/bash","/opt/app/start-server.sh"]
