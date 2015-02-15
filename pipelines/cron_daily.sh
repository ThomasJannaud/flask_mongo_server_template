#!/bin/bash
LOG_FILE="/var/log/server_name.daily"
date >> $LOG_FILE
mongo db_name --eval "pipeline='by_question_sum_days';" /home/tsapp/serveur/pipelines/aggregation.js >> $LOG_FILE
# backup db and uploads
timestamp=$(date +-%y-%m-%d)
mongodump --quiet --out /tmp/aaa
cp -r /home/tsapp/serveur/serveur/static/upload* /tmp/aaa/
tar -czf /opt/backup_db_mongo_${timestamp}.tar.gz /tmp/aaa