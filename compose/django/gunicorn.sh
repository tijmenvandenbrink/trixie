#!/bin/sh
python /trixie/manage.py collectstatic --noinput
/usr/local/bin/gunicorn bubbles.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/trixie
