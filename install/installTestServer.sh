#!/bin/bash
#
# ./installOpinionazerServer.sh [--prod]
#
# For security, deploys beta server by default.
#
# Executed once when deploying. It puts the files to the right place on the server and restart the server service.

if [ "$1" == "--prod" ]
then
    SERVICE_NAME=OpinionazerServer
    server_arg="--prod"
else
    SERVICE_NAME=OpinionazerServer_Beta
    server_arg="--beta"
fi
TARGET_DIR=/home/my_server_directory

service $SERVICE_NAME stop
sleep 2
pkill -f "run_server.py $server_arg"
rm -f /var/run/${SERVICE_NAME}.pid
sleep 2

# install server files
cd $TARGET_DIR
git pull
mkdir -p ${TARGET_DIR}/serveur/serveur/static/upload_debug
mkdir -p ${TARGET_DIR}/serveur/serveur/static/upload_beta
mkdir -p ${TARGET_DIR}/serveur/serveur/static/upload_prod

service $SERVICE_NAME start