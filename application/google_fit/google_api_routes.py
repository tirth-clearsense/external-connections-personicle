from flask import request, session, redirect, url_for
from flask import Blueprint
from flask.json import jsonify
from flask.wrappers import Response
from authlib.integrations.flask_client import OAuth
import os
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow

from application.utils.user_credentials_manager import add_access_token
from application.config import GOOGLE_FIT_CONFIG, PROJ_LOC
oauth_config = GOOGLE_FIT_CONFIG
oauth = OAuth()

from .google_fit_import_module import google_fit_data_import

APP_SCOPE = [
        "https://www.googleapis.com/auth/fitness.sleep.read",
        "https://www.googleapis.com/auth/fitness.heart_rate.read",
        "https://www.googleapis.com/auth/fitness.reproductive_health.read",
        "https://www.googleapis.com/auth/fitness.body_temperature.read",
        "https://www.googleapis.com/auth/fitness.oxygen_saturation.read",
        "https://www.googleapis.com/auth/fitness.blood_glucose.read",
        "https://www.googleapis.com/auth/fitness.blood_pressure.read",
        "https://www.googleapis.com/auth/fitness.nutrition.read",
        "https://www.googleapis.com/auth/fitness.body.read",
        "https://www.googleapis.com/auth/fitness.location.read",
        "https://www.googleapis.com/auth/fitness.activity.read"
    ]

# from application import app
from application.models.base import db
google_API_routes = Blueprint("google_fit_routes", __name__)

@google_API_routes.route('/google-fit')
def dashboard_home():
    return "Google routes"

@google_API_routes.route("/google-fit/connection", methods=['GET', 'POST'])
def google_fit_connection():
    # print("in google route")
    user_id = request.args.get("user_id", None)
    if user_id is None:
        return Response("User not logged in", 401)
    
    for k in list(session.keys()):
        session.pop(k)

    session['user_id'] = user_id
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.join(PROJ_LOC, GOOGLE_FIT_CONFIG['SECRET_JSON']),
        scopes=APP_SCOPE)

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = GOOGLE_FIT_CONFIG['REDIRECT_URL']
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true', enable_reauth_refresh='true')
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
        
    session['state'] = state
    # Enable incremental authorization. Recommended as a best practice.

    return redirect(authorization_url)

@google_API_routes.route("/google-fit/oauth/access_token", methods=['GET'])
def get_access_token():
    user_id = session.get("user_id", None)
    if user_id is None:
        return Response("User not logged in", 401)
    error_resp = request.args.get("error", None)
    if error_resp:
        return Response(error_resp, 401)
    auth_code = request.args.get("code", None)
    
    auth_response = request.url
    if auth_code is None:
        return Response("Error while accessing authorizarion code", 401)

    # print(auth_code, state)
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.join(PROJ_LOC, GOOGLE_FIT_CONFIG['SECRET_JSON']),
        scopes=APP_SCOPE,
        state=state)
    flow.redirect_uri = GOOGLE_FIT_CONFIG['REDIRECT_URL']

    flow.fetch_token(authorization_response=auth_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expires_at': credentials.expiry
    }

    print(session)
    action ,user_record = add_access_token(user_id, service_name='google-fit', access_token=credentials.token, expires_in=credentials.expiry,
                            created_at=datetime.utcnow(), external_user_id=None, refresh_token=credentials.refresh_token)

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
    # th = threading.Thread(target=initiate_fitbit_data_import, args=(user_id,))
    google_fit_data_import(user_id)
    
    return result
