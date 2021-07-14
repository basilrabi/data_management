#!/usr/bin/bash

rm -f log_test

source $HOME/.virtualenvs/data_management/bin/activate &&
sleep 1 &&
./manage.py test 2>&1 | tee -a log_test
