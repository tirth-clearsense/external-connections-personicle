from flask import Flask
from flask import render_template
from flask import request, session, redirect

import requests
import pprint
import json
import configparser
import os
import base64

app = Flask(__name__)
config={}

PUBLIC_IP='http://127.0.0.1'
# EXCHANGE_ENDPOINT = 'https://www.strava.com/oauth/token'

REDIR_URL = PUBLIC_IP+"/oauth/access_token"

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@app.route('/userDash', methods=['GET', 'POST'])
def dashboard_home():
    return True

@app.route('/fitbitConnection', methods=['GET', 'POST'])
def fitbit_connection():
    session_id = True #request['data']['session_id']
    session.clear()
    session['user_id'] = session_id
    return redirect('oauth/code_callback')
    

def hello():
    if 'message' not in session:
        session.clear()
        return render_template('strava_login.html', redir_url=REDIR_URL, user_attr="/oauth/user_attr",message=""), 200
    else:
        message = session['message']
        session.clear()
        return render_template('strava_login.html', redir_url=REDIR_URL, user_attr="/oauth/user_attr", message=message), 200


@app.route("/oauth/user_attr", methods=['POST'])
def get_user_attr():
    user_attr = request.form
    pprint.pprint(user_attr)
    if user_attr['height'] == "" or user_attr['weight'] == "" or user_attr['waist'] == "":
        session['message'] = "Fields marked * cannot be left blank"
        return redirect('/index')
    session['user_dat'] = user_attr
    return redirect('oauth/code_callback')


# OAuth call back with the client token
# store this and use to get access code
@app.route('/oauth/code_callback/')
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

@app.route('/oauth/access_token/')
def get_access_token():
    # assert 'request_sent' in session
    # session.pop('request_sent')
    code = request.args.get('code')
    print(code)
    # basic_code = base64.urlsafe_b64encode(oauth_config['CLIENT_ID'] + ':' + oauth_config['CLIENT_SECRET'])
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
    # resp['athlete_id'] = resp['athlete']['id']

    # session_id = session['user_id']
    # for i in user_dat.keys():
    #     resp[i] = user_dat[i]
    pprint.pprint(resp)

    # store a user's access token and refrezsh tokens in a sqlite db
    

    return resp


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    oauth_config = config['FITBIT']

    app.secret_key = os.urandom(24)
    app.run(debug=True)