from flask import Flask, jsonify
from flask import render_template
from flask import request, session, redirect
from flask_sqlalchemy import SQLAlchemy

import requests
import pprint
import configparser
import os
import base64
from datetime import datetime
import threading

PUBLIC_IP='http://127.0.0.1'
REDIR_URL = PUBLIC_IP+"/oauth/access_token"

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
oauth_config = config['FITBIT']

sqlite_config = config['SQLITE']

os.makedirs(os.path.join(sqlite_config['DATABASE_LOCATION']), exist_ok=True)

app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(sqlite_config['DATABASE_LOCATION'], sqlite_config['DATABASE_NAME']))

db = SQLAlchemy(app)

from user_credential_manager import add_access_token
from data_import_modules import IMPORT_MODULES


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@app.route('/user-dashboard', methods=['GET', 'POST'])
def dashboard_home():
    return True

@app.route('/fitbit-connection', methods=['GET', 'POST'])
def fitbit_connection():
    session_id = True #request['data']['session_id']
    session.clear()
    request_data = request.args
    session['user_id'] = session_id
    print(request_data)
    session['redirect_url'] = request_data.get("redirect_uri")
    return redirect('/oauth/code-callback')
    

# OAuth call back with the client token
# store this and use to get access code
@app.route('/oauth/code-callback/')
def get_token():
    scope = "activity%20heartrate%20location%20nutrition%20profile%20sleep%20weight"
    print(session.keys())
    if 'user_id' not in session:
        return 'Use proper channels'
    if 'request_sent' not in session:
        session['request_sent'] = True
        print("request sent")
        return redirect("{}?client_id={}&redirect_uri={}&scope={}&response_type=code".format(oauth_config['AUTH_URL'],
                oauth_config['CLIENT_ID'] ,oauth_config['REDIRECT_URL'], scope))
    return "Already connected"


# Store the access token in sqlite db and initiate data import
@app.route('/oauth/access-token/')
def get_access_token():
    # need personicle user id in session
    user_id = "test_id"
    code = request.args.get('code')
    # print(session['user_id'])
    print(code)

    message = oauth_config['CLIENT_ID'] + ':' + oauth_config['CLIENT_SECRET']
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    basic_code = base64_bytes.decode('ascii')


    request_params = {'grant_type': 'authorization_code',
                      'client_id': oauth_config['CLIENT_ID'],
                      'client_secret': oauth_config['CLIENT_SECRET'],
                      'code': code,
                      'redirect_uri': oauth_config['REDIRECT_URL']}
    request_headers = {'Authorization': 'Basic {}'.format(basic_code),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
    resp = requests.post(oauth_config['REQUEST_URL'], data=request_params, headers=request_headers).json()

    resp["client_token"] = code

    pprint.pprint(resp)

    # store a user's access token and refresh tokens in a sqlite db
    action ,user_record = add_access_token(user_id, service_name='fitbit', access_token=resp['access_token'], expires_in=resp['expires_in'],
                            created_at=datetime.utcnow(), external_user_id=resp['user_id'], refresh_token=resp['refresh_token'],
                            scope=resp['scope'])

    try:
        if action == 'add':
            db.session.add(user_record)
        else:
            pass
        result = jsonify(success=True)
        db.session.commit()
    except Exception as e:
        print(e)
        # raise e
        db.session.rollback()
        result = jsonify(success=False)
    # return resp
    th = threading.Thread(target=IMPORT_MODULES['fitbit'], args=(user_id, ))
    th.start()

    return result


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)