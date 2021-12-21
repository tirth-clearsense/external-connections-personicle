from flask import jsonify
from flask import request, session, redirect
from flask import Blueprint

import requests
import pprint
import base64
from datetime import datetime
import threading

# from application import app
from application.models.base import db

healthkit_routes = Blueprint("healthkit_routes", __name__)

@healthkit_routes.route('/healthkit', methods=["GET", "POST"])
# @app.route('/index', methods=["GET", "POST"])
# @app.route('/user-dashboard', methods=['GET', 'POST'])
def dashboard_home():
    return jsonify({}), 200


@healthkit_routes.route('/healthkit/upload', methods=['POST'])
def fitbit_connection():
    if not request.json or not 'data' in request.json:
        abort(400)
    result = {
        'success': True
    }


    return jsonify(result), 201


