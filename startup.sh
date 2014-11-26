#!/bin/bash
export DOCKER_DB_NAME=postgres
export DOCKER_DB_USER=postgres
export DOCKER_DB_HOST=$PHAGEREGDB_PORT_5432_TCP_ADDR
export DJANGO_SETTINGS_MODULE=phageregistry.dockersettings

mkdir -p /opt/static/
python manage.py collectstatic --noinput -v 0

PASS=$(date +%s | sha256sum | base64 | head -c 32)
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '$PASS')" | ./manage.py shell
echo "Password is $PASS"
# Sync the database models
python manage.py syncdb --noinput

# Reindex data (this needs to be a cronjob somehow, or data needs to be exposed in a volume)
./manage.py rebuild_index --noinput

service nginx start

# Serve content
gunicorn phageregistry.wsgi -b 0.0.0.0:8000 &

tail -f /var/log/nginx/*.log

