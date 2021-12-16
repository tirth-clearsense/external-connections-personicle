from os import access
from flask import jsonify
from flask import request, session, redirect
from flask import Blueprint
from flask.helpers import url_for
from flask.wrappers import Response
from authlib.integrations.flask_client import OAuth

import requests
import pprint
import base64
from datetime import datetime
import threading

from application.config import GOOGLE_FIT_CONFIG
oauth_config = GOOGLE_FIT_CONFIG
oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=GOOGLE_FIT_CONFIG['CLIENT_ID'],
    client_secret=GOOGLE_FIT_CONFIG['CLIENT_SECRET'],
    access_token_url=GOOGLE_FIT_CONFIG['TOKEN_URL'],
    access_token_params=None,
    authorize_url=GOOGLE_FIT_CONFIG['AUTH_URL'],
    authorize_params=None,
    api_base_url=GOOGLE_FIT_CONFIG['API_ENDPOINT'],
    client_kwargs={}
)

# from application import app
from application.models.base import db

google_fit_routes = Blueprint("google_fit_routes", __name__)

@google_fit_routes.route('/google-fit')
def dashboard_home():
    return "Google routes"

@google_fit_routes.route("/google-fit/connection", methods=['GET', 'POST'])
def google_fit_connection():
    # print("in google route")
    user_id = request.args.get("user_id", None)
    if user_id is None:
        return Response("User not logged in", 401)

    session['user_id'] = user_id

    google_fit = oauth.create_client("google")
    redirect_uri = url_for('google-fit/oauth/code-callback', external=True)

    return google_fit.authorize_redirect(redirect_uri)


@google_fit_routes.route("/google-fit/oauth/code-callback")
def get_token():
    user_id = session.get("user_id", None)
    if user_id is None:
        return Response("User not logged in", 401)

    google_fit = oauth.create_client("google")
    token = google_fit.authorize_access_token()

    print(token)
    pass