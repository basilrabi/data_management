#!/usr/bin/bash

set -a
. $HOME/.gunicorn_env
set +a

$HOME/.virtualenvs/data_management/bin/python $HOME/data_management/manage.py sms_response
