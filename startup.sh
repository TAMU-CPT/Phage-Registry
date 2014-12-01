#!/bin/bash
. env.sh

# https://github.com/nathanleclaire/laraveldocker/commit/fb0f579f1482ba3396255b36c52506d71ef7fbcc#diff-76a1947cdef4e9ab08d8746a400e3681
echo "Stalling for DB"
while true;
do
    nc -q 1 $DOCKER_DB_HOST 5432 > /dev/null && break
    sleep 1
done

mkdir -p /opt/static/
python manage.py collectstatic --noinput -v 0

# Sync the database models
python manage.py syncdb --noinput

PASS=$(date +%s | sha256sum | base64 | head -c 32)
# This is kinda bad :(
echo "from django.contrib.auth.models import User;user = User.objects.get(username='admin'); user.set_password('$PASS'); user.save()" | ./manage.py shell
echo "Password is $PASS"

# Reindex data (this needs to be a cronjob somehow, or data needs to be exposed in a volume)
./manage.py rebuild_index --noinput

service nginx start

# Serve content
gunicorn phageregistry.wsgi -b 0.0.0.0:8000 &

tail -f /var/log/nginx/*.log

