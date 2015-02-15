#!/bin/bash

# ./deploy.sh [--prod]
# 
# For security, deploys beta server by default.
#
# Script to be launched from local. It copies the necessary files, install them onto
# the server and restarts it.
# If it is the first install, you need to manually add the cron tab (hourly and daily) too.

HOST="91.236.239.90"  # beta

if [ "$1" != "--prod" ] && [ "$1" != "" ]
then
    echo "Usage : $0 [--prod]"
    exit
fi

if [ "$1" == "--prod" ]
then
    echo "deploy as prod"
    HOST="185.26.124.224"
fi


scp -P 2339 installTestServer.sh root@${HOST}:/tmp || exit
ssh -p 2339 root@${HOST} "bash /tmp/installTestServer.sh $1" || exit
