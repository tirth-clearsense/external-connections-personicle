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
from . import healthkit_upload
from application.config import IOS_APP_CONFIG
import logging
config = IOS_APP_CONFIG


healthkit_routes = Blueprint("healthkit_routes", __name__)
LOG = logging.getLogger(__name__)

@healthkit_routes.route('/healthkit', methods=["GET", "POST"])
# @app.route('/index', methods=["GET", "POST"])
# @app.route('/user-dashboard', methods=['GET', 'POST'])
def dashboard_home():
    return jsonify({}), 200


@healthkit_routes.route('/healthkit/upload', methods=['POST'])
def healthkit_connection():
    if not request.json or not 'data' in request.json:
        LOG.error("JSON or data not found")
        LOG.error(request.get_data(as_text=True))
        return jsonify({}), 400

    result = {
        'success': False
    }


    if 'test_key' in request.json:
        if request.json['test_key'] == config['KEY']:
            data = request.json['data']
            healthkit_upload.send_records_to_producer('user_id', data, 'sleep', limit=5)
            result = {
                'success': True
            }

            LOG.info("Received healthkit data")
            LOG.info('Number of data records:', len(data))
            if len(data) > 0:
                LOG.info('Sample record:', data[0])

            return jsonify(result), 201
    else:
        LOG.error("Received API call without authorization test_key")

    return jsonify(result), 400

