#!/bin/bash

# Script to be launched from local. It copies the necessary files, install them onto
# the server and restarts it.
# If it is the first install, you need to manually add the cron tab (hourly and daily) too.

HOST="91.236.239.90"

rm -rf /tmp/server
cp -r ../../server /tmp/server
rm -rf /tmp/server/.git

# Initiates first connection so that subsequent sshpass commands work.
ssh -p 2339 root@${HOST} "rm -rf /tmp/server" || exit
scp -P 2339 -r /tmp/server root@${HOST}:/tmp || exit
scp -P 2339 StorycsServer root@${HOST}:/tmp || exit
scp -P 2339 installTestServer.sh root@${HOST}:/tmp || exit
ssh -p 2339 root@${HOST} "bash /tmp/installTestServer.sh" || exit