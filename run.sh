#!/bin/bash
# install postgres dev libraries before installing python dependencies
sudo apt-get install libpq-dev python-dev
pip3 install -r requirements.txt
echo "Starting flask server"

gunicorn --bind 0.0.0.0:8000 run:app
