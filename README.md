# external-connections-personicle
API server for managing data import from 3rd party connections (such as fitbit) to personicle. We have provided instructions for running and testing the app server on your local dev environment, please contact the repository administrators for access to staging environment. Changes to the prod environment can only be made once approved by the administrators.


# Getting started

## Config file

Create a config file `config.ini` under the main application. This file contains the client secrets, event hub configuration and database urls for the application.
```
[HOST]
HOST_ADDRESS=https://localhost:5000
[GOOGLE_FIT]
CLIENT_ID=XXX
CLIENT_SECRET=XXX
REDIRECT_URL=/google-fit/oauth/access_token
AUTH_URL=https://accounts.google.com/o/oauth2/auth
API_ENDPOINT=https://www.googleapis.com/fitness/v1/
TOKEN_URL=https://oauth2.googleapis.com/token
SECRET_JSON=config_json/client_secret_XXX.json
[FITBIT]
CLIENT_ID=XXX
CLIENT_SECRET=XXX
REDIRECT_URL=/fitbit/oauth/access-token/
AUTH_URL=https://www.fitbit.com/oauth2/authorize
REQUEST_URL=https://api.fitbit.com/oauth2/token
API_ENDPOINT=https://api.fitbit.com
[SQLITE]
DATABASE=userDatabase/external_tokens.db

[EVENTHUB]
CONNECTION_STRING=XXX
EVENTHUB_NAME=XXX
SCHEMA_REGISTRY_FQNS=XXX
SCHEMA_REGISTRY_GROUP=XXX

[IOS_APP]
KEY=XXX
```

The fields with values `XXX` are sensitive secrets and should be defined by the developers and not shared in the repository.


## Setting up the virtual environment
We recommend using Python3.7+ for running the Flask application. You create a python virtual environment for the application as follows:
1) Follow the instruction listed [here](https://pip.pypa.io/en/stable/installation/) to install pip.
2) Install `virtualenv` to manage the virtual environments for your application.
   ```
   python3 -m pip install --user virtualenv
   ```
3) Create a virtual environment
   ```python3 -m venv personicle-env```
4) Activate the virtual environment for the current session
   ```source personicle-dev/bin/activate```
5) Install the required packages listed in `requirements.txt` usign the following command
   ```
   pip install -r requirements.txt
   ```
Note: You can deactivate the virutal environment using the command `deactivate`.

## Running the application
You can now run the application (in the virtual environment created in previous steps) using the following command
```
python run.py
```

This will host the flask application on port `5000` on `localhost`.
