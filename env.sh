#!/bin/bash
export DOCKER_DB_NAME=postgres
export DOCKER_DB_USER=postgres
export DOCKER_DB_HOST=$PHAGEREGDB_PORT_5432_TCP_ADDR
export DJANGO_SETTINGS_MODULE=phageregistry.dockersettings
