#!/usr/bin/bash

set -a
. $HOME/.gunicorn_env
set +a

source $HOME/.virtualenvs/data_management/bin/activate &&
$HOME/data_management/manage.py sms_response
