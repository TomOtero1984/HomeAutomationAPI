#!/bin/bash
#
#
# This script is intended to be run as root
# 
# -Tom
#
#

# Including local env variables
source /Users/tomotero/.bash_profile

# Starting from project root
cd $HOME_AUTOMATION_API_DIR

source ./venv/bin/activate

cd flask
python3 -m gunicorn --certfile=$CERTFILE --keyfile=$KEYFILE -b 127.0.0.1:8443 app:app

