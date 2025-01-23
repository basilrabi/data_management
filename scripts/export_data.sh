#!/usr/bin/bash

if [ "$(whoami)" != "datamanagement" ]; then
	echo "You can't use this script $(whoami)!."
    exit 1
fi

export address=datamanagement.tmc.nickelasia.com
export db_host=datamanagement.tmc.nickelasia.com
export db_name=data_management
export db_port=5432
export db_user=developer

if [ -z "${datadir}" ]; then
    echo "The variable 'datadir' is not defined. Data export aborted."
    exit 1
fi

source scripts/export_data_common.sh

