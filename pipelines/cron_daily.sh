#!/bin/bash
LOG_FILE="/var/log/test.daily"
date >> $LOG_FILE
mongo test_db --eval "pipeline='xxx'; arg1='a1';" /home/test/pipelines/aggregation.js >> $LOG_FILE
