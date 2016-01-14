#!/bin/bash

# Runs the mongoDB mapreduce pipelines and backs up the whole database
# WARNING : back up only small databases...

LOG_FILE="/var/log/server_name.daily"
date >> $LOG_FILE
mongo REPLACEME_DBNAME --eval "pipeline='by_question_sum_days';" /home/tsapp/serveur/pipelines/aggregation.js >> $LOG_FILE
# backup db and uploads
timestamp=$(date +-%y-%m-%d)
mongodump --quiet --out /tmp/aaa
cp -r /home/REPLACEME_TOP_DIRECTORY/serveur/serveur/static/upload* /tmp/aaa/
tar -czf /opt/backup_db_mongo_${timestamp}.tar.gz /tmp/aaa