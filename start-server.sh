#!/usr/bin/env bash
# start-server.sh
#cd digiriseWeb; gunicorn digiriseWeb.wsgi --user www-data --bind 0.0.0.0:8010 --workers 1 --reload
uwsgi --http :8010  --chdir digiriseWeb/ --wsgi-file digiriseWeb/wsgi.py --master --processes 2 --threads 2 --stats 127.0.0.1:9191


