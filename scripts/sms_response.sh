#!/usr/bin/bash

source $HOME/.virtualenvs/data_management/bin/activate &&
sleep 1 &&
$HOME/.virtualenvs/data_management/bin/python $HOME/data_management/scripts/sms_response.py
