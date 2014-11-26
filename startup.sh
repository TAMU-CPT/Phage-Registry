#!/bin/bash
export DOCKER_DB_NAME=postgres
export DOCKER_DB_USER=postgres
export DOCKER_DB_HOST=$PHAGEREGDB_PORT_5432_TCP_ADDR
export DJANGO_SETTINGS_MODULE=phageregistry.dockersettings

# Sync the database models
python manage.py syncdb --noinput

# Reindex data (this needs to be a cronjob somehow, or data needs to be exposed in a volume)
./manage.py rebuild_index --noinput

# Serve content
gunicorn phageregistry.wsgi
