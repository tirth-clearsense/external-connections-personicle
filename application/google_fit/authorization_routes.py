from flask import request, session
from flask import Blueprint
from flask.wrappers import Response
from authlib.integrations.flask_client import OAuth

import pprint
from datetime import datetime

from application.config import GOOGLE_FIT_CONFIG
oauth_config = GOOGLE_FIT_CONFIG
oauth = OAuth()

APP_SCOPE = "https://www.googleapis.com/auth/fitness.sleep.read%20https://www.googleapis.com/auth/fitness.heart_rate.read%20https://www.googleapis.com/auth/fitness.reproductive_health.read%20https://www.googleapis.com/auth/fitness.body_temperature.read%20https://www.googleapis.com/auth/fitness.oxygen_saturation.read%20https://www.googleapis.com/auth/fitness.blood_glucose.read%20https://www.googleapis.com/auth/fitness.blood_pressure.read%20https://www.googleapis.com/auth/fitness.nutrition.read%20https://www.googleapis.com/auth/fitness.body.read%20https://www.googleapis.com/auth/fitness.location.read%20https://www.googleapis.com/auth/fitness.activity.read"
google = oauth.register(
    name='google',
    client_id=GOOGLE_FIT_CONFIG['CLIENT_ID'],
    client_secret=GOOGLE_FIT_CONFIG['CLIENT_SECRET'],
    access_token_url=GOOGLE_FIT_CONFIG['TOKEN_URL'],
    access_token_params=None,
    authorize_url=GOOGLE_FIT_CONFIG['AUTH_URL'],
    authorize_params=None,
    api_base_url=GOOGLE_FIT_CONFIG['API_ENDPOINT'],
    client_kwargs={"scope": " ".join([
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
    ])
    }
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
    redirect_uri = GOOGLE_FIT_CONFIG['REDIRECT_URL']#url_for('google-fit/oauth/code-callback', external=True)

    return google_fit.authorize_redirect(redirect_uri)


@google_fit_routes.route("/google-fit/oauth/access_token")
def get_token():
    user_id = session.get("user_id", None)
    if user_id is None:
        return Response("User not logged in", 401)

    google_fit = oauth.create_client("google")
    token = google_fit.authorize_access_token()
    refresh_token = google_fit.authorize_refresh_token()

    print(token)

    pprint.pprint(refresh_token)
    return token