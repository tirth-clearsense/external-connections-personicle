from flask import jsonify
from flask import request, session, redirect,url_for
from flask import Blueprint
from flask_cors import CORS
from application.okta.helpers import  is_authorized

okta_routes = Blueprint("okta_routes", __name__)
CORS(okta_routes)

@okta_routes.route('/authenticate', methods=["GET", "POST"])
def authenticate():
    if not is_authorized(request):
        return "Unauthorized", 401
    # return jsonify({"message":True})

    # redir = redirect(url_for('fitbit_routes.fitbit_connection'))
    print(request.headers.get("Authorization"))
    # redir.headers['headers'] = request.headers
    # return redir
    return redirect(f"/fitbit/connection?user_id={request.args.get('user_id', None)}")
    # return jsonify({"message": True})
