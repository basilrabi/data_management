#!/usr/bin/bash

export datadir=data
export address=datamanagement.tmc.nickelasia.com
export db_host=datamanagement.tmc.nickelasia.com
export db_name=data_management
export db_port=5432
export db_user=developer

rsync -rlpvhPit --delete datamanagement@$address:/media/tmc/nginx/81/uploads/ $DATA_MANAGEMENT_MEDIA_ROOT

source scripts/export_data_common.sh
