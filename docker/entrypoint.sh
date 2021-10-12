#!/bin/sh

set -x
set -e

API_PATH="/var/www/html"
cd $API_PATH

#Do this every time, even though its wasteful on startup.
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py $@
