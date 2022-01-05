sql_script () {
    if [ "$3" != "" ];
    then
        db_role=$3
    else
        db_role=$db_user
    fi
    echo "Running $1/$2 script." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    psql -h $db_host -p $db_port -U $db_role -w $db_name -a -f scripts/sql/$1/$2.pgsql 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "sql $1-$2, $time_elapsed" >> log_upload_data_time.csv
}

upload_orm () {
    echo "Running $1 script." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    python3 manage.py shell < scripts/upload_data/$1.py 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "orm $1, $time_elapsed" >> log_upload_data_time.csv
}

vacuum () {
    echo "Running vacuum analyze on $1." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    psql -h $db_host -p $db_port -U $db_user -w $db_name -a -c "VACUUM ANALYZE $1" 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "vacuum $1, $time_elapsed" >> log_upload_data_time.csv
}
