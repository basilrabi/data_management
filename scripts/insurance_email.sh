#!/usr/bin/bash

source $HOME/datamanagement/.virtualenvs/data_management/bin/activate

cd $HOME/datamanagement/data_management/

#Make sure to activate celery worker. Instruction below
#celery -A data_management worker -l INFO -f $HOME/%n%I.log

echo -e "from camp_admin.functions import get_expiring \nget_expiring()" | ./manage.py shell 