#!/bin/sh
python manage.py db_load ncbi.json hxr NCBI --clean_name
python manage.py db_load embl.json hxr EBI --clean_name
python manage.py db_load phagesdb.json hxr mycophagedb
