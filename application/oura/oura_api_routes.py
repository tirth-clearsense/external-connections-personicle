from flask import Blueprint
from flask import jsonify
from flask import request, session, redirect
from requests.auth import HTTPBasicAuth
import requests
import traceback
import logging
from flask.wrappers import Response
from application.config import OURA_CONFIG, HOST_CONFIG
from datetime import datetime
from application.utils.user_credentials_manager import add_access_token, verify_user_connection
from application.models.base import db
from .oura_import_module import initiate_oura_data_import

oura_routes = Blueprint("oura_routes", __name__)
LOG = logging.getLogger(__name__)

@oura_routes.route("/oura/connection", methods=['GET', 'POST'])
def oura_connection():
    user_id = request.args.get("user_id", None)
    personicle_access_token = request.headers.get("Authorization")
  
    if user_id is None:
        LOG.error("Unauthorised access: Denied")
        return Response("User not logged in", 401)

    session['user_id'] = user_id
    session['personicle_token'] = personicle_access_token
    LOG.info("OURA authorization for user: {}".format(session['user_id']))

    if verify_user_connection(personicle_user_id=session['user_id'], connection_name='oura'):
        LOG.info("User {} has active access token for oura".format(session['user_id']))
        try:
            resp = initiate_oura_data_import(user_id, personicle_access_token)
            success= True
        except Exception as e:
            LOG.error(traceback.format_exc(e))
            resp = {'error': str(e)}
            success = False
        result = jsonify(resp)
        return result
        
   
    return redirect('/oura/oauth/code-callback')

@oura_routes.route('/oura/oauth/code-callback')
def get_code():
    if session['user_id'] is None:
        return Response("User not logged in", 401)
    scopes = "email%20personal%20daily%20heartrate%20workout%20tag%20session"
    if 'user_id' not in session:
        return 'Use proper channels'

    if 'request_sent' not in session:
        print("Redirect url: {}".format(HOST_CONFIG['HOST_ADDRESS'] + OURA_CONFIG['REDIRECT_URL']))
        session['request_sent'] = True
        print("request sent")
        return redirect("{}?client_id={}&redirect_uri={}&scope={}&response_type=code".format(OURA_CONFIG['AUTH_URL'],
                OURA_CONFIG['CLIENT_ID'] ,HOST_CONFIG['HOST_ADDRESS'] + OURA_CONFIG['REDIRECT_URL'], scopes))
    return "Already connected"

@oura_routes.route('/oura/oauth/access-token/')
def get_token():
    if session['user_id'] is None:
        return Response("User not logged in", 401)
    # need personicle user id in session
    user_id = session['user_id']
    personicle_token = session.get("personicle_token", None)
    code = request.args.get('code')
    request_params = {'grant_type': 'authorization_code',
                      'code': code,
                      'redirect_uri': HOST_CONFIG['HOST_ADDRESS'] + OURA_CONFIG['REDIRECT_URL']
                     }
    request_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(OURA_CONFIG['TOKEN_URL'], data=request_params, headers= request_headers,auth=HTTPBasicAuth(f"{OURA_CONFIG['CLIENT_ID']}", f"{OURA_CONFIG['CLIENT_SECRET']}"))
    resp = res.json()

    if res.status_code == 400:
         return jsonify({"message": "failed"})
    action ,user_record = add_access_token(user_id, service_name='oura', access_token=resp['access_token'], expires_in=resp['expires_in'],
                            created_at=datetime.utcnow(), refresh_token=resp['refresh_token'])
    
    try:
        if action == 'add':
            db.session.add(user_record)
        else:
            pass
        result = jsonify(success=True)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        result = jsonify(success=False)
    try:
        resp = initiate_oura_data_import(user_id, personicle_token)
        result = jsonify(resp)
        return result
    except Exception as e:
        LOG.error(traceback.format_exc())
        return jsonify(success=False, message="Error while initiating download request")