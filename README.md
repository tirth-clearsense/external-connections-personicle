# external-connections-personicle
API server for managing data import from 3rd party connections (such as fitbit) to personicle


# Getting started

## Config file

Create a config file config.ini under the main application.
```
[FITBIT]
...

[IOS_APP]
...
```

## Data ingestion module patterns

Every external data service package is self contained and placed inside the application directory.

Every data connection module defines api routes using flask-blueprints and defines a ```init_app(app: Flask)``` method in the ```__init__.py``` module that registers the blueprint with the ```app``` object.

