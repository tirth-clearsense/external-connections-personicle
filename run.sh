#!/bin/bash
# install postgres dev libraries before installing python dependencies
# sudo apt-get install libpq-dev python-dev
# pip3 install -r requirements.txt
echo "Starting flask server"
if [ -z $INGESTION_PROD ];
then 
    # dev/staging environment
    echo "Dev/Staging Environment"
else
    # prod environment
    echo "Production environment"
    if [ -z $APP_CERTIFICATE_VALUE];
    then
        echo "SSL/TSL Certificate file missing"
        exit 1
    fi

    if [ -z $APP_KEY_VALUE];
    then
        echo "SSL/TSL Key file missing"
        exit 1
    fi 

    echo $APP_CERTIFICATE_VALUE > cert.pem
    echo $APP_KEY_VALUE > key.pem

fi

# gunicorn --certfile cert.pem --keyfile key.pem --bind 0.0.0.0:8000 run:app
gunicorn --bind 0.0.0.0:8000 run:app
