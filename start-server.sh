#!/usr/bin/env bash
# start-server.sh
cd digiriseWeb; gunicorn digiriseWeb.wsgi --user www-data --bind 0.0.0.0:8010 --workers 1 --reload

