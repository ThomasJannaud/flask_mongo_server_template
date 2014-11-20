#!/bin/bash

# Executed once when deploying. It puts the files to the right place on the server and restart the server service.

SERVICE_NAME=TestServer
TARGET_DIR=/home/test

service $SERVICE_NAME stop
sleep 2
pkill main.py
rm -f /var/run/${SERVICE_NAME}.pid
sleep 2
[ -f /etc/init.d/${SERVICE_NAME} ] && update-rc.d -f ${SERVICE_NAME} remove

# install server files
rm -rf $TARGET_DIR
cp -r /tmp/server ${TARGET_DIR}

# install init.d service
cp /tmp/${SERVICE_NAME} /etc/init.d/
chmod +x /etc/init.d/${SERVICE_NAME}
update-rc.d ${SERVICE_NAME} defaults
service $SERVICE_NAME start