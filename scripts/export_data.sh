#!/usr/bin/bash

export address=datamanagement.tmc.nickelasia.com
export db_host=datamanagement.tmc.nickelasia.com
export db_name=data_management
export db_port=5432
export db_user=developer

if [ -z "${datadir}" ]; then
    echo "The variable 'datadir' is not defined. Data export aborted."
    exit 1
fi

if [ $DATA_MANAGEMENT_MEDIA_ROOT != "/home/datamanagement/media/uploads/" ]; then
  rsync -rlpvhPit --delete datamanagement@$address:/home/datamanagement/media/uploads/ $DATA_MANAGEMENT_MEDIA_ROOT
fi

source scripts/export_data_common.sh
