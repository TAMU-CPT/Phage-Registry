#!/bin/bash
out=$(date "+%Y-%m-%d.sql")
pg_dump postgres -U postgres -h $PHAGEREGDB_PORT_5432_TCP_ADDR -p $PHAGEREGDB_PORT_5432_TCP_PORT $DATABASE | gzip -f > /export/$out.gz
