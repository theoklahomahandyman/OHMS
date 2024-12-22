#!/bin/sh

NAME='back-end'
DJANGODIR='OHMS/back-end'
SOCKFILE=/OHMS/back-end/run/gunicorn.sock
USER=ohms-user
GROUP=ohms
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=main.settings
DJANGO_WSGI_MODULE=main.wsgi
TIMEOUT=120

cd $DJANGODIR
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec .venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers $NUM_WORKERS --timeout $TIMEOUT --user=$USER --group=$GROUP --bind=unix:$SOCKFILE --log-level=debug --log-file=-
